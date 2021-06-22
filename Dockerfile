FROM python:3.8-alpine

WORKDIR /app

# Install the required dependencies
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

# Copy all files into the workdir
COPY . .

# Run the Discord bot
CMD ["python3", "main.py"]
