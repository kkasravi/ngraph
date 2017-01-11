DIR = $(realpath ../..)
VOLUME = -v ${DIR}:/root/private-ngraph -v $$HOME/nervana/data:/root/nervana/data

# default version is python 2, but can be switched to 3 from command
# line
PYTHON_VERSION = 2

.PHONY: build_test test build_base build_dev

build_base:
	@docker build -f=Dockerfile.base --build-arg python_version=${PYTHON_VERSION} -t=ngraph_base ${DIR}

build_dev: build_base
	@docker build -f=Dockerfile.dev -t=ngraph_dev ${DIR}

build_test: build_base
	@docker build -f=Dockerfile.test -t=ngraph_test ${DIR}

build_doc: build_base
	@docker build -f=Dockerfile.doc -t=ngraph_doc ${DIR}

test: build_test
	@echo docker run --rm ${VOLUME} -t ngraph_test make test
	@echo ${NGRAPH_DATA_DIR}
	@docker run --rm ${VOLUME} -t ngraph_test make test

test_gpu: build_test
	@nvidia-docker run --rm ${VOLUME} -t ngraph_test make test

doc: build_doc
	@docker run --rm ${VOLUME} -t ngraph_doc make doc

style: build_test
	@docker run --rm ${VOLUME} -t ngraph_test make style

test_shell: build_test
	@docker run --rm ${VOLUME} -it ngraph_test /bin/bash

shell: build_dev
	@docker run --rm ${VOLUME} -it ngraph_dev /bin/bash

all: style doc test test_gpu