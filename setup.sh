#!/data/data/com.termux/files/usr/bin/bash
pkg update -y && pkg install python git -y

# আগের folder থাকলে মুছো
rm -rf ~/remotebot

git clone https://github.com/Arif91786/remotebot.git ~/remotebot
cd ~/remotebot
pip install requests python-telegram-bot==21.5 -q

# stdin ঠিক করে চালাও
python3 install.py < /dev/tty
