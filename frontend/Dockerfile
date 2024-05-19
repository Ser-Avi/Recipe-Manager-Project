FROM python:3.8-slim

WORKDIR /app

COPY . /app

RUN pip3 install --trusted-host pypi.python.org -r requirements.txt

EXPOSE 4280

CMD ["python3", "-m", "flask", "--app", "app.py", "run", "--host=0.0.0.0", "--port=4280"]
