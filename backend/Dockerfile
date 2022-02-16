FROM python:3.10

RUN adduser --system --group --no-create-home app

COPY . /app
WORKDIR /app

RUN pip install --upgrade pip

# Install dependencies
RUN pip install -r requirements.txt

RUN chown -R app:app /app

USER app

#COPY . /app/

#EXPOSE 8080

# Run the executable
#CMD ["python", "api.py"]
