# alx-backend-python/messaging_app/Dockerfile

# Base image
FROM python:3.10

# Set work directory inside container
WORKDIR /app

# Copy requirements and install them
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy entire app source code into container
COPY . .

# Expose the Django port
EXPOSE 8000

# Run the Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
