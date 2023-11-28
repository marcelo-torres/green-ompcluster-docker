FROM ubuntu:20.04

RUN apt-get update && apt-get install -y locales && rm -rf /var/lib/apt/lists/* \
	&& localedef -i pt_BR -c -f UTF-8 -A /usr/share/locale/locale.alias pt_BR.UTF-8

RUN apt update
RUN apt-get update

# MPI + CLANG
RUN apt install cmake -y 
RUN apt install libelf-dev libffi-dev -y
RUN apt install mpich libmpich-dev -y
RUN apt install python3 -y 
RUN apt install clang -y 
RUN apt install ccache -y
RUN apt install ninja-build
RUN apt install libencode-locale-perl -y

RUN apt install git -y
RUN apt install jq -y

# OMPCH BENCH

RUN apt install pip -y
RUN git clone https://gitlab.com/ompcluster/ompcbench.git
RUN cd ompcbench
RUN apt install python3-dev graphviz libgraphviz-dev pkg-config -y
RUN pip install virtualenv
RUN apt install graphviz -y
RUN pip install virtualenv

# Use "source venv/bin/activate" do access de virtual env
RUN cd /ompcbench && python3 -m virtualenv venv && venv/bin/pip install -e ".[dev]"


RUN apt install nano -y

RUN mkdir /ompc/
ADD compile-llvm.ssh /ompc/
ADD set-clang.ssh /ompc/