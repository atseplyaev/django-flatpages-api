FROM python:3.8-alpine
ARG POETRY_PARAMS=""
ENV PYTHONUNBUFFERED 1
EXPOSE 8000/tcp

RUN mkdir /app
WORKDIR /app/
COPY requirements.txt /app/
RUN apk add --no-cache --virtual build-deps \
    git `# для установки зависимостей из git` \
    make gcc g++ `# для сборки пакетов` \
    postgresql-dev `# для psycopg2`
RUN pip install -U --trusted-host pypi.org --trusted-host files.pythonhosted.org pip setuptools && pip install -U --trusted-host pypi.org --trusted-host files.pythonhosted.org -r requirements.txt
COPY / /app/

#RUN python manage.py migrate
#RUN python manage.py collectstatic
RUN chmod +x entrypoint.*
#CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
