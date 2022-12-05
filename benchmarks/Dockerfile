FROM thekevjames/nox:latest

RUN curl -fsSo /tmp/pypy3 https://downloads.python.org/pypy/pypy3.9-v7.3.9-linux64.tar.bz2 && \
    tar xf /tmp/pypy3 --director /opt && \
    ln -s /opt/pypy3.9-v7.3.9-linux64/bin/pypy3.9 /usr/bin/pypy3.9 && \
    rm /tmp/pypy3


# docker build . -t viblo/pymunk-bench:2022.12.01    
