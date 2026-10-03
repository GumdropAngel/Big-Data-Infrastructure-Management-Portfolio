#!/bin/bash
#script to setup Hadoop mini cluster on LXC

#1. cloning node from template
lxc copy master-template namenode
lxc copy master-template datanode1
lxc copy master-template datanode2

#2. locking static IP (LXD side)
lxc network attach lxdbr0 namenode eth0 eth0
lxc config device set namenode eth0 ipv4.address 10.10.10.10

lxc network attach lxdbr0 datanode1 eth0 eth0
lxc config device set datanode1 eth0 ipv4.address 10.10.10.11

lxc network attach lxdbr0 datanode2 eth0 eth0
lxc config device set datanode2 eth0 ipv4.address 10.10.10.12

#3. starting all nodes
lxc start namenode datanode1 datanode2

#4. SSH passwordless (only on namenode as hadoop user)
# su - hadoop
# ssh-keygen -t rsa -P "" -f ~/.ssh/id_rsa
# ssh-copy-id namenode
# ssh-copy-id datanode1
# ssh-copy-id datanode2

#5 format namenode & start cluster
# hdfs namenode -format
# start-dfs.sh
# start-yarn.sh
