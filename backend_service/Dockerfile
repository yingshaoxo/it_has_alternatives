# docker build --tag yingshaoxo/it_has_alternatives . --no-cache

FROM python:3.10-bullseye as requirements-stage

WORKDIR /code

RUN pip install poetry

COPY ./pyproject.toml ./poetry.lock* /code/

RUN poetry export -f requirements.txt --output requirements.txt --without-hashes
# RUN poetry install

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./backend_service /code/backend_service

WORKDIR /code/backend_service

EXPOSE 5550
EXPOSE 5551

CMD ["python3.10", "main.py"]

# RUN apt update
# RUN apt install python3.10 -y
# RUN apt install pip -y
# RUN apt install git -y
# RUN apt install wget -y