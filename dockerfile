FROM nvidia/cuda:12.1.0-devel-ubuntu20.04

# Install Python
RUN apt-get update && \
    apt-get install -y python3-pip python3-dev && \
    rm -rf /var/lib/apt/lists/*

COPY . server
WORKDIR server

# Install requreimtnes
RUN pip install -r requirements.txt --no-cache-dir

# clean up
RUN rm -rf /root/.cache
RUN apt-get remove -y --purge python3-pip