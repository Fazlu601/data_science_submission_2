import streamlit as st
import pandas as pd
import joblib
import numpy as np
import os

# --- Konfigurasi Halaman Streamlit ---
st.set_page_config(page_title="Student Dropout Prediction", layout="wide")

# --- Path File ---
model_path = 'models/best_dropout_model.pkl'
scaler_path = 'models/scaler.pkl'
columns_path = 'models/columns.pkl'
scaled_columns_path = 'models/scaled_columns_names.pkl'

# --- Memuat Model dan Konfigurasi ---
try:
    model = joblib.load(model_path)
    scaler = joblib.load(scaler_path)
    trained_columns = joblib.load(columns_path)
    scaled_columns_names = joblib.load(scaled_columns_path)
    st.success("Model, scaler, dan konfigurasi berhasil dimuat!")
except FileNotFoundError as e:
    st.error(f"File tidak ditemukan: {e.filename}")
    st.stop()
except Exception as e:
    st.error(f"Error saat memuat file: {e}")
    st.stop()

# --- Mapping Kategorikal ---
marital_status_map = {
    'Single': 1, 'Married': 2, 'Widower': 3,
    'Divorced': 4, 'Facto union': 5, 'Legally separated': 6
}
daytime_map = {'Daytime': 1, 'Evening': 0}
gender_map = {'Male': 1, 'Female': 0}
bool_map = {'Yes': 1, 'No': 0}

# Contoh mapping, sesuaikan dengan dataset asli Anda
course_map = {
    'Informatics Engineering': 9119,
    'Management': 9147,
    'Tourism': 9254,
    'Nursing': 9500
}
prev_qualification_map = {
    'Secondary education': 1,
    'Higher ed. - bachelor': 2,
    'Higher ed. - master': 4
}
nationality_map = {'Portuguese': 1, 'Other': 0}
mothers_qual_map = {'Secondary Education': 1, 'Higher Education': 2, 'Other': 0}
fathers_qual_map = {'Secondary Education': 1, 'Higher Education': 2, 'Other': 0}
mothers_occupation_map = {'Student': 1, 'Teacher': 2, 'Other': 0}
fathers_occupation_map = {'Student': 1, 'Teacher': 2, 'Other': 0}
application_mode_map = {
    '1st phase - general contingent': 1,
    '2nd phase - general contingent': 2,
    'Other': 0
}

# --- UI Streamlit ---
menu = st.sidebar.selectbox("Pilih Halaman", ["Prediksi Status Siswa"])

if menu == "Prediksi Status Siswa":
    st.title("🎯 Prediksi Status Mahasiswa")

    with st.form("form_prediksi"):
        col1, col2 = st.columns(2)
        with col1:
            marital_status = st.selectbox("Status Pernikahan", list(marital_status_map.keys()))
            application_mode = st.selectbox("Mode Aplikasi", list(application_mode_map.keys()))
            daytime = st.selectbox("Waktu Kuliah", list(daytime_map.keys()))
            gender = st.selectbox("Jenis Kelamin", list(gender_map.keys()))
            scholarship = st.selectbox("Penerima Beasiswa", list(bool_map.keys()))
            displaced = st.selectbox("Pindah Tempat Tinggal", list(bool_map.keys()))
            debtor = st.selectbox("Ada Hutang Pembayaran", list(bool_map.keys()))
            tuition_fees = st.selectbox("Pembayaran SPP Tepat Waktu", list(bool_map.keys()))
            international = st.selectbox("Mahasiswa Internasional", list(bool_map.keys()))
            special_needs = st.selectbox("Kebutuhan Pendidikan Khusus", list(bool_map.keys()))
            age = st.number_input("Usia Saat Mendaftar", min_value=15, max_value=100, value=18)

        with col2:
            course = st.selectbox("Program Studi", list(course_map.keys()))
            prev_qual = st.selectbox("Kualifikasi Sebelumnya", list(prev_qualification_map.keys()))
            nationality = st.selectbox("Kebangsaan", list(nationality_map.keys()))
            mother_qual = st.selectbox("Kualifikasi Ibu", list(mothers_qual_map.keys()))
            father_qual = st.selectbox("Kualifikasi Ayah", list(fathers_qual_map.keys()))
            mother_job = st.selectbox("Pekerjaan Ibu", list(mothers_occupation_map.keys()))
            father_job = st.selectbox("Pekerjaan Ayah", list(fathers_occupation_map.keys()))
            admission_grade = st.number_input("Nilai Masuk", 0.0, 200.0, 100.0)
            prev_qual_grade = st.number_input("Nilai Kualifikasi Sebelumnya", 0.0, 200.0, 120.0)

        st.subheader("Data Semester 1")
        col3, col4 = st.columns(2)
        with col3:
            sem1_creds = st.number_input("Kredit", 0, 60, 30, key="sem1_creds")
            sem1_enrolled = st.number_input("Daftar", 0, 10, 6, key="sem1_enrolled")
            sem1_eval = st.number_input("Evaluasi", 0, 10, 7, key="sem1_eval")
            sem1_approved = st.number_input("Lulus", 0, 10, 6, key="sem1_approved")
            sem1_grade = st.number_input("Nilai Rata-rata", 0.0, 20.0, 14.0, key="sem1_grade")
        with col4:
            sem1_no_eval = st.number_input("Tanpa Evaluasi", 0, 10, 0, key="sem1_no_eval")


        st.subheader("Data Semester 2")
        col5, col6 = st.columns(2)
        with col5:
            sem2_creds = st.number_input("Kredit", 0, 60, 30, key="sem2_creds")
            sem2_enrolled = st.number_input("Daftar", 0, 10, 6, key="sem2_enrolled")
            sem2_eval = st.number_input("Evaluasi", 0, 10, 7, key="sem2_eval")
            sem2_approved = st.number_input("Lulus", 0, 10, 6, key="sem2_approved")
            sem2_grade = st.number_input("Nilai Rata-rata", 0.0, 20.0, 14.0, key="sem2_grade")
        with col6:
            sem2_no_eval = st.number_input("Tanpa Evaluasi", 0, 10, 0, key="sem2_no_eval")


        st.subheader("Faktor Eksternal")
        col7, col8 = st.columns(2)
        with col7:
            unemployment = st.number_input("Tingkat Pengangguran", 0.0, 30.0, 11.1)
        with col8:
            inflation = st.number_input("Tingkat Inflasi", -10.0, 20.0, 4.2)
        gdp = st.number_input("GDP", -10000.0, 30000.0, 1741.2)

        submitted = st.form_submit_button("Prediksi")

        if submitted:
            input_data = {
                'Marital_status': marital_status_map[marital_status],
                'Application_mode': application_mode_map[application_mode],
                'Course': course_map[course],
                'Daytime_evening_attendance': daytime_map[daytime],
                'Previous_qualification': prev_qualification_map[prev_qual],
                'Nacionality': nationality_map[nationality],
                'Mothers_qualification': mothers_qual_map[mother_qual],
                'Fathers_qualification': fathers_qual_map[father_qual],
                'Mothers_occupation': mothers_occupation_map[mother_job],
                'Fathers_occupation': fathers_occupation_map[father_job],
                'Educational_special_needs': bool_map[special_needs],
                'Displaced': bool_map[displaced],
                'Debtor': bool_map[debtor],
                'Tuition_fees_up_to_date': bool_map[tuition_fees],
                'Gender': gender_map[gender],
                'Scholarship_holder': bool_map[scholarship],
                'International': bool_map[international],
                'Age_at_enrolment': age,
                'Admission_grade': admission_grade,
                'Previous_qualification_grade': prev_qual_grade,
                'Curricular_units_1st_sem_creds': sem1_creds,
                'Curricular_units_1st_sem_enrolled': sem1_enrolled,
                'Curricular_units_1st_sem_evaluations': sem1_eval,
                'Curricular_units_1st_sem_approved': sem1_approved,
                'Curricular_units_1st_sem_grade': sem1_grade,
                'Curricular_units_1st_sem_without_eval': sem1_no_eval,
                'Curricular_units_2nd_sem_creds': sem2_creds,
                'Curricular_units_2nd_sem_enrolled': sem2_enrolled,
                'Curricular_units_2nd_sem_evaluations': sem2_eval,
                'Curricular_units_2nd_sem_approved': sem2_approved,
                'Curricular_units_2nd_sem_grade': sem2_grade,
                'Curricular_units_2nd_sem_without_eval': sem2_no_eval,
                'Unemployment_rate': unemployment,
                'Inflation_rate': inflation,
                'GDP': gdp,
                'Approval_Ratio_1st_sem': sem1_approved / (sem1_enrolled + 1e-6),
                'Approval_Ratio_2nd_sem': sem2_approved / (sem2_enrolled + 1e-6)
            }

            input_df = pd.DataFrame([input_data])

            categorical_cols = [
                'Marital_status', 'Application_mode', 'Course',
                'Daytime_evening_attendance', 'Previous_qualification',
                'Nacionality', 'Mothers_qualification', 'Fathers_qualification',
                'Mothers_occupation', 'Fathers_occupation'
            ]

            input_df = pd.get_dummies(input_df, columns=categorical_cols, drop_first=True)

            # Tambahkan kolom yang hilang
            missing_cols = set(trained_columns) - set(input_df.columns)
            for col in missing_cols:
                input_df[col] = 0

            input_df = input_df[trained_columns]

            # Scaling
            if scaled_columns_names:
                input_df[scaled_columns_names] = scaler.transform(input_df[scaled_columns_names])

            # Prediksi
            prediction = model.predict(input_df)[0]
            proba = model.predict_proba(input_df)[0][1]

            st.subheader("Hasil Prediksi")
            if prediction == 1:
                st.error(f"Prediksi: Mahasiswa ini berisiko **Dropout**")
            else:
                st.success(f"Prediksi: Mahasiswa ini cenderung **Lulus** atau **Masih Terdaftar**")

            st.info(f"Probabilitas Dropout: **{proba:.2f}**")
