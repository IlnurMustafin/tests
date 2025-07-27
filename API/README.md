# Ильнур Мустафин

pip install fastapi uvicorn
uvicorn main:app --reload

curl -X 'POST' 'http://127.0.0.1:8000/reviews' \
     -H 'Content-Type: application/json' \
     -d '{"text": "плохой продукт!"}'

curl -X GET "http://localhost:8000/reviews?sentiment=negative"

