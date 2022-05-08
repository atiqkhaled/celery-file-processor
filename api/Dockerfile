FROM pytorch/pytorch:latest
WORKDIR /app
RUN apt-get update
COPY requirements.txt requirements.txt
RUN pip install -U pip
RUN pip install -r requirements.txt
RUN pip install azure-storage-blob
COPY . .
# RUN rm -r /app/api/uploads/*; exit 0
# RUN rm -r /app/api/static/*; exit 0