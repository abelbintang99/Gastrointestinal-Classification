import numpy as np
from PIL import Image
from .model import model

def predict_image(image: Image.Image):
    if model is None:
        return "Model tidak ditemukan di server"

    img = image.resize((299, 299)) 
    img_array = np.array(img) / 255.0  
    img_array = np.expand_dims(img_array, axis=0) 

    
    predictions = model.predict(img_array)
    
   
    labels = ['Esofagitis', 'Cecum Normal', 'Polip', 'Kolitis']
    
    idx = np.argmax(predictions[0])
    score = np.max(predictions[0]) * 100
    
    return f"{labels[idx]} ({score:.1f}%)"