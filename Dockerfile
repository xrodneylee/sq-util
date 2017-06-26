FROM python:3-alpine
MAINTAINER guanpu.lee "xrodneylee@infinitiessoft.com"
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt &&
    apk add openssh
COPY . .
EXPOSE 5000
CMD [ "python", "app.py" ]