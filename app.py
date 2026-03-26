import sys
import os
import certifi
import pymongo
import pandas as pd
import json

from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, File, UploadFile, Request
from uvicorn import run as app_run
from fastapi.responses import Response
from starlette.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.pipeline.training_pipeline import TrainingPipeline
from networksecurity.utils.main_utils.utils import read_yaml_file, load_object
from networksecurity.utils.ml_utils.model.estimator import NetworkModel
from networksecurity.constant.training_pipeline import DATA_INGESTION_COLLECTION_NAME, DATA_INGESTION_DATABASE_NAME

# Setup MongoDB and SSL
load_dotenv()
ca = certifi.where()
mongo_db_url = os.getenv("MONGODB_URL_KEY")
client = pymongo.MongoClient(mongo_db_url, tlsCAFile=ca)

database = client[DATA_INGESTION_DATABASE_NAME]
collection = database[DATA_INGESTION_COLLECTION_NAME]

app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

templates = Jinja2Templates(directory="./templates")

@app.get("/", tags=["authentication"])
async def index():
    return RedirectResponse(url="/docs")

@app.get("/train")
async def train_route():
    try:
        train_pipeline = TrainingPipeline()
        train_pipeline.run_pipeline()
        return Response("Training is successful")
    except Exception as e:
        raise NetworkSecurityException(e, sys)

@app.post("/predict")
async def predict_route(request: Request, file: UploadFile = File(...)):
    try:
        # Read the uploaded CSV
        df = pd.read_csv(file.file)
        
        # Load Preprocessor and Model (Ensure these files are in your Docker image)
        preprocessor = load_object("final_model/preprocessor.pkl")
        final_model = load_object("final_model/model.pkl")
        
        network_model = NetworkModel(preprocessor=preprocessor, model=final_model)
        
        # Perform Prediction
        y_pred = network_model.predict(df)
        df['predicted_column'] = y_pred
        
        # Ensure output directory exists before saving
        os.makedirs("prediction_output", exist_ok=True)
        df.to_csv("prediction_output/output.csv", index=False)
        
        # Convert dataframe to JSON to return to the user in Swagger UI
        # This avoids the "unhashable dict" Jinja2 error
        json_compatible_results = json.loads(df.to_json(orient="records"))
        return {"status": "success", "data": json_compatible_results}

    except Exception as e:
        # Convert exception to string to prevent NetworkSecurityException from failing on dict types
        logging.error(f"Prediction Error: {str(e)}")
        raise NetworkSecurityException(str(e), sys)

if __name__ == "__main__":
    app_run(app, host="0.0.0.0", port=8080)