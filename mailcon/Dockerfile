FROM python:3.8-slim

RUN apt-get update && apt-get -y install \
  curl \
  jq \
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

WORKDIR /home/admin

COPY profile .profile
COPY bashrc .bashrc
COPY vimrc .vimrc
COPY src ./src

RUN find /home/admin

RUN chown -R admin.admin /home/admin

USER admin

RUN \
  python -m venv .venv && \
  . .venv/bin/activate && \
  python -m pip install -U pip && \
  cd /home/admin/src &&  \
  pip --use-feature=in-tree-build install .

ENTRYPOINT ["/usr/bin/env", "/usr/local/bin/entrypoint"]
CMD ["list", "servers"]
