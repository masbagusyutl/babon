import requests
import time
from datetime import datetime, timedelta

# URL dasar untuk pengisian energi, klaim hadiah harian, klaim hadiah combo harian, dan perbaikan jari
base_charge_battery_url = "https://baboon-telegram.onrender.com/game/chargeBattery?tgInitData="
base_claim_daily_url = "https://baboon-telegram.onrender.com/game/claimDailyLoginReward?tgInitData="
base_claim_daily_combo_url = "https://baboon-telegram.onrender.com/game/claimDailyComboReward?tgInitData="
base_repair_fingers_url = "https://baboon-telegram.onrender.com/game/repairFingers?tgInitData="

# Header untuk permintaan HTTP
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0"
}

# Payload untuk pengisian energi
charge_payload = {
    "tapsNumber": 26
}

# Payload untuk klaim hadiah combo harian
combo_payload = {
    "battery1": 93.701171875,
    "battery2": 93.896484375,
    "battery3": 98.126953125
}

# Payload untuk perbaikan jari
repair_payload = {
    "fingersToRepair": 14,
    "price": 1.4000000000000001
}

# Fungsi untuk mengisi energi
def charge_battery(url):
    response = requests.post(url, headers=headers, json=charge_payload)
    if response.status_code == 201:
        print(f"Charged battery: {response.status_code}")
    else:
        print(f"Failed to charge battery: {response.status_code}")
    time.sleep(5)  # Jeda 5 detik

# Fungsi untuk klaim hadiah harian
def claim_daily_reward(url):
    response = requests.post(url, headers=headers)
    if response.status_code == 201:
        print(f"Claimed daily reward: {response.status_code}")
    else:
        print(f"Failed to claim daily reward: {response.status_code}")

# Fungsi untuk klaim hadiah combo harian
def claim_daily_combo_reward(url):
    response = requests.post(url, headers=headers, json=combo_payload)
    if response.status_code == 201:
        print(f"Claimed daily combo reward: {response.status_code}")
    else:
        print(f"Failed to claim daily combo reward: {response.status_code}")

# Fungsi untuk memperbaiki jari
def repair_fingers(url):
    response = requests.post(url, headers=headers, json=repair_payload)
    if response.status_code == 201:
        print(f"Repaired fingers: {response.status_code}")
    else:
        print(f"Failed to repair fingers: {response.status_code}")

# Fungsi untuk membaca parameter URL dari file
def read_params_from_file(file_path):
    with open(file_path, 'r') as file:
        params = file.readlines()
    return [param.strip() for param in params]

# Fungsi untuk menjalankan tugas setiap 14 jam
