FROM ompc-build
ARG BUILD_DIR
ADD $BUILD_DIR /ompc/build
ENV BUILD_DIR=/ompc/build

ADD get_task_bench.sh /
RUN . /get_task_bench.sh 
