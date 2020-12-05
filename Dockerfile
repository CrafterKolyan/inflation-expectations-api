FROM continuumio/anaconda3 AS build

ARG renderer_queue
ARG demo_queue
ARG rmq_connect

RUN apt-get update; apt-get install -y apt-utils software-properties-common; add-apt-repository ppa:ubuntu-toolchain-r/test -y; add-apt-repository ppa:acooks/libwebsockets6 -y; apt-get update; apt-get install build-essential -y && apt-get install --fix-missing gcc-8 g++-8 -y &&  update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-8 60 --slave /usr/bin/g++ g++ /usr/bin/g++-8 && update-alternatives --config gcc; apt-get install git git-flow -y; apt-get install wget -y; apt-get install libblas-dev liblapack-dev ccache libssl-dev zlib1g-dev pkg-config libuv1.dev libomp-dev -y


RUN wget -q https://github.com/Kitware/CMake/releases/download/v3.14.5/cmake-3.14.5-Linux-x86_64.sh; sh ./cmake-3.14.5-Linux-x86_64.sh --skip-license --include-subdir; cd cmake-3.14.5-Linux-x86_64; cp -r bin /usr/; cp -r share /usr/; cp -r doc /usr/share/; cp -r man /usr/share/; cd ../; rm -rf cmake-3.14.5-Linux-x86_64; rm -f cmake-3.14.5-Linux-x86_64.sh; git clone https://github.com/google/googletest && cd googletest; mkdir build; cd build; cmake .. && make -j 4; make install && cd /tmp; rm -rf googletest;

RUN git clone https://github.com/maks5507/amqp-interface.git; cd amqp-interface; python setup.py build; pip install .;
RUN git clone https://github.com/bigartm/bigartm; cd bigartm; mkdir build; cd build; cmake ..; make install;


COPY . /root/

RUN pip install -r /root/requirements.txt
RUN python /root/setup/init_amqp.py -c $rmq_connect -rq $renderer_queue -dq $demo_queue
