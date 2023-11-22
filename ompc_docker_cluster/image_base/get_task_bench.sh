#!/bin/bash

git clone https://gitlab.com/ompcluster/task-bench.git
cd task-bench
git merge remotes/origin/fix/openmp-driver

DEFAULT_FEATURES=0 USE_LEGION=0 USE_OMPCLUSTER=1 ./get_deps.sh

. /ompc/set-clang.ssh
export CC=clang
export CXX=clang++

./build_all.sh
