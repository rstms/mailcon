FROM alpine:3.14

RUN apk update && apk add \
  mandoc \
  bash bash-doc \
  curl curl-doc \
  doas doas-doc \
  figlet figlet-doc \
  less less-doc \
  make make-doc \
  openssh openssh-doc \
  python3 py3-pip \
  unzip unzip-doc \
  vim vim-doc

RUN rm /usr/bin/vi && ln -s /usr/bin/vim /usr/bin/vi


RUN pip3 install \
  click \
  arrow \
  cloudsigma

ARG UID
ARG GID

# install terraform
#RUN curl -L https://releases.hashicorp.com/terraform/1.0.3/terraform_1.0.3_linux_amd64.zip --output terraform.zip && \
#  unzip terraform.zip && \
#  mv terraform /usr/local/bin

# ensure container admin UID/GID matches host
ENV CONSOLE_UID $UID
ENV CONSOLE_GID $GID

RUN adduser -D -h /home/admin -s /bin/bash -u $UID -g $GID admin && adduser admin wheel

RUN echo 'permit nopass keepenv :wheel' >/etc/doas.conf

COPY entrypoint /usr/local/bin

RUN chown -R admin.admin /home/admin
WORKDIR /home/admin

USER admin
COPY profile .profile
COPY bashrc .bashrc
COPY vimrc .vimrc

ENTRYPOINT entrypoint
CMD bash -l
