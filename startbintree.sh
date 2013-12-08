#!/bin/sh
./pox/pox.py misc.bintreeswitch > /dev/null &
sudo mn --topo tree,3 --mac --arp --switch ovsk --controller=remote
