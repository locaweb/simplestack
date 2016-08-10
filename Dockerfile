FROM docker-registry.locaweb.com.br/jessie/python-dev:2.7
MAINTAINER PotHix

# libvirt is needed
RUN apt-get update && apt-get install -y --force-yes python-libvirt

RUN mkdir -p /simplestack
WORKDIR /simplestack

EXPOSE 8081
VOLUME /simplestack

CMD ["make", "-f", "dev.makefile", "vendor"]
