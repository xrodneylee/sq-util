FROM python:3-alpine
MAINTAINER guanpu.lee "xrodneylee@infinitiessoft.com"
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN apk update && \
    apk add openssh && \
    pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 5000
CMD [ "python", "app.py" ]