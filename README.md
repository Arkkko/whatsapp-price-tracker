# 📉 WhatsApp Price Tracker (Selenium & Twilio)

An automated Python bot that monitors product prices on dynamic e-commerce websites (handling JavaScript/Vue.js) and sends instant alerts via WhatsApp when a discount is detected.

## 🚀 Key Features

* **Dynamic Scraping:** Uses **Selenium** to render JavaScript-heavy websites (e.g., Media Expert) where standard requests fail.
* **Instant Alerts:** Integrated with **Twilio API** to send real-time notifications directly to WhatsApp.
* **Headless Browser:** Runs Chrome in the background without opening a graphical window (server-ready).
* **Smart Parsing:** robust HTML parsing using **BeautifulSoup**.
* **Security:** API keys and sensitive data are protected using environment variables (`.env`).
* **Scheduler:** Automatically checks prices every 24 hours.

## 🛠️ Tech Stack

* **Python 3.10+**
* **Selenium** (Browser automation)
* **Twilio** (WhatsApp API)
* **BeautifulSoup4** (HTML Parsing)
* **Schedule** (Job scheduling)
* **Python-Dotenv** (Environment management)

## ⚙️ Installation & Setup

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/YOUR_USERNAME/whatsapp-price-tracker.git](https://github.com/YOUR_USERNAME/whatsapp-price-tracker.git)
    cd whatsapp-price-tracker
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Configuration (.env):**
    Create a `.env` file in the root directory and add your Twilio credentials:
    ```env
    TWILIO_SID=your_twilio_sid
    TWILIO_AUTH_TOKEN=your_twilio_auth_token
    MY_PHONE_NUMBER=whatsapp:+48xxxxxxxxx
    ```
    *(Note: You need to join the Twilio Sandbox on WhatsApp first to receive messages).*

4.  **Run the bot:**
    ```bash
    python main.py
    ```

## 📸 Usage Example

When the target price is met, you receive a message like this:

> 🔥 **Promocja!** Słuchawki Technics EAH-AZ100E-K
> **Aktualna cena:** 899.00 zł
> **Link:** [mediaexpert.pl/...]

Console Output:
```text Sprawdzam cenę...
Produkt: Słuchawki Technics
Cena: 899.00 zł
🚀 Cena jest niska! Wysyłam WhatsApp...
✅ Wiadomość wysłana! ID: SMxxxxxxxx...
