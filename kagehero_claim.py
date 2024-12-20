import os
import json
import requests
import platform
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options
from pathlib import Path

# Konstanta dan URL
ROOT = Path(__file__).parent
SYSTEM = platform.system()

LOGIN_URL = 'https://kageherostudio.com/payment/server_.php'
EVENT_URL = 'https://kageherostudio.com/event/?event=daily'
USER_NAME = 'txtuserid'
PASS_NAME = 'txtpassword'
SRVR_POST = 'selserver'
REWARD_CLS = '.reward-star'

# Telegram Bot credentials
TELEGRAM_BOT_TOKEN = "7518490579:AAFDdbjyO4u1L24ke76e_VSDUor-eAqkZgY"
TELEGRAM_CHAT_ID = "7997521757"

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

# GeckoDriver Path
GECKODRIVER_PATH = os.path.abspath("./drivers/geckodriver")


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
    """Menyiapkan driver Firefox"""
    validate_geckodriver()
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    service = FirefoxService(GECKODRIVER_PATH)
    try:
        return webdriver.Firefox(service=service, options=options)
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
        send_telegram_message(f"❌ Login gagal untuk {username}")
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
            send_telegram_message(f"🎉 Klaim sukses untuk {username} di server {server}")
        else:
            send_telegram_message(f"⚠️ Tidak ada item bintang untuk {username} di server {server}")
    except Exception as e:
        send_telegram_message(f"❌ Klaim gagal untuk {username} di server {server}. Error: {str(e)}")


def user_claim(account):
    """Melakukan klaim hadiah dengan menggunakan Selenium"""
    username = account.get("username")
    password = account.get("password")
    server = account.get("server")

    driver = setup_driver()
    try:
        send_telegram_message(f"🔄 Memulai klaim untuk {username} di server {server}...")
        if login_event(driver, username, password):
            claim_item(driver, username, server)
    except Exception as e:
        send_telegram_message(f"❌ Terjadi kesalahan: {e}")
    finally:
        driver.quit()


def main():
    """Jalankan klaim hadiah untuk semua akun"""
    send_telegram_message("🚀 Memulai proses klaim harian...")
    for account in DATA_JSON:
        user_claim(account)
    send_telegram_message("✅ Semua klaim telah selesai!")


if __name__ == "__main__":
    main()
