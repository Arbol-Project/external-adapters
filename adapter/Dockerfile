FROM continuumio/miniconda3

# ARG GITHUB_TOKEN
WORKDIR /adapter
COPY ./ ./

RUN conda env create -f conda.env.yml

SHELL ["conda", "run", "-n", "arbol-dapp", "/bin/bash", "-c"]

RUN conda install pip
# RUN pip install git+https://${GITHUB_TOKEN}@github.com/Arbol-Project/zarr-client.git
RUN pip install git+https://github.com/Arbol-Project/zarr-client.git

ENTRYPOINT ["conda", "run", "--no-capture-output", "-n", "arbol-dapp", "gunicorn", "--worker-class", "gevent", "--workers", "2", "--bind", "0.0.0.0:8000", "wsgi:app", "--log-level", "info"]