# 🌍 Global Multidimensional Poverty Index (MPI) Dashboard

![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge\&logo=Streamlit\&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.9+-blue?style=for-the-badge\&logo=python\&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-239120?style=for-the-badge\&logo=plotly\&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-2C2D72?style=for-the-badge\&logo=pandas\&logoColor=white)

---
🚀 Live Demo

👉 Try the dashboard here:
https://global-mpi-dashboard-ccskfs4zkbvfwdypm4ntq8.streamlit.app/
## 📌 Overview

This project presents an interactive data science dashboard analyzing the **Global Multidimensional Poverty Index (MPI)** dataset.

The dashboard is designed to support **high-level decision-making** by providing clear, interactive insights into global poverty patterns, regional disparities, and key poverty drivers.

Developed as part of the **5DATA004C Data Science Project Lifecycle** coursework, this project aligns with **UN Sustainable Development Goal 1 (SDG 1): End poverty in all its forms everywhere.**

---

## ✨ Key Features

### 💡 Intelligent Insights

* Automatically highlights **high-risk regions**
* Compares selected data with **global averages**
* Provides **explanatory insights** (not just visuals)

### 🎛️ Interactive Control Panel

* Country and region filters
* Poverty risk segmentation (Extreme / High / Moderate)
* Dynamic metric selection:

  * MPI
  * Headcount Ratio
  * Intensity of Deprivation
  * Vulnerability & Severe Poverty
* Adjustable thresholds and Top-N selection

### 🗺️ Geospatial Analysis

* Interactive choropleth map showing global poverty distribution
* Hover-based multi-metric insights

### 📈 Poverty Driver Analysis

* Scatter plots with **OLS regression trendlines**
* Identifies whether poverty is driven by:

  * population affected (headcount)
  * severity of deprivation (intensity)

### 🍰 Risk Segmentation

* Classification of regions into poverty levels
* Donut chart visualization with key insights

### ⚖️ Country Comparison Tool

* Compare two countries side-by-side
* Dynamic performance indicators and visual comparison

### 📊 Data Exploration

* Sortable dataset table
* Export filtered data to CSV

---

## 📂 Project Structure

```
global-mpi-dashboard/
│
├── app.py                     # Main Streamlit dashboard
├── cleaned_global_mpi.csv     # Cleaned dataset used in analysis
├── data_cleaning.ipynb        # Data preprocessing & feature engineering
├── global_mpi.csv             # Raw dataset
├── metadata-global-mpi...     # Dataset metadata
├── requirements.txt           # Dependencies
├── 2.png                      # Dashboard header image
└── README.md                  # Project documentation
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

### 4. Activate Virtual Environment

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

```
http://localhost:8501/
```

---

## 🛠️ Technologies Used

* **Python**
* **Streamlit** (Dashboard Framework)
* **Pandas** (Data Processing)
* **Plotly** (Interactive Visualizations)
* **Statsmodels** (Regression Analysis)
* **PyCountry** (Country standardization)

---

## 🧠 Key Insights Delivered

* Identification of **high-risk poverty regions**
* Understanding of **poverty drivers (intensity vs headcount)**
* Regional comparisons supporting **policy-level decisions**
* Detection of **vulnerability trends and future risks**

---

## ⚠️ Troubleshooting

### PowerShell Execution Error (Windows)

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

Developed as part of the **University of Westminster – Data Science Project Lifecycle module (5DATA004C)**.

---

## ⭐ Final Note

This dashboard is designed not just to visualize data, but to **translate data into actionable insight** — bridging the gap between analysis and real-world decision-making.
