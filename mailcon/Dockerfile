FROM python:3.8-slim

RUN apt-get update && apt-get -y install \
  curl \
  less \
  make \
  sudo \
  vim 


ARG UID
ARG GID

# ensure container admin UID/GID matches host
ENV CONSOLE_UID $UID
ENV CONSOLE_GID $GID

RUN groupadd -g $GID admin && \
  useradd -m -s /bin/bash -u $UID -g $GID admin && \
  usermod -aG sudo admin

# disable password for sudo group
RUN echo '%sudo ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers

COPY entrypoint /usr/local/bin

RUN chown -R admin.admin /home/admin
WORKDIR /home/admin

USER admin
COPY profile .profile
COPY bashrc .bashrc
COPY vimrc .vimrc

RUN pip3 install --user --no-warn-script-location \
  click \
  arrow \
  cloudsigma

ENTRYPOINT ["/bin/bash", "-l" ]
