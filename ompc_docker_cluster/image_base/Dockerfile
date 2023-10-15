FROM ompc-runtime-moheft
#RUN useradd -ms /bin/bash mpiuser
#RUN usermod -aG sudo mpiuser
#USER mpiuser
#WORKDIR /home/mpiuser
#RUN mkdir .ssh && chmod 0700 .ssh
#USER root
RUN mkdir /root/.ssh
ADD id_rsa /root/.ssh
ADD id_rsa.pub /root/.ssh/
WORKDIR /root/.ssh
RUN cat id_rsa.pub >> authorized_keys && rm -f id_rsa.pub
RUN echo "Host *" >> ~/.ssh/config && echo "    StrictHostKeyChecking no" >> ~/.ssh/config
RUN apt install iproute2 iputils-ping -y
WORKDIR /
CMD eval `ssh-agent` && ssh-add /root/.ssh/id_rsa && service ssh start && . /ompc/set-clang.ssh && /bin/bash 

