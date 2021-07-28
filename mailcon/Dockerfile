FROM alpine:3.14

RUN apk update && apk add \
  mandoc \
  less less-doc \
  vim vim-doc \
  curl curl-doc \
  unzip unzip-doc \
  bash bash-doc \
  sudo sudo-doc \
  make make-doc \
  openssh openssh-doc \
  python3 py3-pip

RUN pip3 install cloudsigma click

ARG UID
ARG GID
RUN curl -L https://releases.hashicorp.com/terraform/1.0.3/terraform_1.0.3_linux_amd64.zip --output terraform.zip && \
  unzip terraform.zip && \
  mv terraform /usr/local/bin

ENV CONSOLE_UID $UID
ENV CONSOLE_GID $GID

RUN adduser -D -h /home/admin -s /bin/bash -u $UID -g $GID admin && \
  addgroup sudo && \
  adduser admin sudo

RUN echo '%sudo ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers

COPY entrypoint /usr/local/bin
ENTRYPOINT entrypoint
CMD bash -l

WORKDIR /home/admin
USER admin
