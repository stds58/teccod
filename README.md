
Установка uv: 
    pip install uv
    uv init

Добавить зависимости: 
    uv add <package_name_1> <package_name_2>

Добавить зависимость в группу (чтобы можно было устанавливать отдельной командой опциональные пакеты):
    uv add --group <group_name>  <package_name_1> <package_name_2>

Установить зависимости:
    uv sync
    uv sync --group <group_name>

Все пакеты устанавливаются в virtual env, расположенный в .venv


docker-compose down -v fastapi
docker-compose build
docker-compose up
docker-compose up --build fastapi

docker inspect --format='{{.State.Health}}' opensearch

http://localhost:8000/search?q=Python
http://localhost:8000/search?q=Docker&type=tutorial
http://localhost:8000/api/search

###########################

удалить
from app.dependencies.get_db import get_opensearch



########################


