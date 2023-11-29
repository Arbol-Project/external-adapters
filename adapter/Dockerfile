FROM continuumio/miniconda3

# Copy the two files in place and fix different path/locations inside the Docker image


WORKDIR /adapter
COPY ./ ./

COPY root-config /root/
RUN sed 's|/home/runner|/root|g' -i.bak /root/.ssh/config

RUN conda env create -f conda.env.yml

SHELL ["conda", "run", "-n", "arbol-dapp", "/bin/bash", "-c"]

# RUN pip install git+https://${GITHUB_TOKEN}@github.com/Arbol-Project/zarr-client.git
RUN pip install git+ssh://git@github.com/Arbol-Project/zarr-client.git

ENTRYPOINT ["conda", "run", "--no-capture-output", "-n", "arbol-dapp", "gunicorn", "--worker-class", "gevent", "--workers", "2", "--bind", "0.0.0.0:8000", "wsgi:app", "--log-level", "info"]