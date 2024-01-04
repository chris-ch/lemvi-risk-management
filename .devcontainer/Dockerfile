# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.10-slim

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Install GitHub
RUN apt-get update && \
    apt-get install -y git curl && \
    pip3 install jupyter

WORKDIR /app
COPY . /app


ARG USER_NAME=appuser
ARG USER_UID=5678
ARG USER_GID=${USER_UID}

# Creates a non-root user with an explicit UID and adds permission to access the /workspace folder
# For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
RUN mkdir /workspace
RUN adduser -u ${USER_UID} --disabled-password --gecos "" ${USER_NAME} && chown -R ${USER_NAME} /workspace

USER appuser

WORKDIR /home/${USER_NAME}

RUN curl -sSL https://install.python-poetry.org | python3 -
RUN /bin/echo -e "\nexport PATH=/home/${USER_NAME}/.local/bin:$PATH:\n" >> /home/${USER_NAME}/.bashrc

EXPOSE 8888                                           
CMD ["/bin/bash"]
