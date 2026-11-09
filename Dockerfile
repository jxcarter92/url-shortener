FROM python:3.13-slim
WORKDIR /usr/local/app

# Install the application dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

RUN apt-get update && apt-get upgrade -y && rm -rf /var/lib/apt/lists/*

#uninstall pip
RUN pip uninstall -y pip

# Copy in the source code
COPY app.py ./
EXPOSE 5000

# Setup an app user so the container doesn't run as the root user
RUN useradd app
USER app

CMD ["python", "app.py"]