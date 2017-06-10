"""
@Authors: Omar El Mahjoubi & Youssef El Otmany
"""

from random import sample
from pyactor.context import interval, later

class Tracker(object):
    _ask = ['get_peers','_get_peers','_get_announce_state']
    _tell = ['_init_start','announce','stop_interval','_expel_inactive_peers']

    def __init__(self):
        '''
        The constructor
        Empty Parameters
        '''
        self.torrents = {}
        self.EXP_TIME = 10
        self.__KEY_PEERS = 'peers'
        self.__KEY_ANNOUNCED = 'announced'

    def _get_peers(self, torrent_hash):
        if torrent_hash in self.torrents:
            return self.torrents[torrent_hash][self.__KEY_PEERS]

    def _get_announce_state(self, torrent_hash):
        if torrent_hash in self.torrents:
            return self.torrents[torrent_hash][self.__KEY_ANNOUNCED]

    def _init_start(self, later_time, interval_time=None):
        if not interval_time:
            interval_time = self.EXP_TIME
        self.exp_interval = interval(self.host, interval_time, self.proxy, '_expel_inactive_peers')
        later(later_time, self.proxy, 'stop_interval')

    def stop_interval(self):
        self.exp_interval.set()

    def _expel_inactive_peers(self):
        for torrent in self.torrents:
            list_announced = self._get_announce_state(torrent)
            list_peers = self._get_peers(torrent)
            for peer in list_announced.keys():
                if list_announced[peer]:
                    list_announced[peer] = False
                else:
                    del list_announced[peer]
                    list_peers.remove(peer)

    def announce(self, torrent_hash, peer_id):
        '''
        :param torrent_hash: is the id of torrent
        :param peer_ref: reference of the new peer

        '''
        if torrent_hash in self.torrents:
            peers = self._get_peers(torrent_hash)
            announce_state = self._get_announce_state(torrent_hash)
            if peer_id not in peers:
                peers.append(peer_id)
                announce_state[peer_id] = True
            else:
                announce_state[peer_id] = True

        elif torrent_hash not in self.torrents:
            # add seed
            self.torrents[torrent_hash] = {}
            self.torrents[torrent_hash][self.__KEY_PEERS] = [peer_id]
            self.torrents[torrent_hash][self.__KEY_ANNOUNCED] = {peer_id: True}
        #print self.torrents

    def get_peers(self, torrent_hash):
        '''

        :param torrent_hash:
        :param action: push, pull or push_pull
        :return:
        '''

        #print "Estoy en el metodo get_peers"
        if torrent_hash not in self.torrents:
            print "Error, Torrent not found"
            return []

        peers = self.torrents[torrent_hash][self.__KEY_PEERS]

        if len(peers) >= 3:
            result = sample(peers, 3)
        else:
            result = sample(peers, len(peers))
        return result

