"""Simulasi data sensor IoT (suhu, kelembapan, soil moisture) + anomali.
Dipakai kalau belum ada hardware. Output: data/sensors.csv"""
import numpy as np, pandas as pd, argparse, os

def main(nodes, days, seed):
    rng = np.random.default_rng(seed)
    idx = pd.date_range("2026-01-01", periods=days * 24 * 12, freq="5min")
    frames = []
    for n in range(nodes):
        hour = np.asarray(idx.hour + idx.minute / 60, dtype=float)
        temp = 27 + 4 * np.sin((hour - 9) / 24 * 2 * np.pi) + rng.normal(0, .4, len(idx))
        hum = 75 - 10 * np.sin((hour - 9) / 24 * 2 * np.pi) + rng.normal(0, 1.5, len(idx))
        soil = 600 + rng.normal(0, 15, len(idx)) - (np.arange(len(idx)) % 2000) * 0.1
        label = np.zeros(len(idx), dtype=int)
        for s in rng.choice(len(idx) - 30, size=len(idx) // 800, replace=False):
            temp[s:s+12] += rng.uniform(6, 10)   # anomali: lonjakan suhu
            hum[s:s+12] -= rng.uniform(15, 25)
            label[s:s+12] = 1
        frames.append(pd.DataFrame({"ts": idx, "node": f"node-{n+1:02d}",
                                    "temp": temp, "hum": hum, "soil": soil, "anomaly": label}))
    os.makedirs("data", exist_ok=True)
    pd.concat(frames).to_csv("data/sensors.csv", index=False)
    print("saved data/sensors.csv")

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--nodes", type=int, default=5)
    p.add_argument("--days", type=int, default=60)
    p.add_argument("--seed", type=int, default=42)
    a = p.parse_args(); main(a.nodes, a.days, a.seed)
