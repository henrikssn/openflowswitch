#!/bin/sh
./pox/pox.py log.level --DEBUG misc.bintreeswitch &
sudo mn --topo tree,3 --mac --arp --switch ovsk --controller=remote
