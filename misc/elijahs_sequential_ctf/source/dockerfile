# Use the existing image as base
FROM pintia/ljudge-docker:7469cbb AS app

# Optional: switch to root to ensure permission
USER root

RUN ln -sf $(which python3) $(which python2)

RUN apt-get update && apt-get install -y socat

COPY ./ /

RUN chmod 555 /server.py

# Set working directory
WORKDIR /workspace

USER judger 
CMD socat TCP-LISTEN:5000,reuseaddr,fork EXEC:"python3 /server.py",stderr