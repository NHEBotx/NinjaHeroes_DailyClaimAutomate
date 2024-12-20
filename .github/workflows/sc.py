name: KageHero Claim Bot

on:
  schedule:
    - cron: "0 */6 * * *"  # Menjalankan setiap 6 jam
  workflow_dispatch:  # Menambahkan trigger manual jika ingin menjalankan kapan saja

jobs:
  claim_event:
    runs-on: ubuntu-latest

    steps:
    - name: Checkout repository
      uses: actions/checkout@v2

    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.x'

    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt

    - name: Download geckodriver
      run: |
        sudo apt-get update
        sudo apt-get install -y wget
        wget https://github.com/mozilla/geckodriver/releases/download/v0.30.0/geckodriver-v0.30.0-linux64.tar.gz
        tar -xvzf geckodriver-v0.30.0-linux64.tar.gz
        sudo mv geckodriver /usr/local/bin/

    - name: Run the claim script
      run: |
        python sc.py
