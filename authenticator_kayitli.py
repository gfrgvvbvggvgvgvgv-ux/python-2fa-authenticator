import tkinter as tk
import tkinter.ttk as ttk
import time, hmac, hashlib, base64, struct, urllib.parse, json, os

FILENAME = "accounts.json"
ACCOUNTS = {}

# -------- LOAD / SAVE --------
def load_accounts():
    global ACCOUNTS
    if os.path.exists(FILENAME):
        try:
            with open(FILENAME, "r", encoding="utf-8") as f:
                ACCOUNTS = json.load(f)
        except:
            ACCOUNTS = {}

def save_accounts():
    with open(FILENAME, "w", encoding="utf-8") as f:
        json.dump(ACCOUNTS, f, indent=2)

# -------- TOTP --------
def totp(secret):
    key = base64.b32decode(secret, casefold=True)
    counter = int(time.time()) // 30
    msg = struct.pack(">Q", counter)
    h = hmac.new(key, msg, hashlib.sha1).digest()
    o = h[-1] & 0x0F
    binary = struct.unpack(">I", h[o:o+4])[0] & 0x7FFFFFFF
    return f"{binary % 1000000:06d}"

# -------- QR LINK PARSE --------
def parse(uri):
    if not uri.startswith("otpauth://"):
        return None, None
    p = urllib.parse.urlparse(uri)
    q = urllib.parse.parse_qs(p.query)
    secret = q.get("secret", [None])[0]
    label = urllib.parse.unquote(p.path.replace("/totp/", ""))
    return label, secret

# -------- ADD --------
def add_account():
    uri = entry.get().strip()
    name, secret = parse(uri)
    if name and secret:
        ACCOUNTS[name] = secret
        save_accounts()
        combo["values"] = list(ACCOUNTS.keys())
        selected.set(name)
        entry.delete(0, tk.END)
        status.config(text="✔ Hesap kaydedildi")
    else:
        status.config(text="✖ Geçersiz QR içeriği")

# -------- UPDATE --------
def update():
    if selected.get() in ACCOUNTS:
        code.config(text=totp(ACCOUNTS[selected.get()]))
        rem = 30 - (int(time.time()) % 30)
        timer.config(text=f"Kalan süre: {rem} sn")
        bar["value"] = rem
    root.after(1000, update)

# -------- GUI --------
load_accounts()

root = tk.Tk()
root.title("Authenticator")
root.geometry("440x380")
root.resizable(False, False)

tk.Label(root, text="QR Link (otpauth://...)").pack(pady=6)
entry = tk.Entry(root, width=60)
entry.pack()
tk.Button(root, text="➕ Hesap Ekle", command=add_account).pack(pady=6)
status = tk.Label(root)
status.pack()

selected = tk.StringVar()
combo = ttk.Combobox(root, textvariable=selected, state="readonly", width=48)
combo["values"] = list(ACCOUNTS.keys())
if ACCOUNTS:
    selected.set(list(ACCOUNTS.keys())[0])
combo.pack(pady=6)

code = tk.Label(root, text="------", font=("Consolas", 32))
code.pack(pady=10)

timer = tk.Label(root)
timer.pack()

bar = ttk.Progressbar(root, maximum=30, length=330)
bar.pack(pady=10)

update()
root.mainloop()
