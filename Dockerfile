FROM python:3.12-slim

WORKDIR /app

COPY helpdesk.py .

CMD ["python", "helpdesk.py"]
