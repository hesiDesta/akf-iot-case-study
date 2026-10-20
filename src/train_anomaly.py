"""Deteksi anomali sensor dengan IsolationForest + fitur rolling window.
Dijalankan sebagai job batch di HPC (lihat slurm/train.slurm)."""
import pandas as pd, numpy as np, joblib, os, argparse
from sklearn.ensemble import IsolationForest
from sklearn.metrics import classification_report

def features(df):
    out = []
    for _, g in df.sort_values("ts").groupby("node"):
        g = g.copy()
        for c in ["temp", "hum", "soil"]:
            g[f"{c}_mean"] = g[c].rolling(6, min_periods=1).mean()
            g[f"{c}_std"] = g[c].rolling(6, min_periods=1).std().fillna(0)
            g[f"{c}_diff"] = g[c].diff().fillna(0)
        out.append(g)
    return pd.concat(out)

def main(path, n_jobs):
    df = features(pd.read_csv(path))
    cols = [c for c in df.columns if c not in ("ts", "node", "anomaly")]
    split = int(len(df) * 0.7)
    train, test = df.iloc[:split], df.iloc[split:]
    model = IsolationForest(n_estimators=300, contamination=0.03,
                            n_jobs=n_jobs, random_state=42).fit(train[cols])
    pred = (model.predict(test[cols]) == -1).astype(int)
    print(classification_report(test["anomaly"], pred, digits=3))
    os.makedirs("models", exist_ok=True)
    joblib.dump(model, "models/isoforest.joblib")

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--data", default="data/sensors_anon.csv")
    p.add_argument("--n_jobs", type=int, default=-1)
    a = p.parse_args(); main(a.data, a.n_jobs)
