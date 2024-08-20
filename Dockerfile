# This is partly copied from https://docs.docker.com/guides/docker-concepts/building-images/writing-a-dockerfile/

FROM python:3.12
WORKDIR /usr/local/app

# Install the Python dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Install PyLucene (didn't have time to do this in the Dockerfile, but this
# is most of what I did to get it installed on my computer):
# apt-get install default-jdk ant
# mkdir /usr/lib/jvm/default-java/jre
# mkdir /usr/lib/jvm/default-java/jre/lib
# cd /usr/lib/jvm/default-java/jre/lib
# ln -s ../../lib amd64
# mkdir /usr/src/pylucene
# cd /usr/src/pylucene
# curl https://downloads.apache.org/lucene/pylucene/pylucene-9.10.0-src.tar.gz --output pylucene-9.10.0-src.tar.gz
# tar -xz --strip-components=1 -f pylucene-9.10.0-src.tar.gz
# cd jcc
# JCC_JDK=/usr/lib/jvm/default-java python setup.py build
# JCC_JDK=/usr/lib/jvm/default-java python setup.py install
# cd ..
# [edit the Makefile as needed for the given computer]
# make
# make test
# make install

# Copy in the source code
COPY src ./src

# Create an app user so the container doesn't run as the root user
RUN useradd app
USER app

WORKDIR /usr/local/app/src

# Create the Lucene index (this part doesn't work)
#RUN python doc_index.py

EXPOSE 8000
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "api:app"]

