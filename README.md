# 🔬 Spectral Data API

A FastAPI-based application for analyzing and visualizing scientific datasets.  
Users can submit numeric data and receive statistical summaries or generated plots (e.g., histograms) via an interactive web interface or REST API.

---

## 🚀 Features

- ✅ REST API built with **FastAPI**
- ✅ Interactive API docs using **Swagger UI**
- ✅ POST endpoint for statistical data analysis (`/analyze-data`)
- ✅ POST endpoint for plot generation (`/plot-data`)
- ✅ Simple **frontend** (HTML + JS) to submit data and view plots
- ✅ Handles mean, median, standard deviation, weighted averages, normalization, and more
- ✅ Built-in support for returning plots as PNG images

---

## 🏁 Getting Started

### 🔧 Prerequisites

- Python 3.8 or later
- `pip` for installing packages
- Git (if cloning this repository)

### 📦 Installation

```bash
# Clone the repo (or download manually)
git clone https://github.com/lawanmuk/fastapi-spectral-api.git
cd fastapi-spectral-api

# Create and activate a virtual environment
python -m venv venv
venv\Scripts\activate  

# Install dependencies
pip install -r requirements.txt

