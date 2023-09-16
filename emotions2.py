import streamlit as st
import cv2
import numpy as np
from deepface import DeepFace
from docx import Document
from docx.shared import Inches
import base64
import os

st.title("DeepFace Analysis")
image_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

last_analyzed_image = None
last_dominant_emotion = None
last_analysis = None

def analyze_image(image_file):
    global last_analyzed_image, last_dominant_emotion, last_analysis
    image_data = np.frombuffer(image_file.read(), np.uint8)
    image = cv2.imdecode(image_data, -1)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    predictions = DeepFace.analyze(image_rgb, actions=['emotion', 'age', 'gender', 'race'])
    if isinstance(predictions, dict):
        last_analysis = predictions
        last_dominant_emotion = predictions.get('dominant_emotion', 'N/A')
        last_analyzed_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        st.write("Analysis:", last_analysis)
    else:
        st.write("Could not determine analysis.")

if image_file is not None:
    st.image(image_file, caption="Uploaded Image.", use_column_width=True)
    st.write("Classifying...")
    analyze_image(image_file)

def generate_word_file():
    global last_analyzed_image, last_analysis
    doc = Document()
    doc.add_heading('DeepFace Analysis Report', 0)
    if last_analyzed_image is not None and last_analysis is not None:
        image_path = 'temp_image.jpg'
        cv2.imwrite(image_path, cv2.cvtColor(last_analyzed_image, cv2.COLOR_RGB2BGR))
        doc.add_picture(image_path, width=Inches(2.0))
        os.remove(image_path)
        for key, value in last_analysis.items():
            if isinstance(value, dict):
                for subkey, subvalue in value.items():
                    doc.add_paragraph(f'{key} - {subkey}: {subvalue}')
            else:
                doc.add_paragraph(f'{key}: {value}')
    doc.save('report.docx')
    with open('report.docx', 'rb') as f:
        bytes = f.read()
        b64 = base64.b64encode(bytes).decode()
        href = f'<a href="data:file/docx;base64,{b64}" download="report.docx">Download Report</a>'
        st.markdown(href, unsafe_allow_html=True)

if st.button("Generate Report"):
    generate_word_file()
