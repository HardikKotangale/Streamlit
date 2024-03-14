import json
import streamlit as st
import cv2
import numpy as np
import requests
import sqlite3
from streamlit_option_menu import option_menu
import pandas as pd

api_url = "https://api.platerecognizer.com/v1/plate-reader/"
api_key = "357ebf90c0cc6e6ce54510456d9efcb32a770d31"

user_color = '#000000'
title_webapp = "ANPR Car Registration"

html_temp = f"""
            <div style="background-color:{user_color};padding:12px">
            <h1 style="color:white;text-align:center;">{title_webapp}</h1>
            </div>
            """

st.markdown(html_temp, unsafe_allow_html=True)
# Create a connection to SQLite database
conn = sqlite3.connect('car_data.db')
c = conn.cursor()
# Create table to store car information
c.execute('''CREATE TABLE IF NOT EXISTS car_data
             (plate TEXT, in_time TEXT)''')
# Create a table to store car details if it doesn't exist
c.execute('''CREATE TABLE IF NOT EXISTS user_details
             (id INTEGER PRIMARY KEY AUTOINCREMENT, 
             license_plate TEXT, 
             user_name TEXT,
             mobile_number TEXT,
             car_model TEXT,
             registration_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
             parking_status TEXT DEFAULT 'IN')''')
conn.commit()

def insert_car_data(plate, in_time):
    c.execute("INSERT INTO car_data (plate, in_time) VALUES (?, ?)", (plate, in_time))
    conn.commit()

def fetch_car_data():
    c.execute("SELECT * FROM car_data")
    return c.fetchall()

def main():

    selected_menu = option_menu(None, ['Visitor Validation', 'View Visitor History', 'Register user Database'], icons=['camera', "clock-history", 'person-plus'], menu_icon="cast", default_index=0, orientation="horizontal")

    if selected_menu == 'Visitor Validation':
        ## Reading Camera Image
        frame = st.camera_input("Take a picture")
        if frame is not None:
            files = {"upload": frame}
            headers = {"Authorization": f"Token {api_key}"}
            response = requests.post(api_url, files=files, headers=headers)
            response_data = json.loads(response.text)
            car_number = response_data['results'][0]['plate']
            timestamp = response_data['timestamp']
            st.write(car_number)
            st.write(timestamp)
            insert_car_data(car_number, timestamp)
            st.success('Car Registered Sucessfully')

    if selected_menu == 'View Visitor History':
        st.header("DataBase Entry")
        car_data = fetch_car_data()
        st.write("Car Data in Database")
        df = pd.DataFrame(car_data, columns=['plate', 'in_time'])
        st.write(df)

    if selected_menu == 'Register user Database':

        c.execute("SELECT * FROM user_details")
        data = c.fetchall()
        if data:
            # Display data in a table format
            df1 = pd.DataFrame(data, columns=['ID', 'License Plate', 'User Name', 'Mobile Number', 'Car Model', 'Registration Time', 'Parking Status'])
            st.write(df1)
        else:
            st.warning('No data found in the database.')

if __name__ == "__main__":
    main()