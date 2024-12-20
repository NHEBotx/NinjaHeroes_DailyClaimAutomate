import time
import requests
import json
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Memastikan DATA_JSON tetap utuh seperti yang diberikan
DATA_JSON = [
    {"username": "nhx4@sika3.com", "password": "asd1234", "server": 34},
    {"username": "nhx3@sika3.com", "password": "asd1234", "server": 34},
    {"username": "nhx2@sika3.com", "password": "asd1234", "server": 34},
    {"username": "nhtngx4@gmail.com", "password": "asd1234", "server": 34},
    {"username": "nhtngx3@gmail.com", "password": "asd1234", "server": 34},
    {"username": "nhtngx2@gmail.com", "password": "asd1234", "server": 34},
    {"username": "nhtngx1@gmail.com", "password": "asd1234", "server": 34},
    {"username": "nhx1@sika3.com", "password": "asd1234", "server": 34},
    {"username": "gacor1@gmail.com", "password": "gacor1", "server": 2},
    {"username": "tngxpoolunik@gmail.com", "password": "asd1234", "server": 34},
    {"username": "asd07@sika3.com", "password": "asd1234", "server": 34},
    {"username": "synxx1@sika3.com", "password": "asd1234", "server": 34},
    {"username": "test123@gmail.com", "password": "test123", "server": 1},
    {"username": "asd01@sika3.com", "password": "asd1234", "server": 34},
    {"username": "hantu2@gmail.com", "password": "hantu2", "server": 1},
    {"username": "hantu3@gmail.com", "password": "hantu3", "server": 1},
    {"username": "hantu1@gmail.com", "password": "hantu1", "server": 1},
    {"username": "hantu123@gmail.com", "password": "hantu123", "server": 9},
    {"username": "monyet1@gmail.com", "password": "monyet1", "server": 5},
    {"username": "naruto123@gmail.com", "password": "naruto123", "server": 24}
]

# Mengatur waktu timeout untuk driver
def setup_driver():
    try:
        options = Options()
        options.headless = True  # Menjalankan Firefox dalam mode headless (tanpa UI)

        service = Service("./drivers/geckodriver")  # Path ke GeckoDriver yang sudah diinstal

        # Membuat instance WebDriver
        driver = webdriver.Firefox(service=service, options=options)
        
        # Mengatur timeout untuk driver
        driver.set_page_load_timeout(45)  # Timeout untuk pemuatan halaman (45 detik)
        driver.set_script_timeout(45)  # Timeout untuk eksekusi JavaScript (45 detik)

        return driver
    except Exception as e:
        raise RuntimeError(f"❌ Gagal menginisialisasi WebDriver: {e}")

# Fungsi untuk mengirimkan notifikasi Telegram
def send_telegram_notification(message, bot_token, chat_id):
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        'chat_id': chat_id,
        'text': message,
        'parse_mode': 'Markdown'  # Menggunakan Markdown untuk format teks
    }
    try:
        response = requests.post(url, data=payload)
        response.raise_for_status()  # Memastikan tidak ada error dalam request
    except requests.exceptions.RequestException as e:
        print(f"❌ Gagal mengirim pesan Telegram: {e}")

# Fungsi utama untuk mengklaim akun
def user_claim(account):
    try:
        print(f"📅 Melakukan klaim untuk akun: {account['username']}")
        driver = setup_driver()
        
        # Akses halaman klaim dengan URL yang sesuai
        driver.get("URL_HALAMAN_KLAIM")  # Ganti dengan URL yang relevan
        
        # Tunggu elemen yang diperlukan untuk login (misalnya form login)
        WebDriverWait(driver, 45).until(EC.presence_of_element_located((By.NAME, "username")))
        
        # Lakukan login
        username_input = driver.find_element(By.NAME, "username")
        password_input = driver.find_element(By.NAME, "password")
        username_input.send_keys(account["username"])
        password_input.send_keys(account["password"])
        password_input.send_keys(Keys.RETURN)
        
        # Tunggu halaman setelah login
        WebDriverWait(driver, 45).until(EC.presence_of_element_located((By.NAME, "claim_button")))  # Sesuaikan elemen

        # Klik tombol klaim
        claim_button = driver.find_element(By.NAME, "claim_button")
        claim_button.click()

        # Menunggu hingga klaim selesai
        WebDriverWait(driver, 45).until(EC.presence_of_element_located((By.NAME, "claim_success_message")))  # Sesuaikan elemen

        # Dapatkan item yang diklaim
        claimed_item = driver.find_element(By.NAME, "claimed_item").text  # Sesuaikan elemen
        claim_time = time.strftime("%H:%M:%S", time.localtime())  # Mendapatkan waktu klaim

        # Menyiapkan pesan notifikasi
        message = f"✨ Klaim Berhasil ✨\n\nUsername: *{account['username']}*\nItem: *{claimed_item}*\nWaktu Klaim: *{claim_time}*\nServer: *{account['server']}*"
        
        # Kirim notifikasi Telegram
        send_telegram_notification(message, "YOUR_BOT_TOKEN", "YOUR_CHAT_ID")  # Ganti dengan token dan chat ID

        driver.quit()  # Tutup driver setelah klaim selesai

    except Exception as e:
        print(f"❌ Terjadi kesalahan saat melakukan klaim: {e}")
        driver.quit()  # Tutup driver jika terjadi error

# Main program untuk mengklaim setiap akun dalam DATA_JSON
def main():
    for account in DATA_JSON:
        user_claim(account)

if __name__ == "__main__":
    main()
