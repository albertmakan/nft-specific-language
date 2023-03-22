---
sidebar_position: 1
---

# Setup SPM

Let's get you started by installing `SPM Toolkit` toolkit. `SPM Toolkit` can be used in several ways, using `Docker` or `Python`.

## Running using Docker

:::note
It's worthwhile noting that we support running SPM in a [Dev Container](https://code.visualstudio.com/docs/devcontainers/containers).
:::

### Using Dockerfile

```dockerfile
FROM python:3.9-alpine

RUN apk add --update --no-cache --virtual .tmp-build-deps \
    gcc libc-dev linux-headers postgresql-dev \
    && apk add libffi-dev

WORKDIR /app
COPY . .

RUN python -m pip install --upgrade pip
RUN pip3 install textX[dev]
RUN pip3 install py-solc-x
RUN pip3 install solidity_parser
RUN pip3 install jsonmerge
RUN pip3 install starkbank-ecdsa

RUN pip3 install pygls
RUN pip install --force-reinstall -v "lsprotocol==2022.0.0a10"

RUN pip3 install -e src/spm
RUN pip3 install -e src/spmgen
RUN pip3 install -e src/spl
RUN pip3 install -e src/splgen
RUN pip3 install -e src/spm-cli
RUN pip3 install -e src/spl-cli

# install npm for extension compile
RUN apk add --update npm

# install git
RUN apk update
RUN apk add git

# install bash
RUN apk add --no-cache bash

# install starship
RUN apk add starship
RUN echo 'eval "$(starship init bash)"' >> ~/.bashrc
```

:::info
You can build your Docker image using [`docker build`](https://docs.docker.com/engine/reference/commandline/build/) command.
:::

### Using a prebuilt Docker image

`SPM Toolkit` comes prebuilt in a docker image and is hosted on our custom registry.

```bash
docker run -dit cr.bjelicaluka.com/spm-toolkit --name spm-toolkit
```

## Using Python on your Local Machine

You can install all required tools by running the following command:

```bash
pip install https://github.com/albertmakan/nft-specific-language/archive/develop.zip
```

## Check if SPM Toolkit works

To check if `SPM Toolkit` is successfully installed, run the following command:

```bash
spm --help
```

The expected output should be something similar to:

```bash
Usage: spm [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  deploy
  init
  install
  pack
  version
```

:::caution
If you get something similar to: `zsh: command not found: spm`, that means that `SPM Toolkit` is not set up correctly!
:::