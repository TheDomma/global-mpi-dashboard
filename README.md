# 🌍 Global Multidimensional Poverty Index (MPI) Dashboard

![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge\&logo=Streamlit\&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.9+-blue?style=for-the-badge\&logo=python\&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-239120?style=for-the-badge\&logo=plotly\&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-2C2D72?style=for-the-badge\&logo=pandas\&logoColor=white)

---

## 🚀 Live Application

👉 **Try the dashboard here:**
https://global-mpi-dashboard-ccskfs4zkbvfwdypm4ntq8.streamlit.app/

---

## 📌 Overview

This project presents an interactive data science dashboard analyzing the **Global Multidimensional Poverty Index (MPI)** dataset.

The dashboard is designed to support **data-driven decision-making** by providing clear, interactive insights into global poverty patterns, regional disparities, and underlying drivers of poverty.

Developed as part of the **5DATA004C Data Science Project Lifecycle** coursework, this project aligns with **UN Sustainable Development Goal 1 (SDG 1): End poverty in all its forms everywhere.**

---

## ✨ Key Features

### 💡 Intelligent Insights

* Highlights **high-risk regions**
* Compares selected data with **global averages**
* Provides **causal explanations**, not just visuals

### 🎛️ Interactive Control Panel

* Country and region filters
* Poverty segmentation (Extreme / High / Moderate)
* Dynamic metric selection:

  * MPI
  * Headcount Ratio
  * Intensity of Deprivation
  * Vulnerable & Severe Poverty
* Adjustable thresholds and Top-N filtering

### 🗺️ Geospatial Analysis

* Interactive **choropleth map**
* Multi-metric hover insights

### 📈 Poverty Driver Analysis

* Scatter plots with **OLS regression trendlines**
* Identifies whether poverty is driven by:

  * population affected (headcount)
  * severity of deprivation (intensity)

### 🍰 Risk Segmentation

* Categorizes regions into poverty levels
* Donut chart visualization with insights

### ⚖️ Country Comparison Tool

* Compare two countries side-by-side
* Dynamic indicators and delta comparison

### 📊 Data Exploration

* Sortable dataset table
* Export filtered data to CSV

---

## 📂 Project Structure

```plaintext
global-mpi-dashboard/
│
├── app.py                     # Main Streamlit application
├── cleaned_global_mpi.csv     # Clean dataset used in dashboard
├── data_cleaning.ipynb        # Data preprocessing notebook
├── global_mpi.csv             # Raw dataset
├── metadata-global-mpi...     # Dataset metadata
├── requirements.txt           # Dependencies
├── 2.png                      # Header image
└── README.md                  # Documentation
```

---

## 🚀 Setup & Installation

### 1. Prerequisites

Ensure Python 3.9 or higher is installed:

```bash
python --version
```

---

### 2. Clone the Repository

```bash
git clone https://github.com/TheDomma/global-mpi-dashboard.git
cd global-mpi-dashboard
```

---

### 3. Create Virtual Environment

```bash
python -m venv venv
```

---

### 4. Activate Environment

**Windows (PowerShell):**

```bash
.\venv\Scripts\Activate.ps1
```

**Windows (CMD):**

```bash
venv\Scripts\activate
```

**macOS/Linux:**

```bash
source venv/bin/activate
```

---

### 5. Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 6. Run the Application

```bash
streamlit run app.py
```

Open in browser:
http://localhost:8501/

---

## 🛠️ Technologies Used

* Python
* Streamlit
* Pandas
* Plotly
* Statsmodels
* PyCountry

---

## 🧠 Key Insights Delivered

* Identification of **high-risk poverty regions**
* Understanding **poverty drivers (intensity vs headcount)**
* Regional comparisons for **policy-level decisions**
* Detection of **future vulnerability trends**

---

## ⚠️ Troubleshooting

### PowerShell Execution Policy Error

```bash
Set-ExecutionPolicy Unrestricted -Scope CurrentUser
```

### Module Not Found Error

* Ensure virtual environment is activated `(venv)`
* Reinstall dependencies:

```bash
pip install -r requirements.txt
```

---

## 📬 Author

Developed as part of the
**University of Westminster – Data Science Project Lifecycle (5DATA004C)**

---

## ⭐ Final Note

This dashboard is designed not just to visualize data, but to **transform data into actionable insights** — bridging the gap between analysis and real-world decision-making.
