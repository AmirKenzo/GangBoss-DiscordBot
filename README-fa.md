# 🤖 GangBoss — ربات دیسکورد برای مدیریت گَنگ در VMP (FiveM)

**GangBoss** یک ربات حرفه‌ای، سریع و کاملاً قابل‌سفارشی‌سازی است که برای مدیریت گَنگ در سرورهای رول‌پلی **VMP/FiveM** ساخته شده.
فرقی نداره گَنگ کوچیک داشته باشی یا یه مافیای بزرگ، با GangBoss همه‌چیز مرتب، دقیق و حرفه‌ای پیش میره.

---

## 🚀 قابلیت‌ها

* 📊 **ثبت خودکار XP سرقت‌ها (Rob XP)**
* 📅 **نمایش جدول برترین افراد با بیشترین XP**
* 🧬 **یادآوری شروع کپچر (۱ ساعت قبل)**
* 🛠️ **ریست هفتگی XP تمام یوزرها به صورت خودکار**

---

## 🪄 آموزش نصب و راه‌اندازی

ابتدا دستور زیر را داخل سرور مجازی خود اجرا کنید:

```bash
sudo bash -c "$(curl -sL https://raw.githubusercontent.com/AmirKenzo/GangBoss-DiscordBot/main/install.sh)" @ install
```

سپس:

```bash
source $HOME/.local/bin/env
```

حالا با زدن دستور زیر، اسکریپت راه‌اندازی اجرا می‌شود:

```bash
gangboss
```

برای ویرایش و کانفیگ ربات:

```bash
gangboss edit
```

موارد زیر را باید دقیق وارد کنید:

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

## 📖 توضیحات متغیرها

* **`TOKEN`** → توکن ربات دیسکورد (از Discord Developer Portal می‌گیرید).
* **`SERVER_GUILD_ID`** → آیدی عددی سرور اصلی شما.
* **`CHANNEL_XP_REPORT`** → کانالی که گزارش XP (برترین‌ها) در آن ارسال می‌شود.
* **`CHANNEL_ANNOUNCEMENT`** → کانال اطلاع‌رسانی رویدادها و کپچر.
* **`CHANNEL_STATUS_ROB`** → کانالی برای وضعیت و گزارش Rob.
* **`ACTIVITY_BOT`** → متن وضعیت (Activity) ربات در دیسکورد (می‌تواند چند مقدار داشته باشد).
* **`BANNER_LINK`** → لینک مستقیم تصویر بنر که در پیام‌های Embed نمایش داده می‌شود.
* **`GANG_NAME`** → نام گَنگ شما که در پیام‌ها استفاده می‌شود.
* **`ROLE_FAMILY`** → رول فمیلی دستورات معمولی ربات رو میتونه استفاده کنه
* **`ROLE_XP_MANAGER`** → نقش‌هایی که دسترسی مدیریت XP (ریست/کنترل) را دارند.

⚠️ نکته: همه آیدی‌ها باید **عددی و دقیقاً از سرور شما** کپی شده باشند. اگر اشتباه باشند ربات کار نمی‌کند.

---

## ▶️ اجرای ربات

بعد از ذخیره تغییرات (`Ctrl + X` → `Y` → `Enter`):

```bash
gangboss run
```

در صورت نیاز به توقف یا اصلاح کانفیگ:

```bash
gangboss stop
```

---

## 🛡️ لایسنس

لایسنس **MIT** – استفاده آزاد، فقط فراموش نکنید منبع را ذکر کنید.

---
