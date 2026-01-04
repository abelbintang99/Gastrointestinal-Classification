from tensorflow.keras.models import load_model
from PIL import Image
import numpy as np

model = load_model("app/ml/fine_tuned_model_fold_2.keras")

IMAGE_SIZE = (299, 299)

def predict_image(image: Image.Image):
    img = image.resize(IMAGE_SIZE)
    img_array = np.array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)
    preds = model.predict(img_array)
    return preds