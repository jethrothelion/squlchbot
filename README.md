# 🔒 SqelchBot 

SqelchBot is a continuation of a 9th grade pyton final project. All features not fully implented as of right now because of a major restructuer but all features are there

![SecureBot Banner](http://i.ytimg.com/vi/SQJrYw1QvSQ/hq720.jpg?sqp=-oaymwEhCK4FEIIDSFryq4qpAxMIARUAAAAAGAElAADIQj0AgKJD&rs=AOn4CLBY9A7Gomuj6iHkoDkSidTzx0bZAw/120x300?text=SecureBot)

## 🚀 Features
- **🎵 Music Playback** - Play music in voice channels for a better community experience.
- **📹 Security Camera Integration** - Receive alerts from your security cameras. Only tested with usb cameras.
- **🌅 Morning Announcements** - Automated daily updates with weather, news, countdown to dates, and a ui apearing every morning.
- **🌐 IP Communication** - Send and receive messages using IP-based communication.
- **🔔 Real-Time Alerts** - Get instant Discord notifications for motion detection.
- **📜 Logs & Reports** - Keep track of all alerts and communications in an organized format.

## 📦 Installation
```bash
git clone https://github.com/jethrothelion/squlchbot.git
cd SecureBot
pip install -r requirements.txt
for security camera functions, contacam is needed as of right now
```

## 🛠 Setup
1. Create a `.env` file and add your bot token and other necessary credentials:
```env
BOT_TOKEN=your_discord_bot_token
IP_password=your_password
```
2. put the path of your exes for opus fmmpeg and ytdlp if you want media playing functions
3. Run the bot:
```bash
botfile.py
```

## 🎮 Commands
I will fill out this section later but all commands are avaliable in the on_message method in botfile.py

## ⚡ Future Features
- **Intgeration with custom detection software**
- **rasbary pi support or atleast a diffrent version supporting linux**
- **Multi-Camera Support**
- **Encrypted IP Messaging**
- **Voice Command Integration**
- **Choice of what features to run**

## 🤝 Contributing
Pull requests are welcome

## 🛡️ Security
If you discover any security issues, please report them to me.


