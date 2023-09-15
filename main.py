from fastapi import FastAPI, File, UploadFile, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

import uvicorn
import shutil

import os
import json
import numpy as np
import pandas as pd
from tqdm import tqdm
from pypdf import PdfReader

app = FastAPI()

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

processed_Dbapi_object = {}
lib_manager_path = "E:\intel\lib_manager"
material_path = "E:\intel\material files\\"
spd_path = "E:\intel\spd files\\"

@app.post("/")
async def root():
    return JSONResponse(content="res")

@app.post("/single-file")
def upload_spd(file: UploadFile = File(...)):
    print("okokvvvvvvvvvvvvvvv")
    with open(f'upload/{file.filename}', "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    data = pdf_process()
    print("data is:", data)

    return {"data": data}

def pdf_process():
    all_text = dict()
    manuals_path = "./upload"
    for manual_file in [f for f in os.listdir(manuals_path) if os.path.isfile(os.path.join(manuals_path, f))
                        if f.lower().endswith('.pdf')]:
        print(f'Processing file: {manual_file}')
        all_text.update(read_PDF(manuals_path, manual_file))

    rows_df = list()
    for k, v in all_text.items():
        rows_df.append({'file': k, 'input': v, 'output': ''})
    df_manuals = pd.DataFrame(rows_df)

    # Convert DataFrame to list of dictionaries
    data = df_manuals[['input', 'output']].to_dict(orient='records')

    # Specify the output file path
    # output_file = './upload'
    # with open(output_file, 'w') as file:
    #     json.dump(data, file)

    return df_manuals


def read_PDF(filepath: str, filename: str) -> dict:
    extracted_text = dict()
    reader = PdfReader(os.path.join(filepath, filename))
    for page_num, page in enumerate(reader.pages):
        extracted_text[f'File "{filename}", page {page_num + 1}'] = page.extract_text()
    return extracted_text

if __name__ == "__main__": uvicorn.run(app, host="0.0.0.0", port=8000)

