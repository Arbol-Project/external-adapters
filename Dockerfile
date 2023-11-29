FROM --platform=linux/amd64 continuumio/miniconda3

WORKDIR /adapter
COPY ./adapter ./
COPY ./zarr-client ../zarr-client

RUN conda env create -f conda.env.yml

SHELL ["conda", "run", "-n", "arbol-dapp", "/bin/bash", "-c"]

RUN pip install ../zarr-client/

RUN conda list

ENTRYPOINT ["conda", "run", "--no-capture-output", "-n", "arbol-dapp", "gunicorn", "--worker-class", "gevent", "--workers", "2", "--bind", "0.0.0.0:8000", "wsgi:app", "--log-level", "info"]