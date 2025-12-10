import time
import os
import schedule
from bs4 import BeautifulSoup
from twilio.rest import Client
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

load_dotenv()

TWILIO_SID = os.getenv("TWILIO_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
FROM_WHATSAPP = 'whatsapp:+14155238886'
TO_WHATSAPP = os.getenv("MY_PHONE_NUMBER")

URL = "https://www.mediaexpert.pl/telewizory-i-rtv/sluchawki/wszystkie-sluchawki/sluchawki-dokanalowe-technics-eah-az100e-k-anc-wodoodporne-czarny"
TARGET_PRICE = 900.00

def send_whatsapp_message(product_name, price):
    try:
        client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)
        msg_body = f"🔥 Promocja! {product_name} kosztuje teraz {price} zł. Sprawdź: {URL}"

        message = client.messages.create(
            body=msg_body,
            from_=FROM_WHATSAPP,
            to=TO_WHATSAPP,
        )
        print(f"✅ Wiadomość wysłana! ID: {message.sid}")
    except Exception as e:
        print(f"❌ Błąd Twilio: {e}")

def get_page_source_selenium(url):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        driver.get(url)
        time.sleep(5)
        return driver.page_source
    except Exception as e:
        print(f"Błąd Selenium: {e}")
        return None
    finally:
        driver.quit()

def check_price():
    print(f"\n[{time.strftime('%H:%M:%S')}] Sprawdzam cenę...")

    html_content = get_page_source_selenium(URL)

    if not html_content:
        print("Nie udało się pobrać strony.")
        return

    soup = BeautifulSoup(html_content, "html.parser")

    try:
        title_element = soup.find("h1", class_="name is-title")
        if title_element:
            title = title_element.get_text().strip()
        else:
            title = "Nieznany produkt"
            print("Nie znaleziono tytułu")

        price_container = soup.find("div", class_="main-price is-big")

        if price_container:
            whole = price_container.find("span", class_="whole").get_text().strip()
            cents = price_container.find("span", class_="cents").get_text().strip()

            price_clean = float(f"{whole}.{cents}")

            print(f"Produkt: {title}")
            print(f"Cena:    {price_clean} zł")

            if price_clean < TARGET_PRICE:
                print("🚀 Cena jest niska! Wysyłam WhatsApp...")
                send_whatsapp_message(title, price_clean)
            else:
                print(f"📉 Cena wciąż za wysoka (Cel: {TARGET_PRICE} zł).")
        else:
            print("⚠️ Nie znaleziono ceny na stronie.")

    except Exception as e:
        print(f"Wystąpił błąd parsowania: {e}")

schedule.every(24).hours.do(check_price)

if __name__ == "__main__":
    check_price()

    while True:
        schedule.run_pending()
        time.sleep(60)