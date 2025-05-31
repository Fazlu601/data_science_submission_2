# Proyek Akhir: Menyelesaikan Permasalahan Institusi Pendidikan: Jaya Jaya Institut

## Business Understanding

Jaya Jaya Institut adalah salah satu institusi pendidikan perguruan yang telah berdiri sejak tahun 2000. Namun, mereka menghadapi tantangan tingginya *dropout rate* atau tingkat siswa yang tidak menyelesaikan pendidikannya. Hal ini berdampak negatif pada reputasi institusi, efisiensi penggunaan sumber daya, dan semangat belajar siswa.

### Permasalahan Bisnis

Permasalahan bisnis yang akan diselesaikan adalah:

*   **Tingginya dropout rate:** Jaya Jaya Institut mengalami tingkat *dropout* siswa yang tinggi, yang perlu dikurangi untuk meningkatkan reputasi dan efisiensi institusi.
*   **Kurangnya pemahaman tentang faktor-faktor pendorong dropout:** Pihak institusi membutuhkan informasi dan *insight* yang lebih dalam tentang faktor-faktor yang menyebabkan siswa *dropout*.
*   **Kebutuhan akan sistem deteksi dini:** Pihak institusi membutuhkan sistem untuk mendeteksi siswa yang berisiko *dropout* sejak dini sehingga dapat diberi bimbingan khusus.

### Cakupan Proyek

Proyek ini mencakup:

*   **Analisis data:** Melakukan eksplorasi data dan analisis statistik untuk memahami pola dan tren *dropout rate* di Jaya Jaya Institut.
*   **Pemodelan machine learning:** Membangun model *machine learning* untuk memprediksi probabilitas siswa *dropout* berdasarkan data historis.
*   **Identifikasi faktor penting:** Mengidentifikasi faktor-faktor yang paling berpengaruh terhadap *dropout rate* siswa.
*   **Memberikan rekomendasi aksi:** Memberikan rekomendasi kepada pihak Jaya Jaya Institut untuk mengurangi *dropout rate* berdasarkan hasil analisis dan model prediksi.

### Persiapan

Agar proyek ini dapat dijalankan dengan lancar, ikuti langkah-langkah persiapan berikut:

1.  **Sumber Data**

    ```
    FOLDER/
    ├── dataset/
    │   └── data.csv
    ├── models/
    │   ├── best_dropout_model.pkl
    │   ├── columns.pkl
    │   ├── scaled_columns_names.pkl
    │   ├── scaler.pkl
    ├── app.py
    ├── fazlu_rachman06-dashboard.pdf
    ├── fazlu_rachman06-dashboard.png
    ├── metabase.db.mv.db
    ├── notebook.ipynb
    ├── README.md
    └── requirements.txt
    ```

    Penjelasan :

    *   dataset : Menyimpan file dataset utama.

    *   models : Berisi file model machine learning dan pendukungnya (pickle files).

    *   app.py: Skrip prototype utama.

    *   fazlu_rachman06-dashboard.*: File dashboard dalam format PDF dan PNG.

    *   metabase.db.mv.db: File database Metabase.

    *   notebook.ipynb: Notebook utama untuk eksplorasi dan eksperimen.

    *   README.md: Dokumentasi proyek.

    *   requirements.txt: Daftar dependensi Python.


2.  **Membuat dan Mengaktifkan Virtual Environment**
    *   Buka terminal dan jalankan :
        
              `python -m venv venv`
    *   Aktifkan environment :
        -   Windows :

                 `venv\Scripts\activate`
        -   macOS/Linux :

                `source venv/bin/activate`

3.  **Menginstal Dependensi dari `requirements.txt`**
    *   Semua pustaka Python yang dibutuhkan untuk menjalankan proyek ini tercantum dalam file `requirements.txt`.
    *   Pastikan Anda berada di direktori proyek yang sama dengan file `requirements.txt` dan virtual environment Anda sudah aktif (jika Anda menggunakannya).
    *   Instal semua dependensi dengan perintah berikut:

4.  **Cara Menjalankan Skrip Python**
    *   Buka Terminal
    *   Jalankan perintah `streamlit run app.py`

[Link Dashboard](https://lookerstudio.google.com/reporting/05405c4b-b229-4e12-95d2-55221015be37)

[Link Streamlit](https://datasciencesubmission2-9vr6g4agykbb7mstfhdch5.streamlit.app)


## Conclusion

Dari analisis dan pengembangan model dalam proyek ini, dapat disimpulkan beberapa hal penting terkait prediksi *dropout* di institusi pendidikan:

*   **Situasi Dropout:** Dataset menunjukkan adanya siswa dengan status 'Dropout', yang mengindikasikan bahwa *dropout rate* merupakan isu yang relevan untuk ditangani.
*   **Model Performa Terbaik:** Berdasarkan metrik evaluasi seperti Classification Report, Confusion Matrix, Accuracy, Precision, Recall, F1-score, dan ROC AUC pada data pengujian, **XGBoost** menunjukkan performa yang sangat baik dalam memprediksi *dropout*, diikuti oleh Random Forest. Model ini efektif dalam mengidentifikasi siswa yang berisiko tinggi untuk *dropout*, meskipun metrik pada kelas minoritas (Dropout) mungkin masih menunjukkan ruang untuk perbaikan karena sifat ketidakseimbangan data (yang sudah ditangani dengan SMOTE).
*   **Faktor-faktor Penting (Feature Importance):** Analisis *Feature Importance* dari model terbaik (XGBoost) mengidentifikasi fitur-fitur yang paling berpengaruh terhadap probabilitas *dropout*. Fitur-fitur teratas meliputi:
    *   `Curricular_units_1st_sem_approved`
    *   `Curricular_units_2nd_sem_approved`
    *   `Curricular_units_1st_sem_enrolled`
    *   `Curricular_units_2nd_sem_enrolled`
    *   `Previous_qualification_grade`
    *   `Approval_Ratio_1st_sem` (fitur hasil engineering)
    *   `Approval_Ratio_2nd_sem` (fitur hasil engineering)
    *   `Age_at_enrollment`
    *   Beberapa fitur lain yang juga berkontribusi, termasuk yang terkait dengan latar belakang pendidikan dan lingkungan sosial ekonomi (`Unemployment_rate`, `Inflation_rate`, `GDP`).
*   **Nilai Hasil Belajar sebagai Indikator Kunci:** Fitur-fitur yang berkaitan langsung dengan capaian akademik siswa dalam unit kurikuler (jumlah unit yang disetujui, rasio persetujuan) muncul sebagai prediktor yang sangat kuat.

### Rekomendasi Action Items

Berikut adalah beberapa rekomendasi tindakan strategis yang dapat dipertimbangkan oleh institusi pendidikan berdasarkan temuan proyek ini untuk mengurangi *dropout rate* dan meningkatkan retensi siswa:

*   **Implementasi Sistem Peringatan Dini (Early Warning System):** Manfaatkan model XGBoost yang telah dilatih untuk membangun sistem peringatan dini. Sistem ini dapat secara otomatis mengidentifikasi siswa yang berisiko tinggi *dropout* berdasarkan data akademik dan non-akademik mereka.
*   **Program Intervensi Terarget:** Fokuskan sumber daya pada siswa yang teridentifikasi berisiko tinggi. Intervensi dapat berupa:
    *   **Bimbingan Akademik Intensif:** Memberikan dukungan tambahan bagi siswa yang kesulitan dalam menyelesaikan atau mendapatkan persetujuan pada unit kurikuler di semester awal.
    *   **Konseling dan Dukungan Psikososial:** Menyediakan layanan konseling untuk mengatasi faktor-faktor non-akademik yang mungkin berkontribusi pada risiko *dropout* (misalnya, masalah personal, kesulitan adaptasi).
    *   **Mentoring Sejawat atau Dosen:** Menghubungkan siswa berisiko dengan mentor yang dapat memberikan panduan dan motivasi.
*   **Analisis Mendalam tentang Kinerja Akademik Semester Awal:** Selidiki lebih lanjut mengapa kinerja di semester pertama dan kedua (jumlah unit yang disetujui dan diambil) menjadi prediktor yang kuat. Apakah ada kurikulum atau mata kuliah tertentu yang menjadi hambatan umum? Bagaimana metode pengajaran dapat disesuaikan?
*   **Evaluasi Kurikulum dan Beban Akademik:** Tinjau kembali kurikulum dan beban unit kurikuler, terutama di semester-semester awal, untuk memastikan bahwa siswa memiliki fondasi yang kuat dan tidak kewalahan.
*   **Dukungan Terkait Faktor Eksternal:** Meskipun pengaruhnya mungkin tidak sebesar faktor akademik, perhatikan juga faktor eksternal seperti kondisi ekonomi (yang tercermin dalam `Unemployment_rate`). Institusi dapat mengeksplorasi program bantuan finansial atau sumber daya pendukung lainnya jika relevan.
*   **Pemanfaatan Fitur Rekayasa (Feature Engineering):** Fitur `Approval_Ratio` yang dibuat dalam proyek ini terbukti penting. Institusi dapat mempertimbangkan untuk memantau rasio ini secara berkala sebagai salah satu indikator dini.
*   **Pelatihan Personel:** Berikan pelatihan kepada dosen dan staf akademik untuk mengenali tanda-tanda awal kesulitan siswa dan cara merujuk mereka ke layanan pendukung yang tepat.
*   **Integrasi Data:** Pastikan data siswa (akademik, demografi, dll.) terintegrasi dengan baik untuk memudahkan identifikasi risiko *dropout* secara holistik.

Dengan mengimplementasikan rekomendasi ini, institusi pendidikan dapat mengambil langkah proaktif untuk mendukung siswa, meningkatkan tingkat kelulusan, dan mengurangi angka *dropout*.