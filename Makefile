install:
	@echo "Instalando dependências..."
	-pip install -r requirements.txt  # O '-' ignora erros
	@echo "Dependências instaladas (alguns erros podem ser ignorados)"

run:
	python -m uvicorn app.main:app --reload --port 8000