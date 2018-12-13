.PHONY: default
default: all ;

REPO_ROOT = $(abspath ../..)

wheels-x64:
	docker run --rm -v ${REPO_ROOT}:/io quay.io/pypa/manylinux1_x86_64 /io/tools/manylinux-build/build-wheels.sh

wheels-x86:
	docker run --rm -v ${REPO_ROOT}:/io quay.io/pypa/manylinux1_i686 /io/tools/manylinux-build/build-wheels.sh

wheels: wheels-x64 wheels-x86

pull-x64:
	docker pull quay.io/pypa/manylinux1_x86_64

pull-x86:
	docker pull quay.io/pypa/manylinux1_i686

pull: pull-x64 pull-x86

all: pull wheels
