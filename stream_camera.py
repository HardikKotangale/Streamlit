import cv2
import streamlit as st
from streamlit_webrtc import webrtc_streamer, VideoHTMLAttributes
import numpy as np
import av
import time
st.title("OpenCV Filters on Video Stream")

filter1 = "none"
filter2 = "none"

def anpr_camera(frame: av.VideoFrame):
    img = frame.to_ndarray(format="bgr24")
    time.sleep(1)
    # ANPR Module
    return av.VideoFrame.from_ndarray(img, format="bgr24")

def parking_module(frame: av.VideoFrame):
    img = frame.to_ndarray(format="bgr24")
    time.sleep(1)
    
    return av.VideoFrame.from_ndarray(img, format="bgr24")

webrtc_streamer(
    key="streamer1",
    video_frame_callback=anpr_camera,
    sendback_audio=False
    )  

webrtc_streamer(
    key="streamer2",
    video_frame_callback=parking_module,
    sendback_audio=False
)
