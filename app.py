import streamlit as st
import pandas as pd
import numpy as np
import joblib
import os

# --- Load Model and Scaler ---
try:
    # Pastikan path ke folder models sudah benar
    model_path = 'models/best_dropout_model.pkl'
    scaler_path = 'models/scaler.pkl'
    columns_path = 'models/columns.pkl'

    # Cek apakah file ada sebelum memuat
    if not os.path.exists(model_path):
         st.error(f"Model file not found at {model_path}")
         st.stop()
    if not os.path.exists(scaler_path):
         st.error(f"Scaler file not found at {scaler_path}")
         st.stop()
    if not os.path.exists(columns_path):
         st.error(f"Columns file not found at {columns_path}")
         st.stop()

    model = joblib.load(model_path)
    scaler = joblib.load(scaler_path)
    feature_columns = joblib.load(columns_path) # List of column names the model expects

except FileNotFoundError as e:
    st.error(f"Error loading model files: {e}. Make sure 'models' directory and files are correct.")
    st.stop()
except Exception as e:
     st.error(f"An unexpected error occurred while loading files: {e}")
     st.stop()


# --- Application Title and Description ---
st.title("Prediksi Potensi Dropout Mahasiswa")
st.write("Aplikasi ini memprediksi potensi mahasiswa untuk dropout berdasarkan data historis.")

# --- Dummy Data for Testing ---
# Pastikan data dummy mencakup SEMUA fitur input asli sebelum OHE
dummy_data = {
    'Previous_qualification_grade': 120.0,
    'Curricular_units_1st_sem_enrolled': 6.0,
    'Curricular_units_1st_sem_approved': 4.0,
    'Curricular_units_2nd_sem_enrolled': 6.0,
    'Curricular_units_2nd_sem_approved': 5.0,
    'Unemployment_rate': 10.8,
    'Inflation_rate': 1.4,
    'GDP': 1.74,
    'Age_at_enrollment': 18,
    'Curricular_units_1st_sem_evaluations': 12,
    'Curricular_units_1st_sem_without_evaluations': 2,
    'Curricular_units_2nd_sem_evaluations': 10,
    'Curricular_units_2nd_sem_without_evaluations': 1,
    'Curricular_units_1st_sem_grade': 13.5,
    'Curricular_units_2nd_sem_grade': 14.0,
    'Admission_grade': 130.0,
    # Add dummy values for categorical features
    # IMPORTANT: These must be ACTUAL valid categories used in your training data
    'Marital_status': 'Single',
    'Application_mode': '1st phase - general contingent',
    'Course': 'Informatics Engineering', # Example, change to one from your data
    'Daytime_evening_attendance': 'Daytime',
    'Previous_qualification': 'Secondary education',
    'Nacionality': 'Portuguese',
    'Mothers_qualification': 'Secondary education',
    'Fathers_qualification': 'Secondary education',
    'Mothers_occupation': 'Other',
    'Fathers_occupation': 'Other',
    'Educational_special_needs': 'No',
    'Displaced': 'Yes',
    'Debtor': 'No',
    'Tuition_fees_up_to_date': 'Yes',
    'Gender': 'Male',
    'Scholarship_holder': 'No',
    'International': 'No'
}

# Define numerical columns for input (before any engineering)
numerical_cols_for_input = [
    'Previous_qualification_grade',
    'Curricular_units_1st_sem_enrolled',
    'Curricular_units_1st_sem_approved',
    'Curricular_units_2nd_sem_enrolled',
    'Curricular_units_2nd_sem_approved',
    'Unemployment_rate',
    'Inflation_rate',
    'GDP',
    'Age_at_enrollment',
    'Curricular_units_1st_sem_evaluations',
    'Curricular_units_1st_sem_without_evaluations',
    'Curricular_units_2nd_sem_evaluations',
    'Curricular_units_2nd_sem_without_evaluations',
    'Curricular_units_1st_sem_grade',
    'Curricular_units_2nd_sem_grade',
    'Admission_grade'
]

# Define categorical columns (based on your notebook's OHE)
categorical_cols = [
    'Marital_status',
    'Application_mode',
    'Course',
    'Daytime_evening_attendance',
    'Previous_qualification',
    'Nacionality',
    'Mothers_qualification',
    'Fathers_qualification',
    'Mothers_occupation',
    'Fathers_occupation',
    'Educational_special_needs',
    'Displaced',
    'Debtor',
    'Tuition_fees_up_to_date',
    'Gender',
    'Scholarship_holder',
    'International'
]

# Get actual valid categories from your training data for selectbox options
# This is the crucial part to ensure OHE works correctly
# You need to save these lists during your notebook run
# Example:
# valid_categories = joblib.load('models/valid_categories.pkl')
# Where valid_categories is a dictionary like {'Marital_status': ['Single', 'Married', ...], ...}

# For demonstration, using example options - replace with your actual saved list!
try:
    categorical_options = joblib.load('models/categorical_options.pkl') # Load the saved categories
except FileNotFoundError:
    st.warning("Category options file not found ('models/categorical_options.pkl'). Using placeholder options.")
    # Placeholder options - REPLACE THIS WITH YOUR ACTUAL DATA'S CATEGORIES
    categorical_options = {
        'Marital_status': ['Single', 'Married', 'Widower', 'Divorced', 'Facto Union', 'Legally Separated'],
        'Application_mode': ['1st phase - general contingent', 'Ordinance No. 612/93', '2nd phase - general contingent', 'Ordinance No. 423/2006', 'Transfer', 'Change of course', 'Technological specialization diploma holders', 'Change of institution/course', 'Ordinance No. 854/99 (Alentejo Institute of Technology)', 'International students (Decree-Law No 36/2014)', '1st phase - special contingent (Azores Island)', 'Veterans', 'Holders of other higher courses', '2nd phase - special contingent (Azores Island)', 'Institutional Transfer', 'Student with a disability', 'Foreign students (Decree-Law No 36/2014)'],
        'Course': ['Biofuel production technologies', 'Animation and Multimedia Design', 'Social Service', 'Agronomy', 'Communication Design', 'Veterinary Nursing', 'Informatics Engineering', 'Equinculture', 'Management', 'Social Service (evening attendance)'],
        'Daytime_evening_attendance': ['Daytime', 'Evening attendance'],
        'Previous_qualification': ['Secondary education', "Higher education - bachelor's degree", "Higher education - degree", "Higher education - master's degree", "Higher education - doctorate"],
        'Nacionality': ['Portuguese', 'German', 'Spanish', 'Italian', 'French', 'Dutch', 'Mexican', 'Brazilian', 'Angolan', 'Cape Verdean', 'Guinean', 'Mozambican', 'Sao Tome and Principe', 'Turkish', 'Other'],
        'Mothers_qualification': ['Basic education (3rd cycle)', 'Secondary education', 'Higher education'],
        'Fathers_qualification': ['Basic education (3rd cycle)', 'Secondary education', 'Higher education'],
        'Mothers_occupation': ['Student', 'Other', 'Homemaker', 'Technician', 'Administrative staff', 'Teacher'],
        'Fathers_occupation': ['Student', 'Other', 'Homemaker', 'Technician', 'Administrative staff', 'Teacher'],
        'Educational_special_needs': ['No', 'Yes'],
        'Displaced': ['No', 'Yes'],
        'Debtor': ['No', 'Yes'],
        'Tuition_fees_up_to_date': ['No', 'Yes'],
        'Gender': ['Male', 'Female'],
        'Scholarship_holder': ['No', 'Yes'],
        'International': ['No', 'Yes']
    }


# --- Input Form ---
st.header("Masukkan Data Mahasiswa:")

# Checkbox for dummy data
use_dummy = st.checkbox("Gunakan Data Dummy")

# Initialize input_values dictionary
input_values = {}
if use_dummy:
    input_values = dummy_data
else:
     # Initialize with default values if not using dummy data
     for col in numerical_cols_for_input:
         input_values[col] = 0.0
     for col in categorical_cols:
         # Use the first option from actual categories as default if available
         if col in categorical_options and categorical_options[col]:
             input_values[col] = categorical_options[col][0]
         else:
             input_values[col] = ""


# Dictionary to store values from Streamlit input widgets
user_input = {}

# Input fields for numerical features
st.subheader("Data Numerik:")
for col in numerical_cols_for_input:
    # Use the value from input_values to pre-fill
    user_input[col] = st.number_input(f"Masukkan nilai untuk '{col}':", value=float(input_values.get(col, 0.0)))

# Input fields for categorical features using selectbox
st.subheader("Data Kategorikal:")
for col in categorical_cols:
    options = categorical_options.get(col, [])
    default_value = input_values.get(col, None)

    if options:
        # Find the index of the default value
        try:
            default_index = options.index(default_value)
        except ValueError:
            # If the default value (from dummy data or initial default) is not in options,
            # default to the first option or None.
            default_index = 0 if options else None

        user_input[col] = st.selectbox(f"Pilih nilai untuk '{col}':", options=options, index=default_index)
    else:
        # Fallback to text input if no options are defined (less ideal)
        user_input[col] = st.text_input(f"Masukkan nilai untuk '{col}':", value=str(default_value))


# --- Prediction Button ---
if st.button("Prediksi"):
    # --- Data Preprocessing (based on your notebook) ---

    # Create a DataFrame from user input gathered from the widgets
    input_df = pd.DataFrame([user_input])

    # Handle potential non-numeric input (should be less likely with selectbox/number_input)
    for col in numerical_cols_for_input: # Only check numerical columns
        input_df[col] = pd.to_numeric(input_df[col], errors='coerce')
        if input_df[col].isnull().any():
             # Fill NaNs with 0 as a fallback. Ideally, use median/mean from training data.
             input_df[col].fillna(0, inplace=True)

    # Apply One-Hot Encoding
    # Use the known categories from training data during OHE
    # This ensures consistent columns even if input data is missing categories
    # However, pd.get_dummies by default will create columns based on the input data
    # A better approach is to manually create dummy columns based on ALL possible categories
    # Let's stick to the original get_dummies and then align columns, but refine alignment.

    input_df = pd.get_dummies(input_df, columns=categorical_cols, drop_first=True)


    # --- Feature Engineering (Create the new ratio features) ---
    # Use the columns that exist in the input_df after OHE but before alignment
    # Ensure the base columns for ratios are treated as numeric
    for ratio_col in ['Curricular_units_1st_sem_approved', 'Curricular_units_1st_sem_enrolled',
                      'Curricular_units_2nd_sem_approved', 'Curricular_units_2nd_sem_enrolled']:
        if ratio_col in input_df.columns:
            input_df[ratio_col] = pd.to_numeric(input_df[ratio_col], errors='coerce').fillna(0) # Ensure numeric

    if 'Curricular_units_1st_sem_approved' in input_df.columns and 'Curricular_units_1st_sem_enrolled' in input_df.columns:
         input_df['Approval_Ratio_1st_sem'] = input_df['Curricular_units_1st_sem_approved'] / (input_df['Curricular_units_1st_sem_enrolled'] + 1e-6)
    else:
        # If base columns are missing, create the ratio column and set to 0
        input_df['Approval_Ratio_1st_sem'] = 0

    if 'Curricular_units_2nd_sem_approved' in input_df.columns and 'Curricular_units_2nd_sem_enrolled' in input_df.columns:
         input_df['Approval_Ratio_2nd_sem'] = input_df['Curricular_units_2nd_sem_approved'] / (input_df['Curricular_units_2nd_sem_enrolled'] + 1e-6)
    else:
        # If base columns are missing, create the ratio column and set to 0
         input_df['Approval_Ratio_2nd_sem'] = 0


    # --- Align Columns with Training Data (More Robust) ---
    # Create a DataFrame with all expected feature columns, filled with 0
    aligned_input_df = pd.DataFrame(0, index=[0], columns=feature_columns)

    # Copy the values from the processed input_df to the aligned DataFrame
    # This handles both missing columns (they remain 0) and extra columns (they are ignored)
    for col in input_df.columns:
        if col in aligned_input_df.columns:
            aligned_input_df[col] = input_df[col].iloc[0] # Use .iloc[0] to get the single row value

    # Now aligned_input_df has the correct columns in the correct order, with missing dummies as 0

    # --- Apply Scaling ---
    # Identify numerical columns IN THE ALIGNED DATAFRAME that need scaling
    # These should match the columns the scaler was trained on
    # Assuming the scaler was fit on all numerical columns in the final X_train_smote
    numerical_cols_in_aligned_df = aligned_input_df.select_dtypes(include=np.number).columns.tolist()

    try:
        # Ensure we only attempt to scale columns the scaler was trained on
        # A more robust way is to save scaler.feature_names_in_ if using scikit-learn >= 1.0
        # For now, assuming scaler was fit on all numerical columns in feature_columns
        cols_to_scale = [col for col in numerical_cols_in_aligned_df if col in feature_columns] # Simple check

        if cols_to_scale:
            # Create a temporary copy for scaling
            temp_df_for_scaling = aligned_input_df[cols_to_scale].copy()
            # Scale the temporary copy
            scaled_data = scaler.transform(temp_df_for_scaling)
            # Put the scaled data back into the aligned_input_df
            aligned_input_df[cols_to_scale] = scaled_data
        else:
            st.warning("No numerical columns identified for scaling. Check feature_columns list.")


    except Exception as e:
         st.error(f"Error during scaling: {e}")
         st.write("Please ensure the scaler is compatible with the processed input columns.")
         st.stop()


    # --- Make Prediction ---
    try:
        # Predict using the aligned and scaled DataFrame
        prediction = model.predict(aligned_input_df)
        # Get probability using the aligned and scaled DataFrame
        prediction_proba = model.predict_proba(aligned_input_df)[:, 1]

        # --- Display Result ---
        st.subheader("Hasil Prediksi:")
        if prediction[0] == 1:
            st.error(f"Mahasiswa ini **berpotensi tinggi untuk DO (Dropout)** dengan probabilitas: {prediction_proba[0]:.2f}")
            st.write("Rekomendasi: Berikan bimbingan khusus atau dukungan tambahan.")
        else:
            st.success(f"Mahasiswa ini **cenderung tidak DO** dengan probabilitas dropout: {prediction_proba[0]:.2f}")
            st.write("Rekomendasi: Tetap pantau perkembangannya.")

    except Exception as e:
        st.error(f"An error occurred during prediction: {e}")
        st.write("Please check the input values and try again.")