#!/bin/bash
set -e -x

SUPPORTED_PYTHONS="cp37-cp37m"

ls -la /io

# Compile wheels
for PYVER in $SUPPORTED_PYTHONS; do
    rm -rf /io/Setup /io/build/
    PYBIN="/opt/python/${PYVER}/bin"
    cd /io
    ${PYBIN}/pip install -r "docs/requirements.txt"
    ${PYBIN}/python setup.py build_sphinx bdist_wheel -d wheelhouse/
done

# Bundle external shared libraries into the wheels
for whl in wheelhouse/pymunk*.whl; do
    auditwheel repair $whl -w /io/tools/manylinux-build/wheelhouse/
done

# Dummy options for headless testing
export SDL_AUDIODRIVER=disk
export SDL_VIDEODRIVER=dummy

# Install packages and test
for PYVER in $SUPPORTED_PYTHONS; do
    PYBIN="/opt/python/${PYVER}/bin"
    ${PYBIN}/pip install "cffi<=1.13"
    ${PYBIN}/pip install pymunk \
      --no-index -f /io/tools/manylinux-build/wheelhouse
    (cd $HOME; ${PYBIN}/python -m pymunk.tests)
done

echo "Here are the binary wheels for linux:"
ls /io/tools/manylinux-build/wheelhouse
