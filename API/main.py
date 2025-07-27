import sqlite3
from fastapi import FastAPI, Query
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from datetime import datetime

DB_NAME = "reviews.db"
lst_pos = ["отличный", "хороший", "замечательный", "прекрасный", "любимый"]
lst_neg = ["ужасный", "плохой", "неприятный", "разочаровывающий", "ненавистный"]
created_at = datetime.utcnow().isoformat()

def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    return conn


def create_table():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS reviews (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    text TEXT NOT NULL,
    sentiment TEXT NOT NULL,
    created_at TEXT NOT NULL
    );
    """)

    conn.commit()
    conn.close()


app = FastAPI()


class Item(BaseModel):
    text: str


@app.post("/reviews")
def create_item(item: Item):

    create_table() #создание таблицы в случае отсутствия

    conn = get_db_connection()
    cursor = conn.cursor()
    sentiment = "negative"
    for i in lst_pos:
        if i in item.text:
            sentiment = "positive"
            break

    cursor.execute("INSERT INTO reviews (text, sentiment, created_at) VALUES (?, ?, ?)", (item.text, sentiment, created_at))

    conn.commit()

    conn.close()
    
    return {"message": "Отзыв успешно добавлен!"}

@app.get("/reviews")
def get_reviews(sentiment: str = Query(None)):

    print(sentiment)

    conn = get_db_connection()
    cursor = conn.cursor()

    # Получение всех записей
    cursor.execute("SELECT * FROM reviews WHERE sentiment = ?", (sentiment,))
    rows = cursor.fetchall()

    # Преобразование результата в список словарей
    items = [{"id": row[0], "text": row[1], "sentiment": row[2], "created_at": row[3]} for row in rows]

    conn.close()  

    return JSONResponse(content=items)