import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

def eda():
    st.title('Exploratory Data Analysis (EDA)')
    st.write('Di halaman ini, Anda dapat menjelajahi data yang digunakan untuk melatih model.')
    
    # Load data yang digunakan untuk melatih model
    df = pd.read_csv('healthcare-dataset-stroke-data.csv')
    
    # Tampilkan informasi deskriptif data
    st.subheader('Deskripsi Data')
    st.write(df.describe())
    
    # Insight
    st.subheader('Insight:')
    st.write("""
         1. **Age**
            - Usia rata-rata adalah sekitar 52 tahun dengan standar deviasi sekitar 28 tahun.
            - Persebaran usia cukup luas, dengan rentang dari 0 hingga 100 tahun.
        2. **Average Glucose Level**
            - Tingkat glukosa darah rata-rata adalah sekitar 0.23 dengan standar deviasi sekitar 0.21.
            - Data cukup bervariasi, dengan nilai minimum 0 dan maksimum 1.
        3. **BMI**
            - BMI rata-rata adalah sekitar 0.21 dengan standar deviasi sekitar 0.09.
            - Sebagian besar individu memiliki BMI di kisaran 0.15 hingga 0.26.
        4. **Stroke**
            - Proporsi stroke dalam dataset sekitar 4.30%, dengan nilai minimum dan maksimum 0 dan 1, menunjukkan distribusi tidak seimbang antara kategori stroke dan non-stroke.
        """)

    # Visualisasi distribusi fitur numerik
    st.subheader('Distribusi Fitur Numerik')
    numeric_columns = df.select_dtypes(include=['float64', 'int64'])
    for col in numeric_columns.columns:
        fig, ax = plt.subplots(figsize=(8, 6))
        sns.histplot(df[col], kde=True, ax=ax)
        ax.set_title(f'Distribusi {col}')
        st.pyplot(fig)
        
    # Visualisasi hubungan antar fitur numerik
    st.subheader('Korelasi antar Fitur Numerik')
    correlation_matrix = numeric_columns.corr()
    fig, ax = plt.subplots(figsize=(10, 8))
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f", ax=ax)
    ax.set_title('Matriks Korelasi')
    st.pyplot(fig)

    #Scatter plot
    fig, ax= plt.subplots()
    ax.scatter(df['age'], df['avg_glucose_level'])
    ax.set_xlabel('Age')
    ax.set_ylabel('Average Glucose Level')
    st.pyplot(fig)
    
    fig, ax= plt.subplots()
    ax.hist(df['age'],bins=20, color='red', edgecolor='black')
    st.pyplot(fig)
    
    stroke_dist= df['stroke'].value_counts()
    fig= px.pie(values=stroke_dist.values, names=stroke_dist.index,
                title='Stroke Distribution')
    st.plotly_chart(fig)


if __name__ == '__main__':
    eda()
