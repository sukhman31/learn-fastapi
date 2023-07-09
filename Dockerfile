FROM python:3.11.4-slim-bullseye

RUN mkdir /code

WORKDIR /code

COPY Pipfile Pipfile.lock ./

RUN python -m pip install --upgrade pip
RUN pip install pipenv
RUN pipenv install --dev --system --deploy

COPY . .

CMD ["uvicorn","app.main:app","--host","0.0.0.0","--port","8000"]