import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime

# Create a connection to the SQLite database
conn = sqlite3.connect('car_details.db')
c = conn.cursor()

# Create a table to store car details if it doesn't exist
c.execute('''CREATE TABLE IF NOT EXISTS car_details
             (id INTEGER PRIMARY KEY AUTOINCREMENT, 
             license_plate TEXT, 
             user_name TEXT,
             mobile_number TEXT,
             car_model TEXT,
             registration_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
             parking_status TEXT DEFAULT 'IN')''')
conn.commit()

# Streamlit UI
st.title('Register User')

# Form inputs
license_plate = st.text_input('Enter License Plate Number')
user_name = st.text_input('Enter User Name')
mobile_number = st.text_input('Enter Mobile Number')
car_model = st.text_input('Enter Car Model')

# Save button
if st.button('Save'):
    # Check if the car is already registered
    c.execute("SELECT * FROM car_details WHERE license_plate=?", (license_plate,))
    existing_entry = c.fetchone()
    
    if existing_entry:
        # If the car is already registered and is marked as OUT, update the entry to IN
        if existing_entry[6] == 'OUT':
            c.execute("UPDATE car_details SET parking_status='IN', registration_time=? WHERE license_plate=?", (datetime.now(), license_plate,))
            conn.commit()
            st.success('Car has been marked as IN again.')
        else :
            st.warning('Car is already registered')
    else:
        # If the car is being registered for the first time, mark parking status as "IN"
        c.execute("INSERT INTO car_details (license_plate, user_name, mobile_number, car_model) VALUES (?, ?, ?, ?)",
                  (license_plate, user_name, mobile_number, car_model))
        conn.commit()
        st.success('Car details saved successfully with IN status.')

# View Data option
if st.button('View Data'):
    # Fetch data from the database
    c.execute("SELECT * FROM car_details")
    data = c.fetchall()
    if data:
        # Display data in a table format
        df = pd.DataFrame(data, columns=['ID', 'License Plate', 'User Name', 'Mobile Number', 'Car Model', 'Registration Time', 'Parking Status'])
        st.write(df)
    else:
        st.warning('No data found in the database.')

# Close connection
conn.close()
