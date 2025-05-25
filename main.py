from fastapi import FastAPI, Response, UploadFile, File
from pydantic import BaseModel, Field 
from typing import List, Optional
import statistics
import numpy as np
import matplotlib.pyplot as plt
import io, base64
import scipy.stats as stats
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd 
from routes import plot_csv_column  


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(plot_csv_column.router) 

@app.get("/")
def read_root():
    return {"message": "Welcome to the spectral API"}

@app.get("/hello/{name}")
def greet_user(name: str):
    return {"message": f"Hello, {name}! Welcome to the Spectral API."}

class DataInput(BaseModel):
    values: List[float]
    weights: Optional[list[float]]=Field(None, description="Optional weights for weighted average")
    chart_type: Optional[str] = "histogram"
    bins: Optional[int] = Field(10, description="Number of bins for histogram")
    as_base64: Optional[bool] = Field(False, description="Return image as base64 string")

@app.post("/analyse-data")
def analyse_data(data: DataInput):
    values = data.values
    mean_value= sum(values) / len(values) if values else 0
    count = len(values)
    return {"mean": mean_value, "count": count}

@app.post("/analyse-data-2")
def analyse_data_2(data: DataInput):
    values = data.values
    weights = data.weights

    if not values:
        return{"error": "no data provided"}
    
    mean_value= statistics.mean(values)
    median_value = statistics.median(values)
    stdev_values = statistics.stdev(values) if len(values) > 1 else 0
    minimum = min(values)
    maximum = max(values) 
    total_sum = sum(values)
    count = len(values)
    variance = statistics.variance(values) if len(values) > 1 else 0
    mode = statistics.mode(values) if len(set(values)) > 1 else "No unique mode"
    iqr = np.percentile(values, 75) - np.percentile(values, 25)
    skewness = stats.skew(values)
    kurtosis = stats.kurtosis(values)

    

    weighted_avg = None
    if weights and len(weights) == len(values):
        weighted_avg = float(np.average(values, weights=weights))

    #Normalize data.. 
    normalized = [(v - minimum)/ (maximum - minimum) if maximum != minimum else 0 for v in values]
    normalized_zscore = [(v - mean_value) / stdev_values if stdev_values != 0 else 0 for v in values]
    return {"mean": mean_value,
            "median_value": median_value,
            "stdev_values": stdev_values,
            "minimum": minimum,
            "maximum": maximum,
            "total_sum": total_sum,
            "count": count, 
            "weighted_avg": weighted_avg,
            "normalized": normalized,
            "skewness": skewness,
            "kurtosis": kurtosis,
            "normalized_zscore": normalized_zscore
}


@app.post("/plot-data")
def plot_data(data: DataInput):
    values = data.values
    if not values:
        return{"error": "no data provided"}

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    axes[0].hist(values, bins=10, color='skyblue', edgecolor='black')
    axes[0].set_title("Histogram")
    axes[0].set_xlabel("Values")
    axes[0].set_ylabel("Frequency")

    axes[1].boxplot(values, vert=True, patch_artist=True)
    axes[1].set_title("Box Plot")


    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)

    return Response(content=buf.read(), media_type="image/png")


@app.post("/plot-data-histogram")
def plot_data_histogram(data: DataInput):
    values = data.values
    chart_type = data.chart_type
    bins = data.bins or 10
    as_base64 = data.as_base64

    plt.figure(figsize=(6,4))

    if chart_type == "line":
        plt.plot(values, marker='o', linestyle='-', color='blue')
        plt.xlabel("Index")
        plt.ylabel("Value")
    else:
        plt.hist(values, bins=10, color='skyblue', edgecolor='black')
        plt.xlabel("Value")
        plt.ylabel("Frequency")

    buf = io.BytesIO()
    plt.tight_layout()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)

    if as_base64:
        img_str = base64.b64encode(buf.getvalue()).decode('utf-8')
        return {"image_base64": f"data:image/png;base64,{img_str}"}
    else:
        return Response(content=buf.read(), media_type="image/png")

@app.post("/get-csv-columns")
def get_csv_columns(file: UploadFile = File(...)):
    df = pd.read_csv(file.file)
    return {"columns": df.columns.tolist()}
