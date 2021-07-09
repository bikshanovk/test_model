FROM python:3.9-slim

WORKDIR /usr/src/app
MKDIR 

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY test.py .

CMD [ "python", "./test.py" ]
