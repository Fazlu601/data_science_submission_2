# Proyek Akhir: Menyelesaikan Permasalahan Perusahaan Edutech: Jaya Jaya Maju

## Business Understanding

Jaya Jaya Maju adalah perusahaan edutech yang sedang berkembang pesat.  Namun, mereka menghadapi tantangan tingginya attrition rate atau tingkat resign karyawan. Hal ini berdampak negatif pada produktivitas, biaya rekrutmen, dan moral karyawan. 

### Permasalahan Bisnis

Permasalahan bisnis yang akan diselesaikan adalah:

* **Tingginya attrition rate:** Jaya Jaya Maju mengalami tingkat resign karyawan yang tinggi, yang perlu dikurangi untuk meningkatkan efisiensi dan produktivitas perusahaan.
* **Kurangnya pemahaman tentang faktor-faktor pendorong attrition:** Departemen HR membutuhkan informasi dan insight yang lebih dalam tentang faktor-faktor yang menyebabkan karyawan resign.
* **Kebutuhan akan business dashboard:** Departemen HR membutuhkan business dashboard interaktif untuk memantau attrition rate, mengidentifikasi faktor risiko, dan mengambil tindakan preventif.

### Cakupan Proyek

Proyek ini mencakup:

* **Analisis data:** Melakukan eksplorasi data dan analisis statistik untuk memahami pola dan tren attrition rate di Jaya Jaya Maju.
* **Pemodelan machine learning:** Membangun model machine learning untuk memprediksi probabilitas karyawan resign berdasarkan data historis.
* **Identifikasi faktor penting:** Mengidentifikasi faktor-faktor yang paling berpengaruh terhadap attrition rate.
* **Pembuatan business dashboard:** Mengembangkan business dashboard interaktif di Metabase yang menampilkan insight dari analisis data dan model machine learning.
* **Memberikan rekomendasi aksi:** Memberikan rekomendasi kepada departemen HR untuk mengurangi attrition rate berdasarkan hasil analisis dan dashboard.


### Persiapan

**Sumber data:**

* Dataset `employee_data.csv` yang berisi data karyawan Jaya Jaya Maju, meliputi informasi demografi, pekerjaan, dan status attrition. Data ini diupload ke Supabase dan dihubungkan dengan Metabase.

**Setup environment:**

```
!apt-get install docker.io -y !apt-get update -y 
!service docker start !docker pull metabase/metabase !docker run -d -p 3000:3000 --name metabase metabase/metabase
```

## Business Dashboard

Business dashboard yang telah dibuat menampilkan informasi dan insight tentang attrition rate di Jaya Jaya Maju.  Dashboard ini berisi visualisasi seperti:

* Jumlah karyawan yang resign dan tidak resign.
* Distribusi karyawan berdasarkan departemen dan JobRole.
* Feature importance dari model machine learning.

Dashboard ini membantu departemen HR untuk:

* Memantau attrition rate secara real-time.
* Mengidentifikasi faktor-faktor risiko yang berkontribusi terhadap attrition.
* Mengambil tindakan preventif untuk mengurangi attrition.


[Link Dashboard](http://localhost:3000/public/dashboard/233667c3-95f2-4985-9b86-8e4cb4fc0ed1)


## Conclusion

Dari proyek ini, dapat disimpulkan bahwa:

* Attrition rate di Jaya Jaya Maju cukup tinggi dan perlu ditangani secara serius.
* Faktor-faktor seperti OverTime, MonthlyIncome, JobRole, dan TotalWorkingYears memiliki pengaruh signifikan terhadap attrition rate.
* Business dashboard yang telah dibuat dapat membantu departemen HR dalam memantau dan mengendalikan attrition rate.

### Rekomendasi Action Items

Berikut adalah beberapa rekomendasi action items yang dapat dilakukan perusahaan untuk mengurangi attrition rate:

* **Meningkatkan program retensi karyawan:** Memberikan insentif dan benefit yang lebih baik, meningkatkan work-life balance, dan menciptakan budaya kerja yang positif.
* **Menyesuaikan kebijakan kompensasi dan benefit:** Meninjau gaji dan benefit yang ditawarkan kepada karyawan, dan memastikan bahwa mereka kompetitif di pasar.
* **Memberikan pelatihan dan pengembangan karir:** Memberikan kesempatan kepada karyawan untuk mengembangkan skill dan karir mereka di dalam perusahaan.
* **Mengurangi beban kerja dan OverTime:**  Mengkaji beban kerja karyawan dan mengurangi OverTime yang berlebihan.
* **Meningkatkan komunikasi dan feedback:**  Memperbaiki komunikasi antara manajemen dan karyawan, dan memberikan feedback yang konstruktif secara teratur.
* **Memanfaatkan model machine learning:**  Menggunakan model machine learning untuk memprediksi karyawan yang berisiko tinggi resign dan mengambil tindakan preventif.