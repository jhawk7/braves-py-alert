FROM python:3.11.9-alpine3.19
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
CMD [ "python", "./braves_alert.py" ]
