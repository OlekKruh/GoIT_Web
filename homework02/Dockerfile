FROM python:3.12-alpine

WORKDIR /app

EXPOSE 5000

COPY . .

RUN pip install -r requirements.txt

ENTRYPOINT ["python", "AddressBookV0.2.py", "run"]