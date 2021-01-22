FROM python:3.8-slim
ENV PYTHONUNBUFFERED=1
COPY . .
RUN mv config.ini.docker config.ini
RUN pip install -r requirements.txt