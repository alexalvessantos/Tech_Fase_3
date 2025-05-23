train:
	python ml/train.py

run-api:
	uvicorn api.main:app --reload

run-dashboard:
	streamlit run dashboard/app.py

up-db:
	docker-compose up -d

down-db:
	docker-compose down
