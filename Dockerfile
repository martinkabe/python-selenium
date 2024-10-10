# Use the official Python image.
FROM python:3.9

# https://googlechromelabs.github.io/chrome-for-testing/
ENV CHROMEDRIVER_VERSION=129.0.6668.100

### install chrome
RUN apt-get update && apt-get install -y wget && apt-get install -y zip
RUN wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN apt-get install -y ./google-chrome-stable_current_amd64.deb

### install chromedriver
RUN wget https://storage.googleapis.com/chrome-for-testing-public/${CHROMEDRIVER_VERSION}/linux64/chromedriver-linux64.zip \
  && unzip chromedriver-linux64.zip && rm -dfr chromedriver_linux64.zip \
  && mv /chromedriver-linux64/chromedriver /usr/bin/chromedriver \
  && chmod +x /usr/bin/chromedriver

# Install Python dependencies
COPY requirements.txt requirements.txt
RUN pip install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org --no-cache-dir -r requirements.txt

# Copy local code to the container image
ENV APP_HOME=/app
WORKDIR $APP_HOME
COPY . .

# Run the web service on container startup
# CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 main:app
CMD ["sh", "-c", "gunicorn --bind 0.0.0.0:$PORT --workers 1 --threads 8 main:app"]
