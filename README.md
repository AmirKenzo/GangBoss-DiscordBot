# 📖 GangBoss Documentation

[🇮🇷 فارسی نسخه](./README-fa.md) | [🇬🇧 English Version](./README.md)

---

# 🤖 GangBoss — Discord Bot for Gang Management in VMP (FiveM)

**GangBoss** is a professional, fast, and fully customizable bot built to manage gangs in **VMP/FiveM** roleplay servers.
Whether you run a small crew or a full-scale mafia, GangBoss keeps everything organized, accurate, and professional.

---

## 🚀 Features

* 📊 **Automatic XP tracking for robberies (Rob XP)**
* 📅 **Leaderboard of top players with the highest XP**
* 🧬 **Capture reminders (1 hour before start)**
* 🛠️ **Weekly auto-reset of all users' XP**

---

## 🪄 Installation & Setup

Run the following command on your VPS:

```bash
sudo bash -c "$(curl -sL https://raw.githubusercontent.com/AmirKenzo/GangBoss-DiscordBot/main/install.sh)" @ install
```

Then:

```bash
source $HOME/.local/bin/env
```

Start the setup script with:

```bash
gangboss
```

To edit and configure the bot:

```bash
gangboss edit
```

Fill in the following values carefully:

```env
TOKEN=MTM0OTg5ODA4ODAy111111111111
SERVER_GUILD_ID=123456789012345678
CHANNEL_XP_REPORT=1122116069272846356
CHANNEL_ANNOUNCEMENT=868663566981558342
CHANNEL_STATUS_ROB=333333333333333
ACTIVITY_BOT=["GangBoss", "GangBoss Bot"]
BANNER_LINK=https://dl.loserbot.ir/files/44896_al.png
GANG_NAME="GangBoss"

ROLE_FAMILY=Family,Owner
ROLE_XP_MANAGER=Owner,💻 𝑫𝒊𝒔𝒄𝒐𝒓𝒅 𝑫𝒆𝒗𝒆𝒍𝒐𝒑𝒆𝒓 💻
```

---

## 📖 Variable Descriptions

* **`TOKEN`** → Discord bot token (from the [Discord Developer Portal](https://discord.com/developers/applications)).
* **`SERVER_GUILD_ID`** → Numeric ID of your main Discord server.
* **`CHANNEL_XP_REPORT`** → Channel where XP leaderboard is posted.
* **`CHANNEL_ANNOUNCEMENT`** → Channel for announcements and capture reminders.
* **`CHANNEL_STATUS_ROB`** → Channel where robbery (Rob) logs are posted.
* **`ACTIVITY_BOT`** → Bot status messages (can rotate between multiple).
* **`BANNER_LINK`** → Direct link to a banner image used in embeds.
* **`GANG_NAME`** → Default gang name displayed in bot messages.
* **`ROLE_FAMILY`** → Roles with **basic bot permissions**, such as running normal commands like registering robberies.
* **`ROLE_XP_MANAGER`** → Roles with **advanced XP management permissions**, such as resetting XP, changing values, and viewing detailed reports.

⚠️ Note: All IDs must be **exact numeric IDs from your server**. Incorrect values will break functionality.

---

## ▶️ Running the Bot

After saving your changes (`Ctrl + X` → `Y` → `Enter`):

```bash
gangboss run
```

To stop or reconfigure:

```bash
gangboss stop
```

---

## 🛡️ License

**MIT License** – free to use, just don’t forget to credit.

---
