FROM ompc-build
ARG BUILD_DIR
ADD $BUILD_DIR /ompc/build
RUN export PATH=$BUILD_DIR/bin/:$PATH
RUN export LD_LIBRARY_PATH=$BUILD_DIR/lib/:$LD_LIBRARY_PATH
RUN export LIBRARY_PATH=$BUILD_DIR/lib/:$LIBRARY_PATH
RUN export CPATH=$BUILD_DIR/projects/openmp/runtime/src:$CPATH
