from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
import uvicorn

app = FastAPI(title="Invest Zilla", description="منصة استثمار وتداول تجريبية")

# نموذج بيانات المستخدم
class User(BaseModel):
    username: str
    email: str
    balance: float = 0.0

# قاعدة بيانات بسيطة مؤقتة في الذاكرة
users_db = {}

@app.get("/")
def home():
    return {"message": "مرحبًا بك في Invest Zilla 🚀", "status": "online"}

@app.post("/register")
def register(user: User):
    if user.username in users_db:
        return {"error": "اسم المستخدم مسجل مسبقًا"}
    users_db[user.username] = user
    return {"message": f"تم تسجيل {user.username} بنجاح", "user": user}

@app.get("/user/{username}")
def get_user(username: str):
    user = users_db.get(username)
    if not user:
        return {"error": "المستخدم غير موجود"}
    return user

@app.post("/trade")
def trade(username: str, amount: float):
    user = users_db.get(username)
    if not user:
        return {"error": "المستخدم غير موجود"}
    user.balance += amount
    return {"message": f"تم تحديث رصيد {username}", "balance": user.balance}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=10000)
