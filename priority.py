import streamlit as st
import mysql.connector
import pandas as pd

def create_connection():
    conn = mysql.connector.connect(
        host="sql.freedb.tech",
        user="freedb_anajesset",
        password="D9@WjYGE9?6&b&n",
        database="freedb_scpk_database"
    )
    return conn

def load_data_from_database():
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM patient_data")

    data = cursor.fetchall()
    columns = ['id','username', 'age', 'hypertension', 'glucose_levels', 'bmi', 'cardiac_history', 'smoke']
    df = pd.DataFrame(data, columns=columns)

    cursor.close()
    conn.close()

    return df

def calculate_criteria(df):
    df['C1'] = df['age'].apply(lambda x: 1 if x <= 10 else (2 if x <= 20 else (3 if x <= 30 else (4 if x <= 40 else (5 if x <= 50 else (6 if x <= 60 else (7 if x <= 70 else (8 if x <= 80 else (9 if x <= 90 else 10)))))))))
    df['C2'] = df['hypertension'].map({'Yes': 3, 'No': 1})
    df['C3'] = df['glucose_levels'].apply(lambda x: 1 if x <= 90 else (2 if x <= 110 else (3 if x <= 130 else (4 if x <= 150 else (5 if x <= 170 else (6 if x <= 190 else (7 if x <= 210 else (8 if x <= 230 else (9 if x <= 250 else 10)))))))))
    df['C4'] = df['bmi'].apply(lambda x: 1 if x <= 5 else (2 if x <= 10 else (3 if x <= 20 else (4 if x <= 25 else (5 if x <= 30 else (6 if x <= 35 else (7 if x <= 40 else (8 if x <= 45 else (9 if x <= 50 else 10)))))))))
    df['C5'] = df['cardiac_history'].map({'Have': 4, 'Haven\'t': 2})
    df['C6'] = df['smoke'].map({'Never Smoked': 1, 'Formerly Smoked': 3, 'Smokes': 4})

    return df

def calculate_wp(data):
    weights = {
        'C1': 0.23,
        'C2': 0.18,
        'C3': 0.14,
        'C4': 0.14,
        'C5': 0.18,
        'C6': 0.14
    }

    def calculate_s(row):
        s = 1
        s *= row['C1'] ** weights['C1']
        s *= row['C2'] ** weights['C2']
        s *= row['C3'] ** weights['C3']
        s *= row['C4'] ** weights['C4']
        s *= row['C5'] ** weights['C5']
        s *= row['C6'] ** weights['C6']
        return s

    data['Vektor S'] = data.apply(calculate_s, axis=1)

    total_s = data['Vektor S'].sum()

    data['WP Score'] = data['Vektor S'] / total_s

    sorted_data = data.sort_values(by='WP Score', ascending=False).reset_index(drop=True)
    sorted_data['Ranking'] = sorted_data.index + 1
    
    return sorted_data

def show_priority():
    st.title('Stroke Doctor Referral Patient Priority Ranking')

    data = load_data_from_database()
    data_with_criteria = calculate_criteria(data)

    sorted_df = calculate_wp(data_with_criteria)

    st.write("Patient Priority Ranking for Stroke Doctor Referral:")
    st.write(sorted_df)

if __name__ == "__main__":
    show_priority()
