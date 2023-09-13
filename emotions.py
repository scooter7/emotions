import streamlit as st
import cv2
import numpy as np
from deepface import DeepFace
from docx import Document

st.title("Emotion Analysis using DeepFace")

image_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

def analyze_image(image_file):
    image = cv2.imdecode(np.frombuffer(image_file.read(), np.uint8), -1)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    predictions = DeepFace.analyze(image, actions=['emotion'])
    st.write("Emotion:", predictions['dominant_emotion'])

if image_file is not None:
    st.image(image_file, caption="Uploaded Image.", use_column_width=True)
    st.write("")
    st.write("Classifying...")
    analyze_image(image_file)

video_file = st.file_uploader("Upload a video", type=["mp4", "avi", "mkv"])

def analyze_video(video_file):
    video_bytes = video_file.read()
    video_path = "uploaded_video.mp4"
    with open(video_path, "wb") as f:
        f.write(video_bytes)

    cap = cv2.VideoCapture(video_path)
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        predictions = DeepFace.analyze(frame, actions=['emotion'])
        st.write("Emotion:", predictions['dominant_emotion'])
    cap.release()

if video_file is not None:
    st.video(video_file)
    st.write("")
    st.write("Classifying...")
    analyze_video(video_file)

def generate_word_file():
    doc = Document()
    doc.add_heading('Emotion Analysis Report', 0)
    doc.save('report.docx')
    
    with open('report.docx', 'rb') as f:
        bytes = f.read()
        b64 = base64.b64encode(bytes).decode()
        href = f'<a href="data:file/docx;base64,{b64}" download="report.docx">Download Report</a>'
        st.markdown(href, unsafe_allow_html=True)

if st.button("Generate Report"):
    generate_word_file()
