FROM python:3.7-slim-buster
COPY monitoring.py app/
WORKDIR /app

RUN	apt-get update && apt-get install -y \
	net-tools \
    iputils-ping \
    curl \
	iproute2
RUN pip install Flask APScheduler requests
EXPOSE 5000
ENTRYPOINT ["python3", "monitoring.py"]