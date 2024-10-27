# app/review.py

import logging
from fastapi import HTTPException
from pydantic import BaseModel

data = {
    "reviews": [],
    "positive": 0,
    "negative": 0
}

class TextInput(BaseModel):
    text: str

async def get_data():
    """Endpoint to retrieve the current data (positive, negative counts, and reviews)"""
    return data

async def submit_text(input: TextInput):
    """Endpoint to process submitted text, update sentiment counts, and add the review to the list"""
    text = input.text
    logging.info(f'Text received: {text}')

    # Process the text
    preprocessed_text = preprocessing(text)  # Make sure to import this function from your helper module
    vectorized_text = vectorizer(preprocessed_text)  # Import accordingly
    prediction = get_prediction(vectorized_text)  # Import accordingly
    logging.info(f'Prediction: {prediction}')

    # Update counts based on prediction
    if prediction == 'negative':
        data["negative"] += 1
    else:
        data["positive"] += 1

    data["reviews"].insert(0, text)
    return {"prediction": prediction, "message": "Text processed successfully"}
