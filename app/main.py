from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pyautogui
import time

app = FastAPI()

class Message(BaseModel):
    phone_no: str
    text: str

# Инициализация веб-драйвера для Chrome
driver = webdriver.Chrome()

@app.post("/send-message-pywhatkit/")
def send_message_pywhatkit(message: Message):
    try:
        # Получаем текущее время
        current_time = datetime.now()
        time_hour = current_time.hour
        time_min = current_time.minute

        send_whatsapp_message_pywhatkit(message.phone_no, message.text, time_hour, time_min)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return {"status": "Message sent successfully using pywhatkit"}

def send_whatsapp_message_pywhatkit(phone_no, text, time_hour, time_min):
    try:
        # Отправляем сообщение на WhatsApp с помощью pywhatkit
        pywhatkit.sendwhatmsg(f"+{phone_no}", text, time_hour, time_min)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/send-message-selenium/")
def send_message_selenium(message: Message):
    try:
        send_whatsapp_message_selenium(message.phone_no, message.text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return {"status": "Message sent successfully using Selenium"}

def send_whatsapp_message_selenium(phone_no, text):
    try:
        driver.get(f"https://web.whatsapp.com/send?phone={phone_no}&text={text}")
        time.sleep(10)  # Даем время для загрузки страницы и QR-кода
        input_box = driver.find_element(By.CSS_SELECTOR, 'div[data-tab="6"]')
        input_box.send_keys(text)
        input_box.send_keys(Keys.ENTER)
        time.sleep(3)  # Даем время для отправки сообщения
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.on_event("shutdown")
def shutdown_event():
    driver.quit()
