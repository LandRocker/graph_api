FROM python:3.10-slim-buster

WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Install gunicorn for production
RUN pip install gunicorn

# Copy the rest of the application code
COPY . .

# Set environment variables
ARG FLASK_ENV=production
ENV FLASK_ENV=${FLASK_ENV}

# Expose the application port
EXPOSE 5000

# Default command for development
CMD if [ "$FLASK_ENV" = "development" ]; \
    then flask run --host=0.0.0.0 --reload; \
    else gunicorn -w 4 -b 0.0.0.0:5000 app:app; \
    fi


