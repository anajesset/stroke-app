import streamlit as st
import mysql.connector

def create_connection():
    conn = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="",
        database="patient_database"
    )
    return conn

def save_application(conn, username, age, hypertension, glucose_levels, bmi, cardiac_history, smoke):
    cursor = conn.cursor()
    cursor.execute("INSERT INTO patient_data (username, age, hypertension, glucose_levels, bmi, cardiac_history, smoke) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                   (username, age, hypertension, glucose_levels, bmi, cardiac_history, smoke))
    conn.commit()
    cursor.close()



def validate_data(username, age, hypertension, glucose_levels, bmi, cardiac_history, smoke):
    if not username or not age or not hypertension or not glucose_levels or not bmi or not cardiac_history or not smoke:
        return False
    try:
        age = int(age)
        hypertension = float(hypertension)
        glucose_levels = float(glucose_levels)
        bmi = float(bmi)
    except ValueError:
        return False
    return True

def registration():
    st.title('Patient Prioritization Registration for Stroke Doctor Referral')

    with st.form(key='registration_form'):
        username = st.text_input('Name')
        age = st.number_input('Age (Years)', min_value=0, step=1, format='%d')
        hypertension = st.radio('Hypertension', ['Yes', 'No'])
        glucose_levels = st.number_input('Average Blood Glucose (mg/dL)', min_value=0.0, step=0.1, format='%f')
        bmi = st.number_input('Body Mass Index (kg/m²)', min_value=0.0, step=0.1, format='%f')
        cardiac_history = st.radio('Cardiac History', ['Have', 'Haven\'t'])
        smoke = st.radio('Smoking Status', ['Never Smoked', 'Formerly Smoked', 'Smokes'])

        submitted = st.form_submit_button('Register')

        if submitted:
            if validate_data(username, age, hypertension, glucose_levels, bmi, cardiac_history, smoke):
                conn = create_connection()
                save_application(conn, username, age, hypertension, glucose_levels, bmi, cardiac_history, smoke)
                st.success('Patient data has been successfully saved!')
                conn.close()
            else:
                st.error('Please fill in all fields correctly!')

if __name__ == "__main__":
    registration()
