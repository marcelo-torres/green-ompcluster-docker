FROM ompc-runtime-moheft

# SSH 
RUN apt install openssh-server -y
RUN apt install ufw -y
RUN systemctl enable ssh

RUN mkdir /root/.ssh
ADD id_rsa /root/.ssh
ADD id_rsa.pub /root/.ssh/
RUN chmod 0700 /root/.ssh/*
WORKDIR /root/.ssh
RUN cat id_rsa.pub >> authorized_keys && rm -f id_rsa.pub
RUN echo "Host *" >> ~/.ssh/config && echo "    StrictHostKeyChecking no" >> ~/.ssh/config
RUN apt install iproute2 iputils-ping -y
WORKDIR /
ADD get_task_bench.sh /
RUN . /get_task_bench.sh 
CMD eval `ssh-agent` && ssh-add /root/.ssh/id_rsa && service ssh start && . /ompc/set-clang.ssh && /bin/bash 

