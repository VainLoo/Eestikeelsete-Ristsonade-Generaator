FROM python:3.10-alpine
WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip
RUN apk update
RUN apk add make automake gcc g++ subversion python3-dev

RUN pip3 install --no-cache-dir \
    pandas \
    numpy 

# Install dependencies
COPY requirements.txt /app/
RUN pip install -r requirements.txt

COPY . /app/

EXPOSE 8080

# Run the executable
CMD ["python", "api.py"]
