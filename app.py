import streamlit as st
from PIL import Image, ImageOps
import numpy as np
import pandas as pd
from src.ml_logic.model import load_Model_G
import os
import cv2
from tensorflow.keras.applications.imagenet_utils import decode_predictions
import tensorflow as tf
import matplotlib.pyplot as plt
from tensorflow.keras.applications.efficientnet import preprocess_input
import pickle
from src.ml_logic.registry import load_model

SIDEBAR = st.sidebar.image("/home/naimabechari/code/naimabe/melanoma-project/data/lewagonimage.png", use_column_width=True)
st.sidebar.write("Batch #1061 - Data Science")
st.sidebar.write("## Who are we?")
st.sidebar.write("George, Dejan and Naïma")
st.sidebar.write("The Goal of our project is to predict whether a skin lesion is benign or malignant.")


st.markdown("""# PREDICTION OF MELANOMAS
## Is my Skin lesion a benign or malignant lesion?""")

uploaded_image = st.file_uploader(label = "You can drop your skin image here:", type=["jpg", "png"])
st.set_option('deprecation.showfileUploaderEncoding', False)


#model = load_Model_G()

if uploaded_image is not None:
    image = Image.open(uploaded_image)
    st.success("You did it !")

    #st.write(f"Original size : {image.size}") # 5464x3640
    st.image(image, use_column_width=True, caption='Your Picture')
    st.write("")
    st.write("Classifying...")
    image_resized = image.resize((64,64))
    image_resized = preprocess_input(image)
    image_resized = np.asarray(image_resized)
    loaded_model = load_model()

    #st.write(f"Resize: {image_resized.size}")
    #image_resized.save('resized_image.jpeg')
    #prediction = loaded_model.predict(image_resized)

    #image_class = str(prediction[0][0][1])
    #score=np.round(prediction[0][0][2])
    #st.write("The image is classified as",image_class)
    #st.write("The similarity score is approximately",score)
    #print("The image is classified as ",image_class, "with a similarity score of",score)


    #label = teachable_machine_classification(image, 'brain_tumor_classification.h5')
    #if label == 0:
    #    st.write("The MRI scan has a brain tumor")
    #else:
    #    st.write("The MRI scan is healthy")

 # print out the top 3 prediction labels with scores
    #for i in labels:
    #    st.write("Prediction (index, name)", i[0], ",   Score: ", i[1])