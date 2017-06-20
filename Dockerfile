FROM python:3-alpine
MAINTAINER guanpu.lee "xrodneylee@infinitiessoft.com"
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD [ "python", "./app.py" ]