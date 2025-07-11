FROM mcr.microsoft.com/vscode/devcontainers/python:0-3.10

COPY app/requirements.txt requirements.txt
COPY app/requirements-dev.txt requirements-dev.txt

RUN pip install --no-cache-dir \
    -r app/requirements-dev.txt \
    && rm -rf /tmp/pip-tmp