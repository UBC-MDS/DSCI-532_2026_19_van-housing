from pathlib import Path
import pandas as pd

# repo root = parent of src/
ROOT = Path(__file__).resolve().parent.parent

csv_path = ROOT / "data" / "raw" / "non-market-housing.csv"
parquet_path = ROOT / "data" / "processed" / "non-market-housing.parquet"

print("Reading from:", csv_path)
print("Saving to:", parquet_path)

df = pd.read_csv(csv_path, sep=";", low_memory=False)

parquet_path.parent.mkdir(parents=True, exist_ok=True)
df.to_parquet(parquet_path, index=False)

print("Done.")
print("Shape:", df.shape)