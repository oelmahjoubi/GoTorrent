'''

'''

from InfoPeer import InfoPeer
from random import randint

class Leech(object):
    _ask = ['add_info', 'get_info_peer', 'get_id']
    _tell = ['increment_points']


    def __init__(self):
        self.torrent = {}

    def add_info(self, torrent_hash, points, ini_pos):
        '''

        :param torrent_hash:
        :param points:
        :param ini_pos:
        :return:
        '''
        self.info_peer = InfoPeer(self.get_id(), torrent_hash, points)
        self.info_peer.add_ini_pos(ini_pos)

    def add_peers(self, peers):
        self.peers = peers

    def pushear(self):

        chunks = list(self.torrent.keys())
        if len(chunks) > 0:
            print "pusheando"
            chunk_pos = randint(0, int(len(chunks)) -1)
            chunk_id = chunks[chunk_pos]
            for peer in self.peers:
                peer.push(chunk_id, self.torrent[chunk_id])
                peer.get_info_peer().increment_points_peer()

    def get_info_peer(self):
        return self.info_peer

    def get_id(self):
        return self.id

    def printHola(self):
        print "I'm a leech "+ self.id

    def push (self, chunk_id, chunk_data):
        if chunk_id not in self.torrent:
            print self.id
            self.torrent[chunk_id] = chunk_data
            print self.torrent
        """

        :param chunk_id: is the identifier of the chunk
        :param chunk_data: is the actual data in the chunk
        :return:
        """
        pass

    def pull (self, chunk_data):
        """

        :param chunk_data: is the actual data in the chunk
        :return:
        """
        pass
