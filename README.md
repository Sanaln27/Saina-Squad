# 💤 Sleep Debt Wallet  ⏳🔒

A smart wellness app that tracks your **sleep hours** and **screen time**, and automatically **locks social media** when you're not giving your mind enough rest.
🧠Concept
- 📉 **Sleep Debt:** Hours you owe your body
- 📱 **Screen Time Debt:** Hours you spend glued to screens

> 🔐 **If sleep debt increases** AND screen time gets too high, your social media apps/websites are **automatically locked**.
> 
## Core Features

| Feature                      | Description |
|-----------------------------|-------------|
| 🛌 Sleep Tracking           | Log your sleep hours daily |
| ⏳ Screen Time Tracker       | Automatically track screen time (mobile/PC) |
| 🧮 Combined Debt Score       | Combines sleep debt + screen usage to create a **wellness score** |
| 🔒 Social Media Lock         | Auto-blocks apps/websites (YouTube, Instagram, etc.) when thresholds are exceeded |
| 📈 Visual Dashboard          | See your patterns with graphs and tips |
| 🔓 Auto Unlock               | Access is restored after enough sleep or screen detox |

---

## How Locking Works

| Condition | Result |
|----------|--------|
| Sleep debt ≤ 2 hrs and screen time ≤ 2 hrs/day | ✅ Normal access |
| Sleep debt > 3 hrs or screen time > 3.5 hrs/day | ⚠️ Warning |
| Sleep debt ≥ 5 hrs and screen time ≥ 4 hrs/day | 🔒 Lock activated |
| Sleep recovery or screen time reduction | 🔓 Unlock access |

---

##  Tech Stack

- 🐍 Python (main logic)
- 📉 Pandas & Matplotlib (data + graphs)
- 📱 Android Screen Time APIs *(or Shizuku/Tasker if rooted)*
- 🖥️ PC Version: `pyautogui`, `time`, `browser history` module
- 🔐 Chrome Extension / Windows Host File Modifier *(for blocking)*

## How to Run

1. Clone the repo:
   ```bash
   git clone https://github.com/yourusername/sleep-debt-wallet.git
   cd sleep-debt-walle
## Project Structure 
sleep-debt-wallet/
│
├── sleep_wallet.py          # Main app logic
├── screen_time_reader.py    # Gets daily screen time
├── lock_controller.py       # Social media lock/unlock logic
├── data/
│   ├── sleep_log.csv
│   └── screen_time_log.csv
├── dashboard.ipynb          # Graphs and trends
├── requirements.txt
└── README.md
