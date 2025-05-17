from fastapi import FastAPI, Response
from pydantic import BaseModel, Field 
from typing import List, Optional
import statistics
import numpy as np
import matplotlib.pyplot as plt
import io
import scipy.stats as stats
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Welcome to the spectral API"}

@app.get("/hello/{name}")
def greet_user(name: str):
    return {"message": f"Hello, {name}! Welcome to the Spectral API."}

class DataInput(BaseModel):
    values: List[float]
    weights: Optional[list[float]]=Field(None, description="Optional weights for weighted average")


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
