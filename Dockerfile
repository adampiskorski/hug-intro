FROM python:3.6

LABEL Name=hug-intro Version=0.0.1
EXPOSE 8000

WORKDIR /app
ADD . /app

RUN pip install pipenv
RUN pipenv install  --ignore-pipfile

CMD ["pipenv", "run", "hug", "-f", "todo_api.py"]
