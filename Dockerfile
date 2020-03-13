FROM tiangolo/uvicorn-gunicorn-fastapi:python3.6-alpine3.8

#Numpy para Alpine
RUN apk --no-cache add --virtual .builddeps gcc gfortran musl-dev    && pip install numpy==1.18.1     && apk del .builddeps     && rm -rf /root/.cache

# Make directories suited to your application
RUN mkdir -p /home/project/app
WORKDIR /home/project/app

# Copy and install requirements
COPY requirements.txt /home/project/app
RUN pip install --no-cache-dir -r requirements.txt

# Copy contents from your local to your docker container
COPY . /home/project/app