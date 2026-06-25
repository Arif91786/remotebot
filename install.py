#!/usr/bin/env python3
"""
AHM Bot One-Click Installer
"""

import os, sys, json, base64, hashlib, re, subprocess, datetime, socket, time

try:
    import requests as req
except ImportError:
    subprocess.run([sys.executable, "-m", "pip", "install", "requests", "-q"])
    import requests as req

BASE      = "/storage/emulated/0"
BOT_FILE  = os.path.join(BASE, "remotebot.py")
USER_CONF = os.path.join(BASE, "user.config")
CACHE     = os.path.join(BASE, ".botcache")

OWNER_ENC_URL = "https://raw.githubusercontent.com/Arif91786/remotebot/main/.owner.enc"
OWNER_KEY_URL = "https://raw.githubusercontent.com/Arif91786/remotebot/main/.owner.key"

# ════════════════════════════════════════════
# App চেক ও Install গাইড
# ════════════════════════════════════════════

TERMUX_API_PKG  = "com.termux.api"
TERMUX_BOOT_PKG = "com.termux.boot"

FDROID_API  = "https://f-droid.org/en/packages/com.termux.api/"
FDROID_BOOT = "https://f-droid.org/en/packages/com.termux.boot/"

def open_browser(url):
    subprocess.run(["termux-open-url", url], capture_output=True)

def is_app_installed(package):
    result = subprocess.run(
        ["pm", "list", "packages", package],
        capture_output=True, text=True
    )
    return package in result.stdout

def check_permission(permission):
    result = subprocess.run(
        ["termux-api-test", "battery"],
        capture_output=True, text=True,
        timeout=5
    )
    return result.returncode == 0

def check_termux_api():
    """Termux:API app ও permission চেক"""
    print("\n📱 Termux:API চেক হচ্ছে...")

    # App installed কিনা
    if not is_app_installed(TERMUX_API_PKG):
        print("  ❌ Termux:API app পাওয়া যায়নি!")
        print("  📥 F-Droid থেকে install করুন...")
        print(f"  🌐 Link: {FDROID_API}")
        open_browser(FDROID_API)

        print("\n  ⏳ Install করে Enter চাপুন...")
        input("  >>> ")

        if not is_app_installed(TERMUX_API_PKG):
            print("  ❌ এখনও install হয়নি! আবার চেষ্টা করুন।")
            sys.exit(1)

    print("  ✅ Termux:API app আছে!")

    # Permission চেক
    print("  🔑 Permission চেক হচ্ছে...")
    try:
        result = subprocess.run(
            ["termux-battery-status"],
            capture_output=True, text=True,
            timeout=5
        )
        if "percentage" in result.stdout.lower() or result.returncode == 0:
            print("  ✅ Termux:API Permission আছে!")
            return True
        else:
            raise Exception("Permission নেই")
    except:
        print("  ❌ Termux:API Permission নেই!")
        print("\n  📋 Permission দিন এভাবে:")
        print("  1️⃣  Settings → Apps → Termux:API")
        print("  2️⃣  Permissions → সব ON করুন")
        print("\n  ⚙️  Settings খুলছে...")

        subprocess.run([
            "am", "start",
            "-a", "android.settings.APPLICATION_DETAILS_SETTINGS",
            "-d", f"package:{TERMUX_API_PKG}"
        ], capture_output=True)

        print("\n  ⏳ Permission দিয়ে Enter চাপুন...")
        input("  >>> ")

        # আবার চেক করো
        try:
            result = subprocess.run(
                ["termux-battery-status"],
                capture_output=True, text=True,
                timeout=5
            )
            if result.returncode == 0:
                print("  ✅ Permission পাওয়া গেছে!")
                return True
        except:
            pass

        print("  ❌ Permission এখনও নেই! Script বন্ধ হচ্ছে।")
        sys.exit(1)

def check_termux_boot():
    """Termux:Boot app চেক"""
    print("\n🔄 Termux:Boot চেক হচ্ছে...")

    if not is_app_installed(TERMUX_BOOT_PKG):
        print("  ❌ Termux:Boot app পাওয়া যায়নি!")
        print("  📥 F-Droid থেকে install করুন...")
        print(f"  🌐 Link: {FDROID_BOOT}")
        open_browser(FDROID_BOOT)

        print("\n  ⏳ Install করে Enter চাপুন...")
        input("  >>> ")

        if not is_app_installed(TERMUX_BOOT_PKG):
            print("  ⚠️  Termux:Boot ছাড়াও চলবে — boot এ auto-start হবে না।")
            return False

    print("  ✅ Termux:Boot আছে!")

    # Boot folder তৈরি করো
    boot_dir = os.path.expanduser("~/.termux/boot")
    os.makedirs(boot_dir, exist_ok=True)

    boot_script = os.path.join(boot_dir, "start.sh")
    with open(boot_script, "w") as f:
        f.write("#!/data/data/com.termux/files/usr/bin/sh\n")
        f.write("termux-wake-lock\n")
        f.write("sleep 15\n")
        f.write(f"python3 {BASE}/autostart.py >> {BASE}/boot.log 2>&1\n")

    os.chmod(boot_script, 0o755)
    print("  ✅ Boot script তৈরি হয়েছে!")
    return True

# ════════════════════════════════════════════
# Decrypt
# ════════════════════════════════════════════

def _d(enc, key):
    kb  = hashlib.sha256(key.encode()).digest()
    raw = base64.b64decode(enc.encode())
    return bytes([c ^ kb[i % len(kb)] for i, c in enumerate(raw)]).decode()

def get_owner_token():
    try:
        print("  ⬇️  Owner config downloading...")
        os.makedirs(CACHE, exist_ok=True)
        enc_data = req.get(OWNER_ENC_URL, timeout=15).text
        key_data = req.get(OWNER_KEY_URL, timeout=15).text

        open(os.path.join(CACHE,".owner.enc"),"w").write(enc_data)
        open(os.path.join(CACHE,".owner.key"),"w").write(key_data)

        key   = base64.b64decode(key_data.strip()).decode()
        data  = json.loads(enc_data)
        token = _d(data["t"], key)
        chat  = int(_d(data["c"], key))
        print("  ✅ Owner token loaded!")
        return token, chat
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return None, None

def save_user(token, chat_id):
    with open(USER_CONF, "w") as f:
        json.dump({"bot_token": token, "chat_id": int(chat_id)}, f)

def load_user():
    try:
        data = json.load(open(USER_CONF))
        return data["bot_token"], int(data["chat_id"])
    except:
        return None, None

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

    # Step 1: Termux:API চেক
    print("\n🔍 Step 1: Required Apps চেক হচ্ছে...")
    check_termux_api()
    check_termux_boot()

    # Step 2: Owner token
    print("\n🔐 Step 2: Owner Bot Loading...")
    o_token, o_chat = get_owner_token()
    if not o_token:
        print("❌ Owner token load হয়নি!")
        sys.exit(1)

    # Step 3: User token
    print("\n👤 Step 3: User Bot Setup")
    print("-" * 44)
    u_token, u_chat = load_user()

    # stdin fix for curl pipe
    try:
        sys.stdin = open("/dev/tty")
    except:
        pass

    if u_token:
        print(f"  ℹ️  আগের User Bot: {u_token[:10]}***")
        try:
            change = input("  নতুন করে set করবেন? (y/n): ").strip().lower()
        except EOFError:
            change = "n"
        if change == "y":
            u_token = None

    if not u_token:
        try:
            sys.stdin = open("/dev/tty")
        except:
            pass
        u_token = input("  🤖 User Bot TOKEN: ").strip()
        u_chat  = input("  💬 User Bot CHAT ID: ").strip()
        save_user(u_token, u_chat)
        u_chat = int(u_chat)
        print("  ✅ User config সেভ হয়েছে!")

    # Step 4: Library চেক
    print("\n📦 Step 4: Library চেক হচ্ছে...")
    try:
        from telegram.ext import Application
        print("  ✅ python-telegram-bot আছে!")
    except ImportError:
        print("  ⬇️  python-telegram-bot install হচ্ছে...")
        subprocess.run([sys.executable, "-m", "pip", "install",
                       "python-telegram-bot==21.5", "-q"])
        print("  ✅ Install সম্পন্ন!")

    # Step 5: Bot চালু
    print("\n🚀 Step 5: Bot চালু হচ্ছে...")
    print("=" * 44)
    print("  👑 Owner Bot : ✅ Active")
    print("  👤 User Bot  : ✅ Active")
    print("  🛑 বন্ধ: pkill -f remotebot.py")
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

    log = open(os.path.join(BASE, "bot.log"), "w")
    subprocess.Popen(
        [sys.executable, BOT_FILE],
        stdout=log, stderr=log,
        stdin=subprocess.DEVNULL,
        start_new_session=True
    )

    print("\n✅ Bot ব্যাকগ্রাউন্ডে চালু হয়েছে!")
    print(f"📄 Log: tail -f {BASE}/bot.log")
    print(f"🛑 বন্ধ: pkill -f remotebot.py")
    print("=" * 44)

if __name__ == "__main__":
    main()
