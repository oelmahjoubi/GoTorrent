import pyactor
import hashlib
from pyactor.context import set_context, create_host, serve_forever, sleep
'''
* Funciona el anounce, falta crear un metodo para eliminar los peers que no se anuncian en 10 segundos.
* El get_peers no da ningun error pero aun no se ha verificado que funciona al 100 por cien. Ver porque no
  se hace el callback(debe ser alguna tonteria... :D).
'''

class Tracker(object):
    _tell = ['announce']
    _ask = ['get_peers']
    _ref = ['announce']

    def __init__(self):
        '''
        The constructor
        Empty Parameters
        '''
        self.torrents = {}

    def anounce(self, torrent_hash, peer_ref):
        '''

        :param torrent_has:
        :param peer_ref:
        :return:
        '''
        torrent_hash_code = hashlib.sha1(torrent_hash)
        if not self.torrents.has_key(torrent_hash_code):
            #usar una estructura de datos adicional que contenga el peer y su puntuacion
            #al sed se le puede asignar valor de -1



        print "Received: " + hash_id + " from: " + peer_ref
        self.files_peers["peer"].append(peer_ref)
        self.files_peers["peer2"] = "torrent"
        print self.files_peers["peer"]

        for file in self.files_peers.keys():
            for peer in self.files_peers[file]:
                if file == hash_id:
                    if self.files_peers[file] != peer:
                        self.files_peers[file].append(peer_ref)


    def get_peers(self,torrent_hash, action):
        '''

        :param torrent_hash:
        :param action: push, pull or push_pull
        :return:
        '''
        sleep(1)
        return self.files_peers[self.peer]

    def get_peers_push(self, torrent_hash):
        '''

        :param torrent_hash:
        :return:
        '''
        print "TODO"

    def get_peers_pull(self, torrent_hash):
        '''

        :param torrent_hash:
        :return:
        '''
        print "TODO"

    def get_peers_push_pull(self, torrent_hash):
        '''

        :param torrent_hash:
        :return:
        '''
        print "TODO"


    def __pridecate_push(self):
        print "TODO"

    def __predicate_pull(self):
        print "TODO"

    def __predicate_push_pull(self):
        print "TODO"




class InfoPeer(object):

    def __init__(self, id, points):
        '''

        :param id:
        :param points:
        '''
        self.id = id
        self.points = points
        self.active = False

    def increment_points(self):
        '''

        :return:
        '''
        self.points = int(self.points) + 1

    def active(self):
        '''

        :return: void
        '''
        self.active = True

    def desactive(self):
        '''

        :return:
        '''
        self.active = False

    def is_active(self):
        '''

        :return:
        '''
        if self.active:
            return True
        return False
