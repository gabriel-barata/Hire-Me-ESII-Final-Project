```bash

# subir o container do banco de dados
docker compose up -d

# rodar o programa
poetry run python -m app.main

# checar o coverage
poetry run pytest --cov=app

```
