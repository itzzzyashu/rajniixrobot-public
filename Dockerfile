# Python Based Docker
FROM python:3.10.6

WORKDIR /app
COPY . /app

# Install system dependencies in one layer
RUN apt update && apt upgrade -y && apt install git gcc python3-dev netcat -y \
    && python -m pip install pip==22 setuptools ez_setup \
    && pip install --upgrade -r requirements.txt

# Command to run the application
CMD ["/bin/bash", "/app/start.sh"]