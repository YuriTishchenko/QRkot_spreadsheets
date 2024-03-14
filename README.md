### приложение QRKot
приложение для Благотворительного фонда поддержки котиков QRKot. 
Фонд собирает пожертвования на различные целевые проекты: на медицинское обслуживание нуждающихся хвостатых, на обустройство кошачьей колонии в подвале, на корм оставшимся без попечения кошкам — на любые цели, связанные с поддержкой кошачьей популяции.
## Создание и применение миграций
- alembic revision --autogenerate -m "The name of the migration" 
- alembic upgrade head 
## Технологии
- Python
- FastAPI
- SQLAlchemy
- Alembic
- Pydantic
- Asyncio
## Пример запроса
**`POST` | Создание проекта: `http://localhost:8000/charity_project/`**
Request:
```
{
  "name": "Мертвый Бассейн",
  "description": "Deadpool inside",
  "full_amount": 100
}
```
Response:
```
{
  "name": "Мертвый Бассейн",
  "description": "Deadpool inside",
  "full_amount": 100,
  "id": 8,
  "invested_amount": 0,
  "fully_invested": false,
  "create_date": "2024-03-07T00:24:30.063772"
}
```
### Автор
Тищенко Юрий