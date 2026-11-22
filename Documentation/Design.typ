Variabel yang diperlukan untuk mengukur Weight Gain, Bulking, Weight Loss, Cutting:
+ Berat badan (kg/lbs)
+ Tinggi badan (cm/in)
+ Usia (tahun)
+ Seks (hehe seggss)
+ Kategori aktivitas \
  _\*lihat Multiplier pada TDEE_
+ BMI (Body Mass Index) \
  BMI adalah nilai untuk mengkategorikan perbandingan berat dan tinggi badan seseorang dalam skala BMI
  $ "BMI(kg)" = "berat badan(kg)"/"tinggi badan(cm)"^2 $
  $ "BMI(lbs)" = 703 dot "berat badan(lbs)"/"tinggi badan(in)"^2 $
  #table(
    columns: (2),
    table.header(
      [Nilai], [Kategori]
    ), [\<18.5], [Underweight],
    [18.5 - 24.9], [Normal],
    [25 - 29.9], [Overweight] ,
    [30 - 34.9], [Obesity],
    [35 - 39.9], [Extreme obesity],

  )
+ BMR (Basal Metabolic Rate) \
  BMR adalah jumlah kalori yang diperlukan tubuh dalam keadaan stasioner (tidak beraktivitas/beristirahat). \ \
  Pria:
  $ "BMR[kcal]" = (10 dot "berat-badan[kg]") + (6.25 dot "tinggi-badan[cm]") - (5 dot "usia[tahun]") + 5 $
  Wanita:
  $ "BMR[kcal]" = (10 dot "berat-badan[kg]") + (6.25 dot "tinggi-badan[cm]") - (5 dot "usia[tahun]") - 161 $ \
+ TDEE (Total Daily Energy Expenditure) \
  TDEE adalah jumlah kalori yang diperlukan tubuh untuk beraktivitas sehari-hari. \
  $ "TDEE[kcal]" = "BMR" dot "Multiplier" $

  Multiplier ditentukan dari kategori aktivitas seseorang dalam satu minggunya.
  #table(
    columns: (3),
    table.header(
      [Level], [Contoh], [Nilai]
    ), [Sedentary], [Little to no exercise, such as a desk job with no additional physical activity], [1.2],
    [Lightly Active], [Light exercise 1-2 days/week], [1.375],
    [Moderately Active], [Moderate exercise 3-5 days/week], [1.55] ,
    [Very Active], [Hard exercise 6-7 days/week], [1.725],
    [Extremely Active], [Hard daily exercise and physical job or two times a day training], [1.9]

  )
+ Target rentang waktu (hari)
+ Kategori surplus/defisit kalori
  #table(
    columns: (2),
    table.header(
      [Level], [Nilai]
    ), [Direkomendasikan], [0.1],
    [Agresif], [0.15],
    [Sangat Agresif], [0.2] ,
    [Custom], [(isi sendiri)],

  )

+ Eventual weight change (kg/lbs)
  $ "EWC(lbs)" = "Daily Calorie Surplus/Deficit"/10 $
  $ "EWC(kg)" = "Daily Calorie Surplus/Deficit"/22 $
  _\* EWC memperkirakan perubahan berat badan dalam kurun waktu 3 tahun dengan 95% perubahannya_

+ Expected weight change \
  Dengan menggunakan EWC, kita bisa memperkirakan perubahan berat badan dalam rentang waktu 3 tahun. Contoh: Jika Anda surplus kalori sebesar 500kcal maka EWCnya bernilai sekitar 23kg. Ini artinya jika konsumsi kalori setelah surplus dilakukan secara stabil selama 3 tahun, maka berat Anda akan bertambah 23kg dari berat sebelum surplus. Dengan ini bisa ditarik kesimpulan dalam 6 bulan berat Anda akan bertambah 3.75kg, 1 tahun  7.5kg, 1.5 tahun 11.5kg, dan seterusnya.

Input: \
  Dari list variabel, nomor 1-5 dan 9 akan menjadi input oleh pengguna

Output: \
  Dari list variabel, nomor 6-12 kecuali 9 akan menjadi output oleh program

Catatan: \
  List ini tidak menerangkan(atau menggunakan) jenis makro nutrisi yang digunakan (protein, lemak, dan karbohidrat) dan komposisi tubuh pengguna (persentase lemak tubuh dan massa otot). Saya rasa rekomendasi di area ini perlu ada di output sehingga dapat lebih membantu dalam menerapkan pola hidup sehat penggunanya.

