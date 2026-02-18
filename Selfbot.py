# -*- coding: utf-8 -*-
# 3UVH DARK HACKER SELF-BOT - VERSION 2026
# Librairie : discord.py-self (git+https://github.com/dolfies/discord.py-self.git)

import discord
from discord.ext import commands
import asyncio
import json
import os
import random
import string
import requests
from datetime import datetime

# ==============================================================
# CONFIGURATION
# ==============================================================

TOKEN = "OTA5MTkzNDkyNTM2OTA1NzM4.GIYrF3.dcMhNxYJ8rvZx7J_44W5R32S2pQYxF_5n52jpE"  # ← Ton token (change-le souvent !)

COMMAND_PREFIX = "&"
DM_USERNAME_PREFIX = "@!old "

HISTORY_FILE = "old_usernames.json"

STREAM_IMAGE_URL = "https://cdn.discordapp.com/attachments/.../3uvh_neon_dark_hacker.png"  # ← URL DIRECTE de ton image

ROTATION_INTERVAL = 20  # 2 minutes

HEADERS = {
    "Authorization": TOKEN,
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

CUSTOM_STATUS_LIST = [
    "Angelina my wife "
    "Angelina my only love" 
    "VOID://ROOT ACCESS GRANTED",
    "0xDEADBEEF injected • corrupted",
    "Kernel panic • enjoy the crash",
    "sudo rm -rf /reality",
    "Backdoor open 24/7",
    "Firewall = NULL",
    "Ghost in the shell • ACTIVE",
    "Encrypted soul leaking",
    "Matrix overflow • 404",
    "Red pill swallowed • awake",
    "Neon shadows watching",
    "Terminal.exe running...",
    "Data breach imminent",
    "Null pointer reality",
    "Darknet heartbeat",
    "Cipher self-destruct",
    "Abyss staring back",
    "Binary blood dripping",
    "Shadow root granted",
    "Glitchcore eternal • corrupted"
]

STREAMING_BASE_TEXTS = [
    "VOID BREACH INITIATED",
    "0x1337 SYSTEM OWNED",
    "GHOST PROTOCOL ACTIVE",
    "ENCRYPTED VOID LOOP",
    "NEON HACK PROTOCOL",
    "KERNEL VOID LOADING",
    "GLITCH REALITY DETECTED",
    "CYBER ABYSS ONLINE",
    "MATRIX TERMINAL BREACHED",
    "3UVH ROOT ACCESS"
]

# ==============================================================
# UTILS
# ==============================================================

GLITCH_CHARS = ['̸','̶','̵','͛','͝','͞','͟','͢','̴','̷','█','▒','░']

def glitch_text(text, intensity=0.75):
    result = ""
    for char in text:
        if random.random() < intensity:
            glitch = random.choice(GLITCH_CHARS)
            result += char + glitch if random.random() < 0.5 else glitch + char
        else:
            result += char
        if random.random() < 0.18:
            result += random.choice(['ERROR','404','0x','NULL','VOID','█'])
    if random.random() < 0.55:
        result = random.choice(["//","ERR_","VOID//","0x"]) + result
    if random.random() < 0.55:
        result += random.choice([".exe","̸̸","NULL","█"])
    return result

def set_custom_status(text):
    payload = {
        "custom_status": {"text": text, "expires_at": None, "emoji_id": None, "emoji_name": None},
        "status": "dnd"
    }
    try:
        r = requests.patch("https://discord.com/api/v9/users/@me/settings", headers=HEADERS, json=payload)
        if r.status_code == 200:
            print(f"[CUSTOM] {text}")
        else:
            print(f"[CUSTOM ERR] {r.status_code} {r.text[:100]}")
    except Exception as e:
        print(f"[CUSTOM FAIL] {e}")

# ==============================================================
# HISTORIQUE PSEUDOS
# ==============================================================

name_history = {}
if os.path.exists(HISTORY_FILE):
    try:
        with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
            name_history = json.load(f)
        print(f"[INFO] {len(name_history)} utilisateurs trackés")
    except Exception as e:
        print(f"[ERR LOAD HIST] {e}")
        name_history = {}
else:
    print("[INFO] Nouveau fichier historique créé")

def save_history():
    try:
        with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
            json.dump(name_history, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"[ERR SAVE HIST] {e}")

# ==============================================================
# BOT
# ==============================================================

bot = commands.Bot(
    command_prefix=COMMAND_PREFIX,
    self_bot=True,
    help_command=None
)

@bot.event
async def on_ready():
    print(f"[ON] Connecté → {bot.user} ({bot.user.id})")

    activity = discord.Streaming(
        name=random.choice(STREAMING_BASE_TEXTS),
        url=STREAM_IMAGE_URL
    )
    await bot.change_presence(status=discord.Status.dnd, activity=activity)
    print(f"[INIT STREAM] {activity.name}")

    set_custom_status(random.choice(CUSTOM_STATUS_LIST))

    bot.loop.create_task(status_rotation())

async def status_rotation():
    while True:
        new_custom = random.choice(CUSTOM_STATUS_LIST)
        set_custom_status(new_custom)

        base = random.choice(STREAMING_BASE_TEXTS)
        glitched = glitch_text(base)
        activity = discord.Streaming(name=glitched, url=STREAM_IMAGE_URL)
        await bot.change_presence(status=discord.Status.dnd, activity=activity)
        print(f"[ROTATION] {glitched}")

        await asyncio.sleep(ROTATION_INTERVAL)

@bot.event
async def on_user_update(before, after):
    old = before.global_name or before.name
    new = after.global_name or after.name
    if old != new:
        uid = str(after.id)
        if uid not in name_history:
            name_history[uid] = []
        name_history[uid].append({"ancien": old, "quand": datetime.utcnow().isoformat()})
        save_history()
        print(f"[PSEUDO CHG] {after} : {old} → {new}")

@bot.event
async def on_message(message):
    if message.content.startswith(DM_USERNAME_PREFIX) and isinstance(message.channel, discord.DMChannel):
        try:
            uid_str = message.content[len(DM_USERNAME_PREFIX):].strip()
            user_id = int(uid_str)

            user = await bot.fetch_user(user_id)
            current = user.global_name or user.name

            if uid_str in name_history and name_history[uid_str]:
                hist = sorted(name_history[uid_str], key=lambda x: x['quand'], reverse=True)
                reply = f"**Anciens pseudos de {current}**\n\n"
                for entry in hist:
                    dt = datetime.fromisoformat(entry['quand'].replace('Z', '+00:00'))
                    reply += f"{dt.strftime('%d/%m/%Y')} - **{entry['ancien']}**\n"
                reply += f"\n**Actuel :** {current}"
            else:
                reply = f"Aucun historique pour {current} (ID {uid_str})"

            await message.channel.send(reply)

        except Exception as e:
            await message.channel.send(f"Erreur : {str(e)[:100]}")

    await bot.process_commands(message)

# ==============================================================
# COMMANDES MENU & GRAB
# ==============================================================

@bot.command()
async def menu(ctx):
    txt = "**3UVH DARK SELF-BOT MENU**\n\n"
    txt += f"Préfixe : {COMMAND_PREFIX}\n\n"
    txt += "&grab_IP <id>   → Fake IP grab\n"
    txt += "&grab_token <id> → Fake token grab\n"
    txt += "&id2roblox <id> → Recherche Roblox liée\n"
    txt += "@!old <id> (en MP) → Anciens pseudos\n\n"
    txt += "Statut rotation auto : actif (dark/neon/glitch)"
    await ctx.send(txt)

@bot.command()
async def grab_IP(ctx, user_id: str = None):
    if not user_id:
        return await ctx.send("Utilisation : &grab_IP <ID>")
    try:
        uid = int(user_id)
        user = await bot.fetch_user(uid)
        name = user.name
        disp = user.display_name or name
    except:
        return await ctx.send("ID invalide ou utilisateur introuvable.")
    ip = ".".join(str(random.randint(1, 255)) for _ in range(4))
    port = random.choice(["80","443","8080"])
    loc = random.choice(["Paris FR","NY US","Tokyo JP","VPN/Tor"])
    e = discord.Embed(title="GRAB IP FAKE SUCCESS", color=0xff0000)
    e.add_field(name="Cible", value=f"{disp} ({name}) - {uid}", inline=False)
    e.add_field(name="IP", value=f"```{ip}:{port}```", inline=False)
    e.add_field(name="Loc", value=f"```{loc}```", inline=False)
    e.set_footer(text="FAKE IP • 3uvh")
    await ctx.send(embed=e)

@bot.command()
async def grab_token(ctx, user_id: str = None):
    if not user_id:
        return await ctx.send("Utilisation : &grab_token <ID>")
    try:
        uid = int(user_id)
        user = await bot.fetch_user(uid)
        name = user.name
        disp = user.display_name or name
    except:
        return await ctx.send("ID invalide ou utilisateur introuvable.")
    p1 = ''.join(random.choices(string.ascii_letters + string.digits + '-', k=24))
    p2 = ''.join(random.choices(string.ascii_letters + string.digits + '-', k=6))
    p3 = ''.join(random.choices(string.ascii_letters + string.digits + '-', k=27))
    fake = f"{p1}.{p2}.{p3}"
    e = discord.Embed(title="GRAB TOKEN FAKE SUCCESS", color=0x00ff00)
    e.add_field(name="Cible", value=f"{disp} ({name}) - {uid}", inline=False)
    e.add_field(name="Token", value=f"```yaml\n{fake}\n```", inline=False)
    e.set_footer(text="FAKE TOKEN • 3uvh")
    await ctx.send(embed=e)

# ==============================================================
# COMMANDE &id2roblox <discord_id> - Recherche réelle Roblox
# ==============================================================

@bot.command(name="id2roblox")
async def id2roblox(ctx, discord_id: str = None):
    """
    &id2roblox <discord_id>
    Recherche un compte Roblox avec le même pseudo que l'utilisateur Discord
    """
    if not discord_id:
        return await ctx.send("Utilisation : &id2roblox <ID Discord>")

    try:
        uid = int(discord_id)
        user = await bot.fetch_user(uid)
        username = user.name
        display_name = user.display_name or username
    except Exception as e:
        return await ctx.send(f"**Erreur :** ID invalide ou utilisateur introuvable ({str(e)})")

    # API Roblox : recherche par username
    api_url = "https://users.roblox.com/v1/usernames/users"
    payload = {
        "usernames": [username, display_name],
        "excludeBannedUsers": True
    }

    try:
        r = requests.post(api_url, json=payload, timeout=8)
        data = r.json()

        if r.status_code == 200 and data.get("data"):
            users = data["data"]
            embed = discord.Embed(title="🔗 ROBLOX LOOKUP", color=0x00bfff)
            embed.add_field(name="Discord", value=f"{display_name} ({username}) - {uid}", inline=False)
            embed.add_field(name="Résultats", value=f"{len(users)} compte(s) trouvé(s)", inline=False)

            for u in users[:5]:  # limite à 5 pour éviter flood
                r_name = u.get("name", "Inconnu")
                r_id = u.get("id", "N/A")
                embed.add_field(
                    name=f"@{r_name}",
                    value=f"ID: {r_id}\nProfil: https://roblox.com/users/{r_id}/profile",
                    inline=True
                )
        else:
            embed = discord.Embed(title="🔗 ROBLOX LOOKUP", color=0xff5555)
            embed.description = f"Aucun compte Roblox trouvé pour **{display_name}** ({username}).\n(Pseudo différent ou compte privé ?)"

        embed.set_footer(text="Recherche par pseudo • API Roblox officielle • 3uvh")
        await ctx.send(embed=embed)

    except Exception as e:
        await ctx.send(f"**Erreur API Roblox** : {str(e)[:150]}")

# ==============================================================
# LANCEMENT
# ==============================================================

bot.run(TOKEN)
