!#/bin/sh
./pox.py log.level --DEBUG misc.fattreeswitch &
sudo mn --custom /mininet/custom/topo-fattree.py --topo fattree --mac --arp --switch ovsk --controller=remote
