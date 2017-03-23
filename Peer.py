import pyactor
from pyactor.context import set_context, create_host, serve_forever, Host

'''
Un peer tiene una lista de peers guardada seleccionados aleatoriamente

Usuario normal usa get_anounce

Seed usa anounce
'''


class Peer(object):
    _tell = ['pull','set_peers', 'get_peersP','set_echo', 'say_hi']
    _ask = ['get_name']
    _ref = ['set_echo']

    def __init__(self):
        self.greetings = ['hello', 'hi', 'hey', 'what`s up?']
        self.peers = []

    def pull(self, track, peer_ref, torrent):

        track.anounce(torrent, peer_ref)

    def get_peersP(self, track, peer):
        track.set_request(peer)
        future = track.get_peers(future=True)
        future.add_callback('set_peers')

    def set_peers(self, future):

        self.peers = future.result()
        print "Peers added correctlly!"
