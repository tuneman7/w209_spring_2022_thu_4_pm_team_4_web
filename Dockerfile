# FROM nvidia/cuda
# FROM nvidia/cuda:8.0-cudnn6-devel
# FROM nvidia/cuda:8.0-cudnn5-devel
FROM ubuntu

RUN apt-get update \
  && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    git \
    python3-pip \
    python-setuptools \
    python-dev-is-python3 \
  && rm -rf /var/lib/apt/lists/*

RUN pip3 install h5py pandas
RUN pip3 install theano

RUN pip3 install --upgrade -I setuptools \
  && pip3 install --upgrade \
    keras

RUN pip3 install  \
    matplotlib \
    seaborn

RUN pip3 install scikit-learn tables
RUN pip3 install --upgrade pip
RUN pip3 install 'ipython<6'

RUN pip3 install jupyter

VOLUME /notebook
WORKDIR /notebook
EXPOSE 8888

ENV KERAS_BACKEND=theano

#  CMD jupyter notebook --no-browser --ip=0.0.0.0 --NotebookApp.token= --allow-root
CMD jupyter notebook --no-browser --ip=0.0.0.0 --allow-root