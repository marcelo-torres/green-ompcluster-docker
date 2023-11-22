#!/bin/sh

prefix="experiment_beluga_server"
separator="_"

HOST_FILE="./ompc-host-file"



ConfigureLocalNetwork() {
    local proxy=$1
    local -n containers=$2
    local current_network=$3
    local -n target_networks=$4
    
    local current_network_full_name="$prefix"_"$current_network"
    local proxy_container="$prefix""$separator""$proxy"
    local proxy_ip=$(docker inspect -f "{{ .NetworkSettings.Networks.$current_network_full_name.IPAddress }}" $proxy_container)
    
    for i in "${!target_networks[@]}"
    do
        local target_network=${target_networks[$i]}
        local network_full_name="$prefix"_"$target_network"
        local network_subnet=$(docker network inspect $network_full_name -f '{{range .IPAM.Config}}{{.Subnet}}{{end}}')
        
        for j in "${!containers[@]}"
        do
           local container_name=${containers[$j]}
           local container_full_name="$prefix""$separator""$container_name"
           
           echo "Connecting $container_name to $target_network ($network_subnet) via $proxy ($proxy_ip)"
           docker exec $container_full_name ip route add $network_subnet dev eth0 via $proxy_ip dev eth0
        done
    done
    
    
}

ConfigureProxy() {
    local proxy=$1
    local global_network=$2
    local -n target_proxies=$3
    local -n target_networks=$4

    local proxy_container="$prefix""$separator""$proxy"
    local global_network_full_name="$prefix""_""$global_network"

    for i in "${!target_networks[@]}"
    do
        local target_network=${target_networks[$i]}
        local network_full_name="$prefix"_"$target_network"
        local network_subnet=$(docker network inspect $network_full_name -f '{{range .IPAM.Config}}{{.Subnet}}{{end}}')
        
        local target_proxy=${target_proxies[$i]}
        local target_proxy_full_name="$prefix""$separator""$target_proxy"
        local proxy_global_ip=$(docker inspect -f "{{ .NetworkSettings.Networks.$global_network_full_name.IPAddress }}" $target_proxy_full_name)
        
        echo "Connecting $proxy to $target_network ($network_subnet) via $target_proxy ($proxy_global_ip)"
        docker exec $proxy_container ip route add $network_subnet dev eth0 via $proxy_global_ip dev eth1
    done   
}

ConfigureHeadNetwork() {
    local head=$1
    local global_network=$2
    local -n target_proxies=$3
    local -n target_networks=$4
    
    local head_container="$prefix""$separator""$head"
    local global_network_full_name="$prefix""_""$global_network"

    for i in "${!target_networks[@]}"
    do
        local target_network=${target_networks[$i]}
        local network_full_name="$prefix"_"$target_network"
        local network_subnet=$(docker network inspect $network_full_name -f '{{range .IPAM.Config}}{{.Subnet}}{{end}}')
        
        local target_proxy=${target_proxies[$i]}
        local target_proxy_full_name="$prefix""$separator""$target_proxy"
        local proxy_global_ip=$(docker inspect -f "{{ .NetworkSettings.Networks.$global_network_full_name.IPAddress }}" $target_proxy_full_name)
    
        echo "Connecting $head to $target_network ($network_subnet) via $target_proxy ($proxy_global_ip)"
        docker exec $head_container ip route add $network_subnet dev eth0 via $proxy_global_ip dev eth0
    done
}



WriteContainerIpToHostFile () {
    local container=$1
    local network=$2
    local ranks=$3
    
    local container_full_name="$prefix""$separator""$container"
    local network_full_name="$prefix"_"$network"
    
    local ip=$(docker inspect -f "{{ .NetworkSettings.Networks.$network_full_name.IPAddress }}" $container_full_name)
    echo "($network) $container: $ip"
    
    if [ -z "$ranks" ]
    then
        echo "$ip" >> $HOST_FILE
    else
        echo "$ip:$ranks" >> $HOST_FILE
    fi
    
}


# * * * * * * * * * * * * * * * * * *  \/  * * * * * * * * * * * * * * * * * * #
#                                                                              #
#                          N E T W O R K   S E T T I N G S                     #
#                                                                              #
# * * * * * * * * * * * * * * * * * *  /\  * * * * * * * * * * * * * * * * * * #

global_network="1_global"
dc01_network="0_dc_01"
dc02_network="0_dc_02"
dc03_network="0_dc_03"
dc04_network="0_dc_04"

dc01_proxy="proxy_dc01"$separator"1"
dc02_proxy="proxy_dc02"$separator"1"
dc03_proxy="proxy_dc03"$separator"1"
dc04_proxy="proxy_dc04"$separator"1"

dc01_containers=("worker_dc01_c1"$separator"1" "worker_dc01_c1"$separator"2" "worker_dc01_c1"$separator"3" "worker_dc01_c1"$separator"4" "worker_dc01_c1"$separator"5" "worker_dc01_c1"$separator"6" "worker_dc01_c1"$separator"7" "worker_dc01_c1"$separator"8")
dc01_target_networks=($dc02_network $dc03_network $dc04_network $global_network)
dc01_target_local_networks=($dc02_network $dc03_network $dc04_network)
dc01_target_proxies=($dc02_proxy $dc03_proxy $dc04_proxy)

dc02_containers=("worker_dc02_c1"$separator"1" "worker_dc02_c1"$separator"2" "worker_dc02_c2"$separator"1" "worker_dc02_c2"$separator"2" "worker_dc02_c2"$separator"3" "worker_dc02_c2"$separator"4")
dc02_target_networks=($dc01_network $dc03_network $dc04_network $global_network)
dc02_target_local_networks=($dc01_network $dc03_network $dc04_network)
dc02_target_proxies=($dc01_proxy $dc03_proxy $dc04_proxy)

dc03_containers=("worker_dc03_c1"$separator"1" "worker_dc03_c2"$separator"1" "worker_dc03_c4"$separator"1")
dc03_target_networks=($dc01_network $dc02_network $dc04_network $global_network)
dc03_target_local_networks=($dc01_network $dc02_network $dc04_network)
dc03_target_proxies=($dc01_proxy $dc02_proxy $dc04_proxy)

dc04_containers=("worker_dc04_c2"$separator"1" "worker_dc04_c2"$separator"2" "worker_dc04_c4"$separator"1" "worker_dc04_c4"$separator"2" "worker_dc04_c4"$separator"3" "worker_dc04_c4"$separator"4")
dc04_target_networks=($dc01_network $dc02_network $dc03_network $global_network)
dc04_target_local_networks=($dc01_network $dc02_network $dc03_network)
dc04_target_proxies=($dc01_proxy $dc02_proxy $dc03_proxy)

head="head"$separator"1"
head_target_proxies=($dc01_proxy $dc02_proxy $dc03_proxy $dc04_proxy)
head_target_networks=($dc01_network $dc02_network $dc03_network $dc04_network)


# * * * * * * * * * * * * * * * * * *  \/  * * * * * * * * * * * * * * * * * * #
#                                                                              #
#                       N E T W O R K   C O N N E C T I O N                    #
#                                                                              #
# * * * * * * * * * * * * * * * * * *  /\  * * * * * * * * * * * * * * * * * * #

echo "DC-01"
ConfigureLocalNetwork $dc01_proxy dc01_containers $dc01_network dc01_target_networks
ConfigureProxy $dc01_proxy $global_network dc01_target_proxies dc01_target_local_networks
echo 

echo "DC-02"
ConfigureLocalNetwork $dc02_proxy dc02_containers $dc02_network dc02_target_networks
ConfigureProxy $dc02_proxy $global_network dc02_target_proxies dc02_target_local_networks
echo 

echo "DC-03"
ConfigureLocalNetwork $dc03_proxy dc03_containers $dc03_network dc03_target_networks
ConfigureProxy $dc03_proxy $global_network dc03_target_proxies dc03_target_local_networks
echo 

echo "DC-04"
ConfigureLocalNetwork $dc04_proxy dc04_containers $dc04_network dc04_target_networks
ConfigureProxy $dc04_proxy $global_network dc04_target_proxies dc04_target_local_networks
echo 

echo "HEAD"
ConfigureHeadNetwork $head $global_network head_target_proxies head_target_networks
echo 


# * * * * * * * * * * * * * * * * * *  \/  * * * * * * * * * * * * * * * * * * #
#                                                                              #
#                           N E T W O R K   D E L A Y                          #
#                                                                              #
# * * * * * * * * * * * * * * * * * *  /\  * * * * * * * * * * * * * * * * * * #

LOCAL_NETWORK_DELAY_IN_MILISECONDS=2
LOCAL_NETWORK_DELAY_JITTER_IN_MILISECONDS=1

GLOBAL_NETWORK_DELAY_IN_MILISECONDS=50
GLOBAL_NETWORK_DELAY_JITTER_IN_MILISECONDS=2


ApplyDelay() {
    local container_name_beginning=$1
    local delay=$2
    local delay_jitter=$3
    local interface=$4

    echo "Adding egress traffic delay $delay""ms to containers ta start with $container_name_beginning"
    # Add delay to egress traffic
    #https://github.com/alexei-led/pumba
    docker run -it -d --rm  -v /var/run/docker.sock:/var/run/docker.sock gaiaadm/pumba netem --interface $interface --duration 60m delay --time $delay --jitter $delay_jitter re2:^$container_name_beginning 
   
}

container_worker_prefix="$prefix""$separator""worker"
ApplyDelay $container_worker_prefix $LOCAL_NETWORK_DELAY_IN_MILISECONDS $LOCAL_NETWORK_DELAY_JITTER_IN_MILISECONDS eth0

container_proxy_prefix="$prefix""$separator""proxy"
ApplyDelay $container_proxy_prefix $GLOBAL_NETWORK_DELAY_IN_MILISECONDS $GLOBAL_NETWORK_DELAY_JITTER_IN_MILISECONDS eth1

container_head_prefix="$prefix""$separator""head"
ApplyDelay $container_head_prefix $GLOBAL_NETWORK_DELAY_IN_MILISECONDS $GLOBAL_NETWORK_DELAY_JITTER_IN_MILISECONDS eth0


# * * * * * * * * * * * * * * * * * *  \/  * * * * * * * * * * * * * * * * * * #
#                                                                              #
#                       H O S T   F I L E   G E N E R A T I N G                #
#                                                                              #
# * * * * * * * * * * * * * * * * * *  /\  * * * * * * * * * * * * * * * * * * #

echo "Writing host file..."

# Delete file if exists
if [ -f "$HOST_FILE" ]; then
    echo "$HOST_FILE will be deleted."
    rm $HOST_FILE
fi
WriteContainerIpToHostFile $head $global_network
for i in "${!dc01_containers[@]}"; do WriteContainerIpToHostFile ${dc01_containers[$i]} $dc01_network 1; done
for i in "${!dc02_containers[@]}"; do WriteContainerIpToHostFile ${dc02_containers[$i]} $dc02_network 1; done
for i in "${!dc03_containers[@]}"; do WriteContainerIpToHostFile ${dc03_containers[$i]} $dc03_network 1; done
for i in "${!dc04_containers[@]}"; do WriteContainerIpToHostFile ${dc04_containers[$i]} $dc04_network 1; done

echo "Entries added to $HOST_FILE"
