FROM continuumio/miniconda3

# Copy the two files in place and fix different path/locations inside the Docker image
ARG GITHUB_WORKSPACE

WORKDIR /adapter
COPY ./ ./

RUN conda env create -f conda.env.yml

SHELL ["conda", "run", "-n", "arbol-dapp", "/bin/bash", "-c"]

# RUN pip install git+https://${GITHUB_TOKEN}@github.com/Arbol-Project/zarr-client.git
RUN echo ${GITHUB_WORKSPACE}
RUN pip install /${GITHUB_WORKSPACE}/zarr-client/

ENTRYPOINT ["conda", "run", "--no-capture-output", "-n", "arbol-dapp", "gunicorn", "--worker-class", "gevent", "--workers", "2", "--bind", "0.0.0.0:8000", "wsgi:app", "--log-level", "info"]