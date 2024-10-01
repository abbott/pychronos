FROM python:3.9-buster
LABEL author="Bruce Abbott (hey@moonmaus.com)"

# Set timezone to Greenwich Mean Time
ENV TZ=GMT
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Add yarn to apt
#RUN curl -sS https://dl.yarnpkg.com/debian/pubkey.gpg | apt-key add -
RUN curl -sS --insecure https://dl.yarnpkg.com/debian/pubkey.gpg | apt-key add -
RUN echo "deb https://dl.yarnpkg.com/debian/ stable main" | tee /etc/apt/sources.list.d/yarn.list

# Install Node and Yarn
RUN apt-get update && apt-get install -y \
    freetds-dev \
    nodejs \
    yarn

# Upgrade pip, setuptools, and wheel to avoid issues with old versions
RUN pip install --upgrade pip setuptools wheel

# Install Cython (required for pymssql) and other Python dependencies
RUN pip install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org cython pymssql


# Copy PyChronos to image
COPY . /app/pychronos

# Build PyChronos UI
WORKDIR /app/pychronos/pychronos-ui
RUN yarn && yarn build

# Set enviroment and expose ports and directories
EXPOSE 5000
VOLUME /pychronos
ENV PYCHRONOS_PATH=/pychronos
ENV PYCHRONOS=yes_sir_docker

# Install Python dependencies
WORKDIR /app/pychronos
RUN pip install -r requirements.txt

ENTRYPOINT ["python", "pychronos.py"]
