FROM python:3.10-slim-bullseye

# Install base utilities
RUN apt-get update && \
    apt-get install -y build-essential  && \
    apt-get install -y wget && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install miniconda
ENV CONDA_DIR /opt/conda
RUN wget --quiet https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda.sh && \
     /bin/bash ~/miniconda.sh -b -p /opt/conda

# Put conda in path so we can use conda activate
ENV PATH=$CONDA_DIR/bin:$PATH
RUN mkdir /app
RUN mkdir /app/papwikires
RUN mkdir /data
RUN chmod -R 777 /data

#COPY environment.yml /app
COPY papwikires /app/papwikires
COPY setup.cfg /app
COPY setup.py /app
WORKDIR app
RUN python setup.py install
