## Template

https://dev.to/googlecloud/using-headless-chrome-with-cloud-run-3fdp

## Install required packages

pip install --default-timeout=100 --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org -r requirements.txt

pip install --default-timeout=100 --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org Jinja2

pip install --default-timeout=100 --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org webdriver-manager

pip freeze > requirements.txt

## Testing and deploying

docker build -t my_screenshot_service:latest .

docker run --rm -p 8090:8080 -e PORT=8080 my_screenshot_service:latest

Then run in browser
http://localhost:8090/

## Deploy it directly to Cloud Run

gcloud builds submit --tag gcr.io/YOUR_PROJECT/my_screenshot_service

gcloud beta run deploy my_screenshot_service --image gcr.io/YOUR_PROJECT/my_screenshot_service --region us-central1 --platform managed

## Check docker image

docker run -it my_screenshot_service bash
