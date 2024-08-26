#FROM python:3.12.3-slim
FROM python:3.11.9-slim
ENV HNSWLIB_NO_NATIVE=1
WORKDIR /app
RUN export HNSWLIB_NO_NATIVE=1
RUN apt-get update --fix-missing && apt-get install -y --fix-missing build-essential

COPY . /app/
RUN pip install --no-cache-dir -r /app/requirements.txt
EXPOSE 8000

CMD ["uvicorn", "athena.main:app", "--host", "0.0.0.0", "--port", "8000"]
#CMD ["gunicorn", "-w", "2", "-k", "uvicorn.workers.UvicornWorker" "athena.main:app", "--host", "0.0.0.0", "--port", "8000"]
