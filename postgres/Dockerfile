FROM postgres 
ENV POSTGRES_PASSWORD postgres 
ENV POSTGRES_DB testdb 
RUN apt-get -y -qq update && \
	apt-get install -y -qq curl && \
	apt-get clean
#
# install jq to parse json within bash scripts
RUN curl -o /usr/local/bin/jq http://stedolan.github.io/jq/download/linux64/jq && \
  chmod +x /usr/local/bin/jq

COPY output.csv .
COPY init.sql /docker-entrypoint-initdb.d/


