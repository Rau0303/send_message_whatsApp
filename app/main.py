from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pywhatkit
from datetime import datetime

app = FastAPI()

class Message(BaseModel):
    phone_no: str
    text: str

@app.post("/send-message/")
def send_message(message: Message):
    try:
        # Получаем текущее время
        current_time = datetime.now()
        time_hour = current_time.hour
        time_min = current_time.minute

        send_whatsapp_message(message.phone_no, message.text, time_hour, time_min)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return {"status": "Message sent successfully"}

def send_whatsapp_message(phone_no, text, time_hour, time_min):
    try:
        # Отправляем сообщение на WhatsApp с помощью pywhatkit
        pywhatkit.sendwhatmsg(f"+{phone_no}", text, time_hour, time_min)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.on_event("shutdown")
def shutdown_event():
    pass  # Не требуется, так как pywhatkit не использует отдельный драйвер браузера
