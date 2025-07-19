# Mini Feedback Sentiment Service

## Запуск

```bash
pip install flask
python main.py
```

## Примеры запросов

### Добавить отзыв
```bash
curl -X POST http://127.0.0.1:5000/reviews -H "Content-Type: application/json" -d '{"text": "Очень плохо, не работает!"}'
```
**Ответ:**
```json
{
  "id": 1,
  "text": "Очень плохо, не работает!",
  "sentiment": "negative",
  "created_at": "2024-05-01T12:34:56.789012"
}
```

### Получить все негативные отзывы
```bash
curl "http://127.0.0.1:5000/reviews?sentiment=negative"
```
**Ответ:**
```json
[
  {
    "id": 1,
    "text": "Очень плохо, не работает!",
    "sentiment": "negative",
    "created_at": "2024-05-01T12:34:56.789012"
  }
]
```

### Добавить позитивный отзыв
```bash
curl -X POST http://127.0.0.1:5000/reviews -H "Content-Type: application/json" -d '{"text": "Очень хорошая служба, люблю вас!"}'
```
**Ответ:**
```json
{
  "id": 2,
  "text": "Очень хорошая служба, люблю вас!",
  "sentiment": "positive",
  "created_at": "2024-05-01T12:35:10.123456"
}
```

### Получить все отзывы (без фильтра)
```bash
curl "http://127.0.0.1:5000/reviews"
```
**Ответ:**
```json
[
  {
    "id": 1,
    "text": "Очень плохо, не работает!",
    "sentiment": "negative",
    "created_at": "2024-05-01T12:34:56.789012"
  },
  {
    "id": 2,
    "text": "Очень хорошая служба, люблю вас!",
    "sentiment": "positive",
    "created_at": "2024-05-01T12:35:10.123456"
  }
]
```

---

**Контакты для связи:**
- [Ваше имя или ник] 