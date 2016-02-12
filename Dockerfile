FROM debian:jessie
MAINTAINER PotHix
RUN ls -lah
RUN apt-get update
RUN apt-get install -y --force-yes build-essential python make
RUN make -f dev.makefile create_env

EXPOSE 8081

CMD ["make", "-f", "dev.makefile", "server"]
