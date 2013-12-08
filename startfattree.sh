#!/bin/sh
./pox/pox.py misc.fattreeswitch > /dev/null &
sudo mn --custom ~/mininet/custom/topo-fattree.py --topo fattree --mac --arp --switch ovsk --controller=remote
