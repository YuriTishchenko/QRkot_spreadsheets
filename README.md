### приложение QRKot
приложение для Благотворительного фонда поддержки котиков QRKot. 
Фонд собирает пожертвования на различные целевые проекты: на медицинское обслуживание нуждающихся хвостатых, на обустройство кошачьей колонии в подвале, на корм оставшимся без попечения кошкам — на любые цели, связанные с поддержкой кошачьей популяции.
### Google Sheets для QRKot
Приложение QRKot может формировать отчёт в гугл-таблице. В таблице присутсвуют закрытые проекты, отсортированные по скорости сбора средств: от тех, что закрылись быстрее всего, до тех, что долго собирали нужную сумму.
## Установка
- Склонируйте репозиторий: git clone git@github.com:AbbadonAA/cat_charity_fund.git
- Создайте venv: python3 -m venv venv
- Активируйте виртуальное окружение: source venv/bin/activate
- установите зависимости: pip install -r requirements.txt
- Создайте в и заполните корневой директории файл .env
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
- Google Sheets;
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
