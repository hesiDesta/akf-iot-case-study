#!/bin/bash
#SBATCH --job-name=akf-iot-anomaly
#SBATCH --nodes=1
#SBATCH --cpus-per-task=16
#SBATCH --time=01:00:00
#SBATCH --output=slurm-%j.out
# NOTE: sesuaikan partition/modul dengan dokumentasi resmi AKF setelah akun aktif.

module load python  # nama modul bisa berbeda
python src/anonymize.py data/sensors.csv data/sensors_anon.csv
python src/train_anomaly.py --data data/sensors_anon.csv --n_jobs $SLURM_CPUS_PER_TASK
