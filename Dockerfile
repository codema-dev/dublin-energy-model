FROM nrel/energyplus:8.9.0 AS builder

# Pull from continium as per CEA
FROM python:3.9-slim-buster

ENV ENERGYPLUS_INSTALL_VERSION=8-9-0

COPY --from=builder /usr/local/bin /usr/local/bin
COPY --from=builder /usr/local/EnergyPlus-$ENERGYPLUS_INSTALL_VERSION usr/local/EnergyPlus-$ENERGYPLUS_INSTALL_VERSION

# Add Tini. Tini operates as a process subreaper for jupyter. This prevents kernel crashes.
ENV TINI_VERSION v0.19.0
ADD https://github.com/krallin/tini/releases/download/${TINI_VERSION}/tini /tini
RUN chmod +x /tini
RUN echo 'alias jnbook="jupyter notebook --port=8888 --no-browser --ip=0.0.0.0 --allow-root"' >> ~/.bashrc

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
