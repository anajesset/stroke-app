import streamlit as st
import pandas as pd
from joblib import load

dt_model = load('decision_tree_model.joblib')
rf_model = load('random_forest_model.joblib')
svm_model = load('svm_model.joblib')

preprocessing_pipeline = load('preprocessing_pipeline.joblib')

def predict_data():
    st.title('Stroke Prediction')
    st.write('Please enter the following information to predict whether you are at risk of having a stroke or not.')
    
    gender = st.selectbox('Gender', ['Male', 'Female'])
    age = st.number_input('Age', min_value=0, max_value=100)
    hypertension = st.selectbox('Do you suffer from hypertension?', ['Yes', 'No'])
    if hypertension == 'Yes':
        hypertension = 1
    else:
        hypertension = 0
    avg_glucose_level = st.number_input('Average Glucose Levels (mg/dL)', min_value=0.0)
    bmi = st.number_input('Body Mass Index (kg/m²)', min_value=0.0)
    ever_married = st.selectbox('Ever Married', ['No', 'Yes'])
    work_type = st.selectbox('Work Type', ['Self-employed', 'Private', 'Govt_job'])
    Residence_type = st.selectbox('Residence Type', ['Rural', 'Urban'])
    smoking_status = st.selectbox('Smoking Status', ['Unknown', 'never smoked', 'formerly smoked', 'smokes'])

    input_data = pd.DataFrame({
        'gender': [gender],
        'age': [age],
        'hypertension': [hypertension],
        'avg_glucose_level': [avg_glucose_level],
        'bmi': [bmi],
        'ever_married':[ever_married],
        'work_type':[work_type],
        'Residence_type':[Residence_type],
        'smoking_status':[smoking_status]
    })

    input_data_preprocessed = preprocessing_pipeline.transform(input_data)
    
    if st.button('Predict'):
        prediction = dt_model.predict(input_data_preprocessed)
        st.write(prediction)
        if prediction[0] == 1:
            st.error('High risk of stroke!')
        else:
            st.success('Low risk of stroke!')
    
if __name__ == '__main__':
    predict_data()
