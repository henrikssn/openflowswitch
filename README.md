openflow
========

Expermients with mininet and open flow switches

## Set-up
Copy fattreeswitch.py and bintreeswitch.py to pox/pox/misc/ on your system.
Create a hostlist.csv file with the provided script (gen_host_list.py)
for the binary tree case, or use the hostlist_fattree.csv file for the 
fattree example. The file must always be named hostlist.csv and stored
in the pox/ directory.

## Start
Start the system (binary tree):
    ./pox.py log.level --DEBUG misc.bintreeswitch

and in another console (the tree topology must be identical with the
hostlist.csv file)

    sudo mn --topo tree,3 --mac --arp --switch ovsk --controller=remote

Start the system (fat tree):
    ./pox.py log.level --DEBUG misc.fattreeswitch

and in another console

    sudo mn --custom /mininet/custom/topo-fattree.py --topo fattree --mac --arp --switch ovsk --controller=remote

## Start by script
Navigate to the pox/ directory
run

    sudo sh startbintree.sh

for binary tree and

    sudo sh startfattree.sh

for fat tree.
