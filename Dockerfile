# docker build --tag yingshaoxo/it_has_alternatives . --no-cache

FROM node:18 as front_end_building_stage

COPY ./front_end /front_end

WORKDIR /front_end

RUN yarn

RUN GENERATE_SOURCEMAP=false NODE_OPTIONS="--max-old-space-size=8192" yarn build




FROM python:3.10-bullseye as building_stage

WORKDIR /code

RUN pip install poetry

COPY ./backend_service/pyproject.toml ./backend_service/poetry.lock* /code/

RUN poetry export -f requirements.txt --output requirements.txt --without-hashes
# RUN poetry install

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./backend_service/backend_service /code/backend_service

COPY --from=front_end_building_stage /front_end/dist /code/backend_service/vue

RUN pip install pyinstaller
COPY ./backend_service/compile.sh /code/compile.sh

RUN bash compile.sh




FROM ubuntu:22.04

#RUN apt update
#RUN apt install -y wget

COPY --from=building_stage /code/backend_service/dist/main.run /binary/main.run

WORKDIR /binary

EXPOSE 5550
EXPOSE 5551
EXPOSE 5552
EXPOSE 5553

CMD ["/binary/main.run"]
