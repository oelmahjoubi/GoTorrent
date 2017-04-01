'''

'''

from InfoPeer import InfoPeer

class Leech(object):
    _ask = ['add_info', 'get_info_peer']
    _tell = ['increment_points']

    def add_info(self, torrent_hash, points, ini_pos):
        '''

        :param torrent_hash:
        :param points:
        :param ini_pos:
        :return:
        '''
        self.info_peer = InfoPeer(self.get_id(), torrent_hash, points)
        self.info_peer.add_ini_pos(ini_pos)

    def get_info_peer(self):
        return self.info_peer

    def get_id(self):
        self.id

    def printHola(self):
        print "I'm a leech "+ self.id

    def push (self, chunk_id, chunk_data):
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
