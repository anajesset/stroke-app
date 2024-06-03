import streamlit as st
import mysql.connector
import hashlib


def create_connection():
    conn = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="",
        database="patient_database"
    )
    return conn


def register_user(conn, username, password):
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, hashed_password))
    conn.commit()
    cursor.close()


def verify_login(conn, username, password):
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, hashed_password))
    user = cursor.fetchone()[0]
    cursor.close()
    return user


# def is_registered():
#     conn = create_connection()
#     cursor = conn.cursor()
#     cursor.execute("SELECT COUNT(*) FROM users")
#     count = cursor.fetchone()[0]
#     cursor.close()
#     conn.close()
#     return count > 0


def register():
    register_page = st.empty()

    with register_page.container():
        st.title('Registrasi Pengguna')
        username = st.text_input('Username', key="1")
        password = st.text_input('Password', type='password', key="2")
        confirm_password = st.text_input('Confirm Password', type='password', key="3")
        register_button = st.button('Register')
        login_button = st.button('Sudah Punya Akun')

    if register_button:
        conn = create_connection()
        if len(username) < 1 and len(password) < 1:
            st.error('Harap isi terlebih dahulu username dan password.')
            return

        if password != confirm_password:
            st.error('Password dan konfirmasi password tidak cocok!')
            return

        register_user(conn, username, password)
        st.success('Registrasi berhasil! Silakan login.')
        st.info('Silakan login menggunakan akun yang telah Anda daftarkan.')
        register_page.empty()
        return True

    if login_button:
        register_page.empty()
        return True

    return False


def login():
    login_page = st.empty()

    with login_page.container():
        st.title('Login Admin')
        username = st.text_input('Username', key="4")
        password = st.text_input('Password', type='password', key="5")
        login_button = st.button('Login')

    if login_button:
        conn = create_connection()
        if len(username) > 0 and len(password) > 0:
            user = verify_login(conn, username, password)
        else:
            st.error('Harap isi terlebih dahulu username dan password.')
            return

        if user:
            st.success(f'Login berhasil, Selamat datang, {username}!')
            login_page.empty()
            return True
        else:
            st.error('Username atau password salah. Silakan coba lagi.')
            return

    return False
