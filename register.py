import streamlit as st
from streamlit_webrtc import webrtc_streamer, VideoProcessorBase
import cv2
import requests
import sqlite3
from datetime import datetime

# Specify the Plate Recognizer API endpoint and your license key
api_url = "https://api.platerecognizer.com/v1/plate-reader/"
api_key = "357ebf90c0cc6e6ce54510456d9efcb32a770d31"

# Create a connection to SQLite database
conn = sqlite3.connect('car_data.db')
c = conn.cursor()

# Create table to store car information
c.execute('''CREATE TABLE IF NOT EXISTS car_data
             (plate TEXT, in_time TEXT, out_time TEXT)''')

# Function to insert car data into the database
def insert_car_data(plate, in_time, out_time):
    c.execute("INSERT INTO car_data (plate, in_time, out_time) VALUES (?, ?, ?)", (plate, in_time, out_time))
    conn.commit()

# Function to fetch all car data from the database
def fetch_car_data():
    c.execute("SELECT * FROM car_data")
    return c.fetchall()

class VideoProcessor(VideoProcessorBase):
    def __init__(self) -> None:
        super().__init__()

    def recv(self, frame):
        # Process the frame
        result = process_frame(frame.to_ndarray())
        st.image(frame)
        # Extract license plate information from the response
        for plate_info in result["results"]:
            plate = plate_info['plate']
            current_datetime = datetime.now()
            formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")

            # Check if the plate is already in the database
            c.execute("SELECT * FROM car_data WHERE plate=?", (plate,))
            data = c.fetchone()
            
            if data:
                # Plate already exists in the database, update the out time
                update_time = formatted_datetime
                c.execute("UPDATE car_data SET out_time=? WHERE plate=?", (update_time, plate))
                conn.commit()
            else:
                # Insert the new plate data into the database
                insert_car_data(plate, formatted_datetime, None)

rtc_configuration = {"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]}

media_stream_constraints = {"video": True, "audio": False}

def process_frame(frame):
    # Send the frame to the Plate Recognizer API
    _, img_encoded = cv2.imencode('.jpg', frame)
    files = {"upload": ("frame.jpg", img_encoded.tobytes(), "image/jpeg")}
    headers = {"Authorization": f"Token {api_key}"}
    response = requests.post(api_url, files=files, headers=headers)
    return response.json()

def main():
    st.title("Automatic Number Plate Recognition (ANPR) System")

    webrtc_ctx = webrtc_streamer(
        key="example",
        video_processor_factory=VideoProcessor,
        rtc_configuration=rtc_configuration,
        media_stream_constraints=media_stream_constraints,
    )

    # Display data from the database in table format
    car_data = fetch_car_data()
    st.write("Car Data in Database:")
    st.table(car_data)

if __name__ == "__main__":
    main()
