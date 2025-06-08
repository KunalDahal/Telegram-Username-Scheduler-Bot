
# Telegram Channel Username Rotator Bot

A sophisticated Telegram bot designed to automate username rotation for channels, preventing username squatting. Manages multiple channels with intelligent scheduling, recovery systems, and real-time analytics.

##  Prerequisites

Before you start, make sure you have:

-  Python 3.10+
-  Telegram API ID & API Hash (from [my.telegram.org](https://my.telegram.org))
-  MongoDB Atlas account for cloud-based database
-  Your Telegram Bot Token from [@BotFather](https://t.me/BotFather)

---

>  **Supports up to 10 channels per session**  
>  **One session only per bot** — simplicity at its best!

###  Core Functionality

---
- **Automated Username Rotation**  
- **Multi-Channel Management**  
- **Flood Control System**  
- **Cycle-Based Scheduling**  
- **Persistent State Recovery**  
- **Admin Hierarchy**   
- **Monitoring & Analytics**
---

## Installation

## Step 1: Clone & Configure

###  1.1 Clone the Repository

```bash
git clone https://github.com/your-repo-link
cd your-bot-folder
```


###  1.2 Set Up Configuration

Create a `.env` file or update your `config.py` or `ss.py` (based on your project structure):

| Key         | Description                                              |
|-------------|----------------------------------------------------------|
| `BOT_TOKEN` | Telegram bot token from @BotFather                       |
| `OWNER_ID`  | YOur Telegram user ID (numeric)                          |
| `API_ID`    | API ID from [my.telegram.org](https://my.telegram.org)   |
| `API_HASH`  | API Hash from [my.telegram.org](https://my.telegram.org) |
| `MONGO_URI` | MongoDB URI (from MongoDB Atlas project)                 |
| `DB_NAME`   | Name of your database inside the cluster                 |

>  **Note**:  
> This bot only supports **ONE session** but can manage up to **10 channels** per session!

##  Step 2: Generate Session String

The bot requires a Telegram **session string** to authenticate and manage channels.

You can generate it using:

```bash
python3 \ses_string
```
Command after starting the bot, For that you'll need the following:
`API ID` of that ID
`API HASH` of that ID
`MOBILE NUMBER` of that ID
`PASSWORD` of that ID

Or use any Pyrogram-based session generator and paste the resulting session string into your database or bot configuration securely.

>  Keep your session string **confidential** and use it wisely!

---

## ▶ Step 3: Run the Bot

Launch your bot using:

```bash
python3 run.py
```

If everything is set up properly, your automation bot should now be **live and running** ⚡

---


## 🛠 Technical Architecture

### Diagram

![Architecture Diagram](other/image.png)

---

## Troubleshooting

| Error               | Solution                                      |
|---------------------|-----------------------------------------------|
| FloodWait: 3600     | Bot auto-skips & resumes after cooldown       |
| UsernameInvalid     | Check username format rules                   |
| SessionRevoked      | Regenerate with /ses_string                   |
| Channel Not Found   | Verify bot has admin permissions              |

---

## License

**MIT License © 2023 Dahalkunal**

---

## Support

Contact [@suu_111](https://t.me/suu_111) for assistance

---

## Contributing

Pull requests welcome! Suggested areas for improvement:

- Enhanced handling for `UsernameInvalid`,`FloodWait Error`
- UI/UX improvements for `/list`
- Multi-language support

---

> **Note**: Use responsibly. Excessive username changes may trigger Telegram rate limits.
