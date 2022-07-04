# 会議室予約管理システム(Udemy)

```bash
git clone https://github.com/hamattiv2/python_fast_api_earning.git
cd python_fast_api_earning/reserve_meeting_apps
docker-compose up -d
docker exec -d web streamlit run app.py
docker-compose exec api bash
uvicorn sql_app.main:app --port 8082 --host 0.0.0.0 --reload
```

127.0.0.1:8501へアクセスする