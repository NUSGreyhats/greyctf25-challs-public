# Use Java 11 runtime
FROM openjdk:11-jre-slim

# Working dir inside container
WORKDIR /app

COPY ./lpmc-server ./lpmc-server

WORKDIR /app/lpmc-server 
RUN apt-get update
RUN apt-get install -y curl
RUN rm -rf /var/lib/apt/lists/*
RUN chmod +x run.sh
CMD ["./run.sh"]