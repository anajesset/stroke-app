import streamlit as st
import mysql.connector
import pandas as pd

# Function to create database connection
def create_connection():
    conn = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="",
        database="patient_database"
    )
    return conn

# Function to load data from database
def load_data_from_database():
    conn = create_connection()
    cursor = conn.cursor()

    # Execute SQL query to fetch data
    cursor.execute("SELECT * FROM patient_data")

    # Fetch all rows and store them in a DataFrame
    data = cursor.fetchall()
    columns = ['id','username', 'age', 'hypertension', 'glucose_levels', 'bmi', 'cardiac_history', 'smoke']
    df = pd.DataFrame(data, columns=columns)

    cursor.close()
    conn.close()

    return df

# Function to calculate C1 to C6 based on the criteria specified
def calculate_criteria(df):
    df['C1'] = df['age'].apply(lambda x: 1 if x <= 10 else (2 if x <= 20 else (3 if x <= 30 else (4 if x <= 40 else (5 if x <= 50 else (6 if x <= 60 else (7 if x <= 70 else (8 if x <= 80 else (9 if x <= 90 else 10)))))))))
    df['C2'] = df['hypertension'].map({'Yes': 3, 'No': 1})
    df['C3'] = df['glucose_levels'].apply(lambda x: 1 if x <= 90 else (2 if x <= 110 else (3 if x <= 130 else (4 if x <= 150 else (5 if x <= 170 else (6 if x <= 190 else (7 if x <= 210 else (8 if x <= 230 else (9 if x <= 250 else 10)))))))))
    df['C4'] = df['bmi'].apply(lambda x: 1 if x <= 5 else (2 if x <= 10 else (3 if x <= 20 else (4 if x <= 25 else (5 if x <= 30 else (6 if x <= 35 else (7 if x <= 40 else (8 if x <= 45 else (9 if x <= 50 else 10)))))))))
    df['C5'] = df['cardiac_history'].map({'Have': 4, 'Haven\'t': 2})
    df['C6'] = df['smoke'].map({'Never Smoked': 1, 'Formerly Smoked': 3, 'Smokes': 4})

    return df

# Function to calculate WP score
def calculate_wp(data):
    # Define weights for each criteria
    weights = {
        'C1': 0.23,
        'C2': 0.18,
        'C3': 0.14,
        'C4': 0.14,
        'C5': 0.18,
        'C6': 0.14
    }

    # Function to calculate S for each row
    def calculate_s(row):
        s = 1
        s *= row['C1'] ** weights['C1']
        s *= row['C2'] ** weights['C2']
        s *= row['C3'] ** weights['C3']
        s *= row['C4'] ** weights['C4']
        s *= row['C5'] ** weights['C5']
        s *= row['C6'] ** weights['C6']
        return s

    # Calculate S for each row
    data['Vektor S'] = data.apply(calculate_s, axis=1)

    # Calculate total S
    total_s = data['Vektor S'].sum()

    # Calculate WP score
    data['WP Score'] = data['Vektor S'] / total_s

    # Sort data by WP score in descending order
    sorted_data = data.sort_values(by='WP Score', ascending=False).reset_index(drop=True)
    sorted_data['Ranking'] = sorted_data.index + 1
    
    return sorted_data

# Function to show priority ranking
def show_priority():
    st.title('Stroke Doctor Referral Patient Priority Ranking')

    # Load data from database
    data = load_data_from_database()

    # Calculate C1 to C6 based on the criteria specified
    data_with_criteria = calculate_criteria(data)

    # Calculate WP score
    sorted_df = calculate_wp(data_with_criteria)

    # Display priority ranking
    st.write("Patient Priority Ranking for Stroke Doctor Referral:")
    st.write(sorted_df)

if __name__ == "__main__":
    show_priority()
