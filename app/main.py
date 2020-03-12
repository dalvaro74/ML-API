# Data Handling
from fastapi.logger import logger as fastapi_logger
from logging.handlers import RotatingFileHandler
import logging
import pickle
import numpy as np

from pydantic import BaseModel

# Server
import uvicorn
from fastapi import FastAPI

# Modeling
import lightgbm

app = FastAPI()

# Initialize logging
#Para Fastapi la gestion y tratamiento de logs es distinto del standar de python

formatter = logging.Formatter("[%(asctime)s.%(msecs)03d] %(levelname)s [%(thread)d] - %(message)s", "%Y-%m-%d %H:%M:%S")
handler = RotatingFileHandler('abc.log', backupCount=0)
logging.getLogger().setLevel(logging.NOTSET)
fastapi_logger.addHandler(handler)
handler.setFormatter(formatter)
fastapi_logger.info('****************** Starting Server *****************')

# Initialize files
clf = pickle.load(open('data/model.pickle', 'rb'))
enc = pickle.load(open('data/encoder.pickle', 'rb'))
features = pickle.load(open('data/features.pickle', 'rb'))


class Data(BaseModel):
    satisfaction_level: float
    last_evaluation: float
    number_project: float
    average_montly_hours: float
    time_spend_company: float
    Work_accident: float
    promotion_last_5years: float
    sales: str
    salary: str
        
        
@app.post("/predict")
def predict(data: Data):
    try:
        # Extract data in correct order
        data_dict = data.dict()
        fastapi_logger.debug(data_dict)
        to_predict = [data_dict[feature] for feature in features]
        fastapi_logger.debug(to_predict)

        # Apply one-hot encoding
        encoded_features = list(enc.transform(np.array(to_predict[-2:]).reshape(1, -1))[0])
        fastapi_logger.debug(encoded_features)
        to_predict = np.array(to_predict[:-2] + encoded_features)
        fastapi_logger.debug(to_predict)

        # Create and return prediction
        prediction = clf.predict(to_predict.reshape(1, -1))
        return {"prediction": int(prediction[0])}
    
    except:
        fastapi_logger.error("Something went wrong!")
        return {"prediction": "error"}
