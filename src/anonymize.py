"""Anonimisasi sebelum data masuk HPC (sejalan dengan kewajiban UU PDP di AKF).
node ID -> hash bergaram; kolom lokasi/identitas dibuang."""
import pandas as pd, hashlib, sys

SALT = "ganti-salt-ini"  # simpan di luar repo (env var) pada penggunaan nyata
DROP = ["lat", "lon", "owner", "address"]

def anonymize(src, dst):
    df = pd.read_csv(src)
    df = df.drop(columns=[c for c in DROP if c in df.columns])
    df["node"] = df["node"].map(lambda x: hashlib.sha256((SALT + x).encode()).hexdigest()[:10])
    df.to_csv(dst, index=False)
    print(f"anonymized -> {dst}")

if __name__ == "__main__":
    anonymize(sys.argv[1], sys.argv[2])
