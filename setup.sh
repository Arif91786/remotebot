#!/data/data/com.termux/files/usr/bin/bash
pkg update -y && pkg install python git -y
git clone https://github.com/Arif91786/remotebot.git
cd remotebot
pip install requests python-telegram-bot==21.5 -q
python3 install.py
