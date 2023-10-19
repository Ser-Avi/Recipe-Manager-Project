FROM python:3.8-slim

WORKDIR /app

COPY . /app

RUN pip3 install --trusted-host pypi.python.org -r requirements.txt

EXPOSE 4200

CMD ["python3", "-m", "flask", "--app", "Flask_test.py", "run", "--host=0.0.0.0", "--port=4200"]
