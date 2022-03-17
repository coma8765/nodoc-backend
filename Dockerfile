FROM python:slim as builed
#For all containers need .env

WORKDIR /code

RUN apt update && \
    apt install gcc git -y && \
    python3 -m venv .env && \
    pip install --user pipenv && \
    mkdir -p -m 0700 ~/.  ssh && ssh-keyscan github.com >> ~/.ssh/known_hosts


COPY Pipfile* ./

RUN --mount=type=cache,target=/root/.cache \
    --mount=type=ssh \
    PIPENV_VERBOSITY=-1 PIP_NO_BINARY=protobuf VIRTUAL_ENV=.env python -m pipenv install && \
    VIRTUAL_ENV=.env python -m pipenv install pipenv --skip-lock

FROM python:slim as dev
#Need mount volume to /code/app

WORKDIR /code

COPY --from=builed /code/.env /code/.env
ENV PATH="/code/.env/bin:$PATH"

EXPOSE 80

CMD pipenv run uvicorn app.main:app --host 0.0.0.0 --port 80 --root-path /api --reload

FROM python:slim as test

WORKDIR /code

COPY --from=builed /code/.env /code/.env
#ENV PATH="/code/.env/bin:$PATH"

EXPOSE 80

CMD pipenv run pytest app -v

FROM python:slim as prod

WORKDIR /code

COPY --from=builed /code/.env /code/.env
ADD ./app /code/app
#ENV PATH="/code/.env/bin:$PATH"

EXPOSE 80

CMD pipenv run uvicorn app.main:app --host 0.0.0.0 --port 80 --root-path /api
