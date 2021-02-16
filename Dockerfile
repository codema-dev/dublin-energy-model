FROM nrel/energyplus:8.9.0 AS builder

FROM python:3.9-slim
COPY ./environment.yml /tmp/environment.yml

ENV ENERGYPLUS_INSTALL_VERSION=8-9-0

COPY --from=builder /usr/local/bin /usr/local/bin
COPY --from=builder \
  /usr/local/EnergyPlus-$ENERGYPLUS_INSTALL_VERSION \
  usr/local/EnergyPlus-$ENERGYPLUS_INSTALL_VERSION

# Add Tini. Tini operates as a process subreaper for jupyter. This prevents kernel crashes.
ENV TINI_VERSION v0.19.0
ADD https://github.com/krallin/tini/releases/download/${TINI_VERSION}/tini /tini
RUN chmod +x /tini
RUN echo 'alias jnbook="jupyter notebook --port=8888 --no-browser --ip=0.0.0.0 --allow-root"' >> ~/.profile

ENV PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  POETRY_VERSION=1.1.4
RUN pip install "poetry==$POETRY_VERSION"

COPY poetry.lock pyproject.toml .
RUN poetry config virtualenvs.create false \
  && poetry install $(test "$YOUR_ENV" == production && echo "--no-dev") --no-interaction --no-ansi

ENTRYPOINT ["/bin/bash"]
