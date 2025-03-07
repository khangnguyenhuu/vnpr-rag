# author khangnh
import os
import time
import logging
import traceback
from http import HTTPStatus
from chainlit.utils import mount_chainlit
from fastapi.responses import JSONResponse
from werkzeug.utils import secure_filename
from multiprocessing.managers import BaseManager
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, File, UploadFile, status

from src.http_message.message import HTTP_STATUS
from src.constants import (cfg)
from src.api.ingest_data_service import IngestionService
from src.constants import logger

app = FastAPI()
origins=['*']
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Hello World"}

# init tmp_documents dir to store uploaded file
os.makedirs(cfg.GENERAL_CONFIG.DATABASE_DOCUMENT_STORE_FOLDER, exist_ok=True)

# init ingestion service
ingestion_service = IngestionService()
@app.post("/uploadFile/")
async def upload_file(uploaded_file: UploadFile = File(...)):
    
    logger.ingest_logger.info(f'----Start request----')
    if len(uploaded_file.filename) == 0:
        logger.ingest_logger.info(f'Empty uploaded file')
        logger.ingest_logger.debug(f'status_code: { HTTP_STATUS[400].status_code}')
        return HTTP_STATUS[400]
     
    filepath = None
    try:
        # check 411 status
        filename = secure_filename(uploaded_file.filename)
        logger.ingest_logger.info(f'Uploaded file {uploaded_file.filename}')
        if not filename.endswith(".txt"):
            logger.ingest_logger.info(f'File type not supported {filename}')
            logger.ingest_logger.debug(f'status_code: {HTTP_STATUS[415].status_code})')
            return HTTP_STATUS[415]
        
        filepath = os.path.join(cfg.GENERAL_CONFIG.DATABASE_DOCUMENT_STORE_FOLDER, os.path.basename(filename))
        with open(filepath, "wb") as f:
            f.write(await uploaded_file.read())
        logger.ingest_logger.info(f'Save uploaded file to {filepath}')

        try:
            start = time.time()
            # insert all files of tmp_documents to vector db
            ingestion_service.insert(cfg.GENERAL_CONFIG.DATABASE_DOCUMENT_STORE_FOLDER)
            # cleanup temp file
            if filepath is not None and os.path.exists(filepath):
                os.remove(filepath)
            end = time.time()
            logger.ingest_logger.info(f'Insert {filename} to vector db sucessfully')
            logger.ingest_logger.debug(f'status_code: {HTTP_STATUS[200].status_code}')
            logger.ingest_logger.info(f'processing time: {end-start}')
            logger.ingest_logger.info(f'----End request----')
            return HTTP_STATUS[200]
        
        except Exception as e:
            logger.ingest_logger.debug(f'status_code: {HTTP_STATUS[412].status_code}')
            logger.ingest_logger.error(traceback.format_exc())
            logger.ingest_logger.info(f'----End request----')
            return HTTP_STATUS[412]
        
    except Exception as e:
        # cleanup temp file
        if filepath is not None and os.path.exists(filepath):
            os.remove(filepath)
        logger.ingest_logger.debug('status_code: 500')
        logger.ingest_logger.error(traceback.format_exc())
        logger.ingest_logger.info(f'----End request----')
        return HTTP_STATUS[500]
    
#init chatbot service
mount_chainlit(app=app, target="chain.py", path="/chainlit")
