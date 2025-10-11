# 🧠 EDA Project on Healthcare Dataset  

This project focuses on performing a **comprehensive Exploratory Data Analysis (EDA)** on a healthcare dataset under the guidance of **[The RD Group of Industry](https://github.com/TheRDGroupOfIndustries)**.  
The goal was to analyze **key healthcare metrics** and uncover **patterns in billing, patient demographics, and medical insights**.

---

## 📂 Project Overview  

- **Domain:** Healthcare Analytics  
- **Objective:** Identify hidden trends and correlations related to patient data, billing, and treatment patterns.  
- **Tech Stack:** Python, Pandas, Matplotlib, Seaborn, NumPy, Jupyter Notebook  

---

## 🧹 Data Cleaning Phase  

Data cleaning was led by **[Nandini](https://github.com/nandiniarjun03)**.  
All cleaning-related files can be explored here:  
👉 [`/data_cleaning/`](data_cleaning/)

Detailed documentation of the cleaning process:  
📄[`ISSUE_RESOLUTION_REPORT.md`](data_cleaning/ISSUE_RESOLUTION_REPORT.md)

**Key Cleaning Steps:**
- Removed **missing values** and **duplicate records**  
- Adjusted **data types** (object, numeric, datetime)  
- Corrected **inconsistent or mis-typed entries**  
- Ensured **data quality and validity** before EDA  

📊 **Cleaned Dataset:**  
[`Cleaned_Medical_Data.csv`](Cleaned_Medical_Data.csv)

---

## 📊 Exploratory Data Analysis (EDA)  

EDA was performed by **me** to identify statistical relationships and business insights.  
Find the complete notebook here:  
📘 [`Final_Medical_Dataset.ipynb`](Final_Medical_Dataset.ipynb)


---

## 📈 Visualizations & Graphs  

A range of analytical visuals were created to explore billing, patient demographics, and disease trends.

| Analysis | Visualization |
|-----------|----------------|
| 🩸 **Billing Amount over Time** | ![Billing Amount Analysis over Time](Project%20Screenshots/Billing%20Amount%20Analysis%20over%20time.png) |
| 💰 **Billing Amount by Blood Type** | ![Billing Amount Distribution by Blood Type](Project%20Screenshots/Billing%20Amount%20Distribution%20by%20Blood%20Type.png) |
| 🏥 **Billing by Admission Type (Yearly)** | ![Billing Amount by Admission Type over Year](Project%20Screenshots/Billing%20Amount%20by%20Admission%20Type%20over%20Year.png) |
| ⏱ **Billing vs Length of Stay** | ![Billing Amount vs Length of Stay](Project%20Screenshots/Billing%20Amount%20vs%20Length%20of%20stay.png) |
| 👶 **Patients by Age Group** | ![Distribution of Patients by Age Group](Project%20Screenshots/Distribution%20of%20patients%20by%20Age%20group.png) |
| ⚕️ **Elective Admissions by Condition & Gender** | ![Elective Admissions](Project%20Screenshots/Elective%20adm.%20By%20Medical%20Condition%20and%20gender.png) |
| 🚑 **Emergency Admissions by Condition & Gender** | ![Emergency Admissions](Project%20Screenshots/Emergency%20adm.%20By%20Medical%20Condition%20and%20gender.png) |
| 🚨 **Urgent Admissions by Condition & Gender** | ![Urgent Admissions](Project%20Screenshots/Urgent%20adm.%20By%20Medical%20Condition%20and%20gender.png) |
| 🔥 **Heatmap: Age, Billing, Length of Stay** | ![Heatmap](Project%20Screenshots/Heatmap%20btw%20Age,%20Billing%20Amount,%20Length%20of%20stay.png) |
| 🎗 **Cancer Patients by Blood Type** | ![Cancer Patients](Project%20Screenshots/No.%20of%20Cancer%20patients%20by%20Blood%20Type.png) |
| 🧾 **Patient Count by Admission Type (Yearly)** | ![Patient Count](Project%20Screenshots/Patient%20Count%20by%20Admission%20type%20over%20year.png) |
| 🧍 **Patients by Age Group & Condition** | ![Patient Count](Project%20Screenshots/Patient%20Count%20by%20Age%20group%20and%20Medical%20condition.png) |
| 🧑‍⚕️ **Patient Count by Insurance Provider** | ![Insurance Provider](Project%20Screenshots/Patient%20count%20by%20insurance%20provider.png) |
| 💳 **Total Billing by Age Group** | ![Total Billing by Age Group](Project%20Screenshots/Total%20Billing%20Amount%20by%20Age%20group.png) |
| 🧍‍♀️ **Total Billing by Gender** | ![Total Billing by Gender](Project%20Screenshots/Total%20Billing%20Amount%20by%20Gender.png) |

---

## 🩺 Key Insights  

1. **Age Distribution:**  
   Most patients fall within the **20–80 age range**.

2. **Billing by Age Group:**  
   The **20–30 age group** contributes the **highest billing (~₹9 crore)**, while **10–20** records the **lowest (~₹2.5 crore)**.

3. **Seasonal Trends:**  
   A **billing surge** occurs between **October–November** every year, likely due to **seasonal illnesses**.  
   Another **major spike appears post-April 2024**.

4. **Cancer Patient Blood Types:**  
   Common among **cancer patients** are **AB−, B+, and B−**.

5. **Obesity & Billing:**  
   **Obesity** cases show the **highest average billing amount**, implying higher treatment costs.

6. **Short Stays, High Bills:**  
   Some patients with **short hospital stays** still incurred **high total bills**, possibly for **intensive procedures**.

7. **Diabetes Probability:**  
   **Diabetes likelihood increases** significantly **after age 30**.

8. **Yearly Billing Comparison:**  
   **2020** shows both the **highest billing total** and **patient volume**.

9. **Insurance Insights:**  
   While differences are minimal, **Medicare** covers the **most patients**.
   
---

## 👨‍🏫 Guided By  
**[The RD Group of Industry](https://github.com/TheRDGroupOfIndustries)**  

---

## 🏷️ Contributors  
- [Nandini](https://github.com/nandiniarjun03) — Data Cleaning  
- **[me](https://github.com/Himanshu76-DA)** — Exploratory Data Analysis & Visualization  
