#!/bin/sh
./pox/pox.py misc.bintreeswitch &
sudo mn --topo tree,3 --mac --arp --switch ovsk --controller=remote
sudo killall python2.7
