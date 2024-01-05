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

ARG USER_NAME=appuser
ARG USER_UID=1000
ARG USER_GID=${USER_UID}

RUN adduser -u ${USER_UID} --disabled-password --gecos "" ${USER_NAME}

USER appuser

WORKDIR /home/${USER_NAME}

RUN curl -sSL https://install.python-poetry.org | python3 -

RUN /home/${USER_NAME}/.local/bin/poetry completions bash >> ~/.bash_completion

RUN /bin/echo -e "\nexport PATH=/home/${USER_NAME}/.local/bin:$PATH:\n" >> /home/${USER_NAME}/.bashrc

COPY docker-entrypoint.sh /
RUN chmod +x /docker-entrypoint.sh

ENTRYPOINT [ "/docker-entrypoint.sh" ]

# The CMD here makes sure the container stays running
# by default. Keeping your startup steps in the ENTRYPOINT
# allows you to safely override the command when using
# docker run with your image or using Docker Compose.

CMD [ "sleep", "infinity" ]
