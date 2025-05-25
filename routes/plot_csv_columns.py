from fastapi import APIRouter, UploadFile, File, Form, Response
import pandas as pd
import matplotlib.pyplot as plt
import io

router = APIRouter()

@router.post("/plot-csv-column")
async def plot_csv_column(
    file: UploadFile = File(...),
    column_name: str = Form(...)
):
    df = pd.read_csv(file.file)

    if column_name not in df.columns:
        return {"error": f"Column '{column_name}' not found."}

    if not pd.api.types.is_numeric_dtype(df[column_name]):
        return {"error": f"Column '{column_name}' is not numeric."}

    plt.figure(figsize=(6, 4))
    plt.plot(df[column_name], marker='o', linestyle='-')
    plt.title(f"Line Chart of '{column_name}'")
    plt.xlabel("Index")
    plt.ylabel(column_name)

    buf = io.BytesIO()
    plt.tight_layout()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)

    return Response(content=buf.read(), media_type="image/png")
