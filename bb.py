import requests
import time
from datetime import datetime, timedelta, timezone

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

# Fungsi untuk menjalankan tugas setiap 2 jam
def run_tasks_every_2_hours(params):
    while True:
        for i, param in enumerate(params):
            print(f"Memproses akun {i + 1} dari {len(params)}")
            charge_battery(base_charge_battery_url + param)
            repair_fingers(base_repair_fingers_url + param)

        print("Semua akun proses untuk tugas charge battery dan repair finger selesai")
        
        # Mulai countdown untuk 2 jam
        countdown(2 * 60 * 60, "Waktu tersisa untuk memulai ulang: ")

# Fungsi untuk menjalankan tugas harian pada jam 7 WIB
def run_daily_tasks_at_7(params):
    while True:
        next_run = calculate_next_run_7()
        countdown((next_run - datetime.now()).seconds, "Waktu tersisa untuk tugas harian: ")

        for i, param in enumerate(params):
            print(f"Memproses akun {i + 1} dari {len(params)}")
            claim_daily_reward(base_claim_daily_url + param)
            claim_daily_combo_reward(base_claim_daily_combo_url + param)
        
        print("Semua akun sudah diproses untuk tugas harian. Menunggu hingga jam 7 WIB berikutnya...")
        time.sleep(24 * 60 * 60)  # Tunggu 24 jam

# Fungsi untuk hitung mundur dengan pesan tambahan
def countdown(seconds, message):
    while seconds > 0:
        print(f"{message}{seconds} detik", end='\r')
        time.sleep(1)
        seconds -= 1
    print()  # Newline after countdown is complete

# Fungsi untuk menghitung waktu berikutnya jam 7 WIB
def calculate_next_run_7():
    now = datetime.now(timezone.utc).astimezone(timezone(timedelta(hours=7)))  # Waktu WIB
    next_run = now.replace(hour=7, minute=0, second=0, microsecond=0)
    if now > next_run:
        next_run += timedelta(days=1)
    return next_run

# Main function
if __name__ == "__main__":
    file_path = 'data.txt'  # Ganti dengan path yang sesuai
    params = read_params_from_file(file_path)

    while True:
        # Menjalankan tugas setiap 2 jam dalam thread terpisah
        import threading
        threading.Thread(target=run_tasks_every_2_hours, args=(params,)).start()

        # Menjalankan tugas harian pada jam 7 WIB
        run_daily_tasks_at_7(params)
