#!/bin/sh
./pox/pox.py misc.fattreeswitch &
sudo mn --custom ~/mininet/custom/topo-fattree.py --topo fattree --mac --arp --switch ovsk --controller=remote
sudo killall python2.7
