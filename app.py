import streamlit as st
import joblib
import pandas as pd
import numpy as np
import os

# Path to the models directory relative to the app.py file
MODELS_DIR = 'models'

# Load model, scaler, columns, and scaled column names
try:
    best_model = joblib.load(os.path.join(MODELS_DIR, 'best_dropout_model.pkl'))
    scaler = joblib.load(os.path.join(MODELS_DIR, 'scaler.pkl'))
    model_columns = joblib.load(os.path.join(MODELS_DIR, 'columns.pkl'))
    scaled_columns_names = joblib.load(os.path.join(MODELS_DIR, 'scaled_columns_names.pkl')) # Load the list of scaled column names
except FileNotFoundError as e:
    st.error(f"Error loading model files. Make sure the '{MODELS_DIR}' directory and its contents exist alongside app.py: {e}")
    st.stop()

st.title("Prediksi Risiko Dropout Mahasiswa")
st.write("Masukkan data mahasiswa untuk memprediksi risiko dropout.")

# --- Input Form ---
st.sidebar.header("Data Mahasiswa")


marital_status_options = ['Single', 'Married', 'Widower', 'Divorced', 'Facto union', 'Legally separated']
selected_marital_status = st.sidebar.selectbox("Marital Status", marital_status_options)

application_mode = st.sidebar.number_input("Application Mode", min_value=1, value=1) 

# Course (Numeric/Categorical)
course = st.sidebar.number_input("Course", min_value=1, value=1) 

# Previous Qualification Grade (Numeric)
previous_qualification_grade = st.sidebar.number_input("Previous Qualification Grade", min_value=0.0, value=100.0)

# Curricular Units (Numeric)
curricular_units_1st_sem_enrolled = st.sidebar.number_input("Curricular Units 1st Sem Enrolled", min_value=0, value=5)
curricular_units_2nd_sem_enrolled = st.sidebar.number_input("Curricular Units 2nd Sem Enrolled", min_value=0, value=5)
curricular_units_1st_sem_approved = st.sidebar.number_input("Curricular Units 1st Sem Approved", min_value=0, value=4)
curricular_units_2nd_sem_approved = st.sidebar.number_input("Curricular Units 2nd Sem Approved", min_value=0, value=4)

curricular_units_1st_sem_grade_str = st.sidebar.text_input("Curricular Units 1st Sem Grade", value="10.0")
curricular_units_2nd_sem_grade_str = st.sidebar.text_input("Curricular Units 2nd Sem Grade", value="10.0")


# for Economic Indicators (Numeric)
unemployment_rate = st.sidebar.number_input("Unemployment Rate", min_value=0.0, value=5.0)
inflation_rate = st.sidebar.number_input("Inflation Rate", min_value=0.0, value=1.0)
gdp = st.sidebar.number_input("GDP", min_value=0.0, value=2.0)

# for Gender (Categorical/Binary) 
gender_options = ['Male', 'Female']
selected_gender = st.sidebar.selectbox("Gender", gender_options)

# for Scholarship Holder (Categorical/Binary) 
scholarship_holder_options = ['No', 'Yes']
selected_scholarship_holder = st.sidebar.selectbox("Scholarship Holder", scholarship_holder_options)


# --- Preprocess Input Data ---
processed_input_data = {}
for col in model_columns:
    processed_input_data[col] = 0

# Populate processed_input_data dengan nilai dari input form

# 1. Handle Original Numeric/Cleaned Columns
processed_input_data['Previous_qualification_grade'] = previous_qualification_grade
processed_input_data['Curricular_units_1st_sem_enrolled'] = curricular_units_1st_sem_enrolled
processed_input_data['Curricular_units_2nd_sem_enrolled'] = curricular_units_2nd_sem_enrolled
processed_input_data['Curricular_units_1st_sem_approved'] = curricular_units_1st_sem_approved
processed_input_data['Curricular_units_2nd_sem_approved'] = curricular_units_2nd_sem_approved
processed_input_data['Unemployment_rate'] = unemployment_rate
processed_input_data['Inflation_rate'] = inflation_rate
processed_input_data['GDP'] = gdp


try:
    # konversi Curricular Units Grade 1st Sem
    grade_1st_sem = pd.to_numeric(curricular_units_1st_sem_grade_str.replace('.', '').replace(',', '.'), errors='coerce')
    if pd.isna(grade_1st_sem):
         st.warning(f"Could not convert '{curricular_units_1st_sem_grade_str}' to number for 1st Sem Grade. Using 0.")
         processed_input_data['Curricular_units_1st_sem_grade'] = 0 
    else:
         processed_input_data['Curricular_units_1st_sem_grade'] = grade_1st_sem

    # konversi Curricular Units Grade 2nd Sem
    grade_2nd_sem = pd.to_numeric(curricular_units_2nd_sem_grade_str.replace('.', '').replace(',', '.'), errors='coerce')
    if pd.isna(grade_2nd_sem):
         st.warning(f"Could not convert '{curricular_units_2nd_sem_grade_str}' to number for 2nd Sem Grade. Using 0.")
         processed_input_data['Curricular_units_2nd_sem_grade'] = 0 
    else:
         processed_input_data['Curricular_units_2nd_sem_grade'] = grade_2nd_sem

except Exception as e:
    st.error(f"Error processing grade input: {e}")
    processed_input_data['Curricular_units_1st_sem_grade'] = 0
    processed_input_data['Curricular_units_2nd_sem_grade'] = 0


# 2. Handle Categorical Features (Replikasi One-Hot Encoding - drop_first=True)

if selected_marital_status != 'Single':
    ohe_col_name = f'Marital_status_{selected_marital_status}'
    if ohe_col_name in model_columns:
        processed_input_data[ohe_col_name] = 1
    # else:
    #     st.warning(f"Marital Status category '{selected_marital_status}' not found in model columns. This input might be ignored.")


# for Gender: Assuming 'Male' was dropped
if selected_gender == 'Female':
     if 'Gender_1' in model_columns: 
         processed_input_data['Gender_1'] = 1
     else:
        st.warning(f"Gender category 'Female' mapping (Gender_1) not found in model columns. This input might be ignored.")

# for Scholarship Holder: Assuming 'No' was dropped
if selected_scholarship_holder == 'Yes':
    if 'Scholarship_holder_1' in model_columns: 
         processed_input_data['Scholarship_holder_1'] = 1
    else:
        st.warning(f"Scholarship Holder category 'Yes' mapping (Scholarship_holder_1) not found in model columns. This input might be ignored.")

# Debtor
debtor_options = ['No', 'Yes']
selected_debtor = st.sidebar.selectbox("Debtor", debtor_options)
if selected_debtor == 'Yes' and 'Debtor_1' in model_columns:
    processed_input_data['Debtor_1'] = 1

# Tuition fees up to date
tuition_options = ['No', 'Yes']
selected_tuition = st.sidebar.selectbox("Tuition Fees Up-to-Date", tuition_options)
if selected_tuition == 'Yes' and 'Tuition_fees_up_to_date_1' in model_columns:
    processed_input_data['Tuition_fees_up_to_date_1'] = 1

# Father's qualification
fathers_qual = st.sidebar.number_input("Father's Qualification (kode)", min_value=1, max_value=99, value=34)
father_ohe_col = f"Fathers_qualification_{fathers_qual}"
if father_ohe_col in model_columns:
    processed_input_data[father_ohe_col] = 1

# Mother's occupation
mothers_occ = st.sidebar.number_input("Mother's Occupation (kode)", min_value=1, max_value=999, value=191)
mother_ohe_col = f"Mothers_occupation_{mothers_occ}"
if mother_ohe_col in model_columns:
    processed_input_data[mother_ohe_col] = 1

# Course (numeric kategori)
course = st.sidebar.number_input("Course", min_value=1, max_value=9999, value=9853)
course_ohe_col = f"Course_{course}"
if course_ohe_col in model_columns:
    processed_input_data[course_ohe_col] = 1


# 3. Handle Feature Engineering 
processed_input_data['Approval_Ratio_1st_sem'] = curricular_units_1st_sem_approved / (curricular_units_1st_sem_enrolled + 1e-6)
processed_input_data['Approval_Ratio_2nd_sem'] = curricular_units_2nd_sem_approved / (curricular_units_2nd_sem_enrolled + 1e-6)


# Convert to DataFrame
input_df = pd.DataFrame([processed_input_data])

input_df = input_df[model_columns]


# 4. Scale the Numeric Features 
try:
    cols_to_scale_in_input = [col for col in scaled_columns_names if col in input_df.columns]
    input_df[scaled_columns_names] = scaler.transform(input_df[scaled_columns_names])

except Exception as e:
     st.error(f"Error during scaling input data. Details: {e}")
     st.stop()


# --- Prediction ---
if st.sidebar.button("Prediksi Risiko Dropout"):
    try:
        prediction = best_model.predict(input_df)
        # Ensure predict_proba is available for the model
        if hasattr(best_model, 'predict_proba'):
             prediction_proba = best_model.predict_proba(input_df)[:, 1] 
        else:
            prediction_proba = None
            st.warning("Model does not support probability prediction.")

        st.subheader("Hasil Prediksi:")
        if prediction[0] == 1:
            st.error(f"Mahasiswa ini **BERISIKO TINGGI** untuk dropout.")
        else:
            st.success(f"Mahasiswa ini memiliki **RISIKO RENDAH** untuk dropout.")

        if prediction_proba is not None:
            st.write(f"Probabilitas Dropout: **{prediction_proba[0]:.2f}**")

    except Exception as e:
        st.error(f"Terjadi error saat melakukan prediksi. Pastikan format data input sesuai dengan model: {e}")