import cv2
import streamlit as st
import numpy as numpy
import sqlite3
import pandas as pd

st.set_page_config(page_title="OpenCV Filters on Video Stream", layout="wide")
conn = sqlite3.connect('car_data.db')
c = conn.cursor()

cap1 = cv2.VideoCapture(0)
cap2 = cv2.VideoCapture(1)

st.title("Video Capture with OpenCV")
col1, col2 = st.columns(2)

with col1:
    frame_placeholder1 = st.empty()
with col2:
    frame_placeholder2 = st.empty()

stop_btn = st.button("Stop")

c.execute("SELECT * FROM car_data")
data = c.fetchall()
df = pd.DataFrame(data, columns=['plate', 'in_time'])
st.sidebar.write(df)

def video_capture():
    while cap1.isOpened() and cap2.isOpened():
        ret1, frame1 = cap1.read()
        ret2, frame2 = cap2.read()
        if not (ret1 and ret2):
            st.write("Failed to capture frames.")
            break
        
        with col1:
            frame1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2RGB)
            frame_placeholder1.image(frame1, channels="RGB")
        with col2:
            frame2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2RGB)
            frame_placeholder2.image(frame2, channels="RGB")

def main():
    video_capture()
    
if __name__ == "__main__" :
    main()