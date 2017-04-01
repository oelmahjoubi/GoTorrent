"""

"""
from InfoPeer import InfoPeer

class Seed(object):

    _ask = ['recibir_peer', 'add_info', 'get_id', 'get_info_peer']
    _tell = ['printHola', 'increment_points']
    _ref = ['recibir_peer']

    def __init__(self):
        self.torrent = ['G','O','T','O','R','R','E','N','T']

    def add_info(self, torrent_hash, points):
        '''

        :param id:
        :param torrent_hash:
        :param points:
        :param ini_pos:
        :return:
        '''
        self.info_peer = InfoPeer(self.get_id(), torrent_hash, points)

    def get_info_peer(self):
        return self.info_peer

    def get_id(self):
        return self.id
    def recibir_peer(self, peer):
        print "The leech " + peer.get_id() + " print"
        peer.printHola()

    def printHola(self):
        print "I'm a seed"

    def push (self, chunk_id, chunk_data):
        """

        :param chunk_id: is the identifier of the chunk
        :param chunk_data: is the actual data in the chunk
        :return:
        """
        pass



