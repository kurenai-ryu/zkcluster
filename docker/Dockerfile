# Pull base image
FROM python:3.6-slim

# Set environment varibles
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /code

# Copy install
COPY Pipfile /code/

# Install dependencies
RUN apt-get update && apt-get install -y iputils-ping \
	&& savedAptMark="$(apt-mark showmanual)" \
	&& apt-get install -y --no-install-recommends git \
	&& pip install --upgrade pip \
	&& pip install pipenv \
	&& pipenv install --deploy --system --skip-lock --dev \
	&& apt-mark auto '.*' > /dev/null \
	&& apt-mark manual $savedAptMark \
	&& apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
	&& rm -rf /var/lib/apt/lists/* 

#copy base files
COPY docker/django-simple/ /code/

COPY zkcluster/ /code/zkcluster/
#develop: volume on /code/zkcluster


#first generate new secret
RUN python manage.py generate_secret_key --replace 

