# Green OMPC

This repository supports the experiments presented in the paper Reducing carbon emissions of distributed systems: a multi-objective approach.

The [OpenMP Cluster (OMPC)](https://doi.org/10.1145/3547276.3548444) allows developers to create distributed applications using the well-known OpenMP API, a specification for parallel programming.

The OMPC uses the OpenMP computation offloading technique to schedule tasks through the MPI programming model. The original OMPC implementation is available in the LLVM Compiler Infrastructure Project.

We fork the LLVM project to extend OMPC with new scheduling algorithms: [MOHEFT](https://doi.org/10.1109/CloudCom.2012.6427573), G-MOHEFT (Green MOHEFT), and a new implementation of HEFT. The G-MOHEFT is a green energy-aware algorithm based on the multi-objective scheduling algorithm MOHEFT.

## Repository

The repository is organized as follows:

**experiment:** _Scripts and files to support the experiment execution._

**ompc_docker_cluster:** _A local cluster built with Docker containers. Scripts to get tasks' durations using a cluster node are implemented here._
 
**ompc_docker_compile:** _The docker image definition to compile LLVM._

**ompc_docker_runtime:** _The docker image definition to run the compiled LLVM._

**photovolta:** _Solar energy traces from Photavolta project and scripts to transform data._

## Compile

The following steps explain how to compile the LLVM  project extended by us and how to reproduce the experiments.

### 1. Create the OMPC build container image
```shell
cd ompc_docker_compile && docker build -t ompc-build .
cd ..
```

### 2. Create the build container
```shell
docker run --name ompc-build -v $PWD:/ompc/volume \
    --env WORK_DIR=/ompc/volume/ompc_docker_runtime/project \
    --env BUILD_DIR=/ompc/volume/ompc_docker_runtime/project/build \
    --env PROJECT_DIR=llvm-project-moheft \
    --env GIT_REPOSITORY=https://gitlab.com/gui.alm02/llvm-project-moheft.git \
    --env GIT_BRANCH=main \
    -it ompc-build
```

### 3. Execute build inside the container 
```shell
. ompc/compile-llvm.ssh
exit
```

### 4. Create OMPC runtime
```shell
cd ompc_docker_runtime && docker build -t ompc-runtime-gmoheft --build-arg BUILD_DIR=./project/build .
cd ..
```

### 5. Run experiments
```shell
docker run --name ompc-experiment -v $PWD:/ompc/volume -it ompc-runtime-gmoheft
```

