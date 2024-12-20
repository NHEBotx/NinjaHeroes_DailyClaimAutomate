import os
import json
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from pathlib import Path
from datetime import datetime

# Konstanta dan URL
ROOT = Path(__file__).parent
LOGIN_URL = 'https://kageherostudio.com/payment/server_.php'
EVENT_URL = 'https://kageherostudio.com/event/?event=daily'
USER_NAME = 'txtuserid'
PASS_NAME = 'txtpassword'
SRVR_POST = 'selserver'
REWARD_CLS = '.reward-star'

# Telegram Bot credentials
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# Data JSON untuk akun
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

# GeckoDriver Path (pastikan path ini sesuai dengan lingkungan Anda, misalnya di GitHub Actions)
GECKODRIVER_PATH = "./drivers/geckodriver"

def send_telegram_message(message, parse_mode="HTML"):
    """Mengirimkan pesan ke Telegram Bot"""
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message, "parse_mode": parse_mode}
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        print("✅ Pesan Telegram berhasil dikirim.")
    except requests.RequestException as e:
        print(f"❌ Gagal mengirim pesan Telegram: {e}")

def validate_geckodriver():
    """Memeriksa apakah GeckoDriver dapat dijalankan"""
    if not os.path.isfile(GECKODRIVER_PATH):
        raise FileNotFoundError(f"❌ GeckoDriver tidak ditemukan di {GECKODRIVER_PATH}")
    if not os.access(GECKODRIVER_PATH, os.X_OK):
        raise PermissionError(f"❌ Tidak ada izin eksekusi untuk GeckoDriver di {GECKODRIVER_PATH}")

def setup_driver():
    """Menyiapkan driver Firefox dengan timeout 45 detik"""
    validate_geckodriver()
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    
    # Menambahkan pengaturan timeout driver
    capabilities = DesiredCapabilities.FIREFOX
    capabilities["marionette"] = True
    service = FirefoxService(GECKODRIVER_PATH)
    try:
        driver = webdriver.Firefox(service=service, options=options, desired_capabilities=capabilities)
        driver.set_page_load_timeout(45)  # Timeout driver 45 detik
        driver.set_script_timeout(45)  # Timeout script 45 detik
        return driver
    except Exception as e:
        raise RuntimeError(f"❌ Gagal menginisialisasi WebDriver: {e}")

def login_event(driver, username, password):
    """Login ke halaman event dengan kredensial yang diberikan"""
    driver.get(EVENT_URL)
    driver.find_element(By.NAME, USER_NAME).send_keys(username)
    driver.find_element(By.NAME, PASS_NAME).send_keys(password)
    driver.find_element(By.NAME, "login").click()
    if "event" in driver.current_url:
        print(f"✅ Login sukses untuk {username}")
        return True
    else:
        print(f"❌ Login gagal untuk {username}")
        send_telegram_message(f"❌ <b>Login gagal</b> untuk akun <b>{username}</b> pada {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        return False

def claim_item(driver, username, server):
    """Melakukan klaim item di halaman event"""
    try:
        driver.find_element(By.NAME, SRVR_POST).send_keys(str(server))
        driver.find_element(By.ID, "claim-button").click()

        # Cari item bertanda bintang
        reward = driver.find_element(By.CSS_SELECTOR, REWARD_CLS)
        if reward:
            reward.click()  # Klik untuk klaim
            driver.find_element(By.XPATH, "//button[text()='OKE']").click()  # Klik OKE di popup
            item_claimed = "Item Bintang"  # Contoh item, bisa disesuaikan jika ada detail lebih lanjut
            send_telegram_message(f"🎉 <b>Klaim sukses</b> untuk akun <b>{username}</b> di server <b>{server}</b> pada {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}.\n\nItem yang diklaim: <b>{item_claimed}</b>")
        else:
            send_telegram_message(f"⚠️ Tidak ada item yang bisa diklaim untuk akun <b>{username}</b> di server <b>{server}</b> pada {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    except Exception as e:
        send_telegram_message(f"❌ <b>Klaim gagal</b> untuk akun <b>{username}</b> di server <b>{server}</b> pada {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}.\n\nError: {str(e)}")

def user_claim(account):
    """Melakukan klaim hadiah dengan menggunakan Selenium"""
    username = account.get("username")
    password = account.get("password")
    server = account.get("server")

    driver = setup_driver()
    try:
        send_telegram_message(f"🔄 Memulai klaim untuk akun <b>{username}</b> di server <b>{server}</b> pada {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}...")
        if login_event(driver, username, password):
            claim_item(driver, username, server)
    except Exception as e:
        send_telegram_message(f"❌ Terjadi kesalahan: {e}")
    finally:
        driver.quit()

def main():
    """Jalankan klaim hadiah untuk semua akun"""
    send_telegram_message(f"🚀 <b>Memulai proses klaim harian</b> pada {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}...")
    for account in DATA_JSON:
        user_claim(account)
    send_telegram_message(f"✅ <b>Semua klaim telah selesai!</b> pada {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    main()
