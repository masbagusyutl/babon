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
        
        two_hour_seconds = 2 * 60 * 60
        daily_task_seconds = time_until_next_7am_wib()
        
        while two_hour_seconds > 0 or daily_task_seconds > 0:
            now = datetime.now(timezone.utc).astimezone(timezone(timedelta(hours=7)))
            formatted_two_hour = format_seconds(two_hour_seconds)
            formatted_daily_task = format_seconds(daily_task_seconds)
            current_time = now.strftime('%H:%M:%S WIB')
            
            print(f"Waktu tersisa untuk memulai ulang: {formatted_two_hour}", end='\r')
            print(f"Saat ini juga masih menunggu tugas harian pada jam 7 WIB")
            print(f"Waktu tersisa untuk tugas harian: {formatted_daily_task}", end='\r')
            print(f"Jam saat ini: {current_time}", end='\r')
            
            time.sleep(1)
            two_hour_seconds -= 1
            daily_task_seconds -= 1
            
        print("\n")  # Newline after countdown is complete

# Fungsi untuk menjalankan tugas harian pada jam 7 WIB
def run_daily_tasks_at_7(params):
    while True:
        now = datetime.now(timezone.utc).astimezone(timezone(timedelta(hours=7)))  # Waktu WIB
        next_run = now.replace(hour=7, minute=0, second=0, microsecond=0)
        if now > next_run:
            next_run += timedelta(days=1)
        countdown((next_run - now).seconds)

        for i, param in enumerate(params):
            print(f"Memproses akun {i + 1} dari {len(params)}")
            claim_daily_reward(base_claim_daily_url + param)
            claim_daily_combo_reward(base_claim_daily_combo_url + param)
        
        print("Semua akun sudah diproses untuk tugas harian. Menunggu hingga jam 7 WIB berikutnya...")
        countdown(24 * 60 * 60)  # 24 jam dalam detik

# Fungsi untuk hitung mundur
def countdown(seconds):
    while seconds:
        mins, secs = divmod(seconds, 60)
        hours, mins = divmod(mins, 60)
        timeformat = '{:02d}:{:02d}:{:02d}'.format(hours, mins, secs)
        print(f"Waktu tersisa: {timeformat}", end='\r')
        time.sleep(1)
        seconds -= 1
    print()  # Newline after countdown is complete

# Fungsi untuk menghitung waktu hingga jam 7 WIB berikutnya
def time_until_next_7am_wib():
    now = datetime.now(timezone.utc).astimezone(timezone(timedelta(hours=7)))  # Waktu WIB
    next_run = now.replace(hour=7, minute=0, second=0, microsecond=0)
    if now > next_run:
        next_run += timedelta(days=1)
    return (next_run - now).seconds

# Fungsi untuk format detik menjadi jam:menit:detik
def format_seconds(seconds):
    mins, secs = divmod(seconds, 60)
    hours, mins = divmod(mins, 60)
    return '{:02d}:{:02d}:{:02d}'.format(hours, mins, secs)

# Main function
if __name__ == "__main__":
    file_path = 'data.txt'  # Ganti dengan path yang sesuai
    params = read_params_from_file(file_path)

    # Menjalankan tugas setiap 2 jam dalam thread terpisah
    import threading
    threading.Thread(target=run_tasks_every_2_hours, args=(params,)).start()

    # Menjalankan tugas harian pada jam 7 WIB
    run_daily_tasks_at_7(params)
