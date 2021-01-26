FROM nrel/energyplus:8.9.0 AS builder

FROM continuumio/miniconda3
COPY ./environment.yml /tmp/environment.yml

# create the conda environment and install 
RUN conda env create -q -f /tmp/environment.yml -n eppy
ENV PATH /opt/conda/envs/eppy/bin:$PATH

ENV ENERGYPLUS_INSTALL_VERSION=8-9-0

COPY --from=builder /usr/local/bin /usr/local/bin
COPY --from=builder /usr/local/EnergyPlus-$ENERGYPLUS_INSTALL_VERSION usr/local/EnergyPlus-$ENERGYPLUS_INSTALL_VERSION
RUN pip install notebook==6.1.5 eppy==0.5.53

# Add Tini. Tini operates as a process subreaper for jupyter. This prevents kernel crashes.
ENV TINI_VERSION v0.19.0
ADD https://github.com/krallin/tini/releases/download/${TINI_VERSION}/tini /tini
RUN chmod +x /tini

ENTRYPOINT source /eppy/bin/activate

CMD ["zsh"]

RUN echo 'alias jnbook="jupyter notebook --port=8888 --no-browser --ip=0.0.0.0 --allow-root"' >> ~/.bashrc
