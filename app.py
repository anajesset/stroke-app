import streamlit as st
from user import register, login, create_connection
import predict, eda, criteria, registration, priority, consultation

st.set_page_config(
    page_title="Stroke Prediction App",
    page_icon=":brain:",
    layout="wide",
    initial_sidebar_state="expanded",
)

def home():
    if 'register_in' not in st.session_state:
        st.session_state.register_in = False

    if not st.session_state.register_in:
        register_successful = register()
        if register_successful:
            st.session_state.register_in = True
        else:
            st.warning('Silakan login apabila sudah memiliki akun')
            return

    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False

    if not st.session_state.logged_in:
        login_successful = login()
        if login_successful:
            st.session_state.logged_in = True
        else:
            st.warning('Silakan login terlebih dahulu!')
            return

    st.sidebar.title('Menu')
    selection = st.sidebar.selectbox("Go to", ["Home", "Predict", "Criteria", "Registration", "Priority", "Consultation", "EDA"])

    if selection == "Home":
        st.title('Welcome to Stroke Prediction App')
        st.write('This app helps you to predict whether you are at risk of having a stroke or not')
        st.image('https://d1vbn70lmn1nqe.cloudfront.net/prod/wp-content/uploads/2022/07/06032532/Stroke-pada-Lansia-Waspada-Faktor-Risikonya.jpg', width=600)
        st.write('Stroke is one of the most dangerous diseases and causes many deaths. Stroke is a disease that can result in loss of ability and loss of life. Stroke is a disease that can result in loss of ability and loss of life. Stroke is a disease that can result in loss of ability and loss of life. This application will help you to find out the potential for stroke in yourself and find out the risk factors associated with the possibility of someone having a stroke.')
    elif selection == "Predict":
        predict.predict_data()
    elif selection == 'Criteria':
        criteria.criteria()
    elif selection == "Registration":
        registration.registration()
    elif selection == "Priority":
        priority.show_priority()
    elif selection == "Consultation":
        consultation.consultation()
    elif selection == "EDA":
        eda.eda()

if __name__ == '__main__':
    home()
