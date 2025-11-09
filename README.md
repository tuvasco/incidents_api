Incidents API

Мини-сервис для учёта инцидентов (FastAPI + SQLite).

🚀 Как запустить
git clone https://github.com/tuvasco/incidents_api.git
cd incidents_api
python -m venv venv
source venv/bin/activate     # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload


API будет доступен на
👉 http://127.0.0.1:8000/docs

🔗 Эндпоинты (примеры)
1️⃣ Создать инцидент

POST /incidents/

{
  "description": "Самокат не в сети",
  "source": "operator"
}

2️⃣ Получить список

GET /incidents/?status=new

3️⃣ Обновить статус

PATCH /incidents/1

{
  "status": "resolved"
}


📄 База данных создаётся автоматически (SQLite).
Статусы: new, in_progress, resolved, closed.

