# coding=utf-8
import pyactor
import hashlib
from InfoPeer import InfoPeer
from pyactor.context import set_context, create_host, serve_forever, sleep

class Tracker(object):
    _tell = ['announce', 'get_peers_push']
    _ask = ['get_peers']
    _ref = ['announce']

    def __init__(self):
        '''
        The constructor
        Empty Parameters
        '''
        self.torrents = {}
        self.initial_pos = []

    def __get_torrent_hash_code(self, torrent_hash):
        '''
        private method to convert the torrent_hash
        :param torrent_hash:
        :return:
        '''
        return hashlib.sha256(torrent_hash)

    def __get_initial_pos(self, torrent_long, peers_initial_pos):

        """

        :param torrent_long: long of the torrent
        :param peers: number of peers in the swarm, without the new peer nor seed
        :return:
        """

        list_len = len(peers_initial_pos)
        if list_len == 0:
            result = 0
        elif list_len < torrent_long:
            n = list_len % torrent_long

            # if is odd half_pos = m/2 else (m-1)/2
            half_pos = (int)(torrent_long / 2)
            if torrent_long % 2 == 1:
                half_pos = half_pos + 1
            if n < half_pos:
                if (n % 4 == 0) and (n != 0):
                    result  = half_pos / (4*n)
                elif n % 2 == 0:
                    result = peers_initial_pos[ n - 2] + (half_pos/2)
                else:
                    result = peers_initial_pos[n - 1] + half_pos
            else:
                result = peers_initial_pos[n - half_pos] + 1

        peers_initial_pos.append(result)

        return peers_initial_pos[list_len]


    #######################################################################################
    def __select_peers(self, seed, peers, peer_ref, comparative_funtion, sort_function):
        """
        private method to select peers with less punctuation
        Doesn't include seed nor applicant peer
        :param seed: Boolean indicating whether to consider Seed or not
        :param peers: list of peers
        :param peer_ref: applicant peer
        :param comparative_funtion: function to compare two peers
        :param sort_function: function to sort a list of peers
        :return: a list containing between 0 and 3 peers
        """
        result = []
        ini_pos = 0
        if not seed:
            ini_pos = 1
        peers_ids = list(peers.keys())
        for pos in range(ini_pos, len(peers)):
            if peer_ref.get_id() != peers[peers_ids[pos]].get_id():
                if len(result) < 3:
                    result.append(peers[peers_ids[pos]])
                elif comparative_funtion(peers[peers_ids[pos]].get_info_peer(), result[2].get_info_peer()):
                    result[2] = peers[peers_ids[pos]]
                result = sort_function(result)

        return result

    def __seed_request(self, peers, peer_ref):
        """
        private method to check if the request is by seed
        :param peers:
        :param peer_ref:
        :return:
        """
        return  peers[0].id == peer_ref and self.__exist_seed(peers)

    def __exist_seed(self, peers):
        """
        private method to check if exist the seed
        :param peers:
        :return:
        """
        return peers[0].points == -1

    def __peer_in_list(self, peers, peer_ref):
        return len(filter(lambda peer: peer.id == peer_ref, peers)) > 0

    ################################################################################
    def announce(self, torrent_hash, peer_ref):
        '''
        :TODO Verificar si el peer cambia su comportamiento:
                    - en caso positivo habría que guardar los NOMBRES de los peers
              SE DEBE COMPROBAR QUE NO EXISTA EL PEER
        :param torrent_hash: is the id of torrent
        :param peer_ref: reference of the new peer

        '''
        peer_id = peer_ref.get_id()
        torrent_hash_code = torrent_hash
        if torrent_hash_code in self.torrents\
                and peer_id not in self.torrents[torrent_hash_code]:
            self.torrents[torrent_hash_code][peer_id] = peer_ref
            #print "Peer"
            ini_pos = self.__get_initial_pos(14, self.initial_pos)
            print ini_pos
            peer_ref.add_info(torrent_hash_code, 0, ini_pos)

        elif torrent_hash_code not in self.torrents:
            # seed
            peer_ref.add_info(torrent_hash_code, -1)
            self.torrents = {torrent_hash_code: {peer_id:peer_ref}}
            print self.torrents
            print "Seed"

    def get_peers(self, torrent_hash, action):
        '''

        :param torrent_hash:
        :param action: push, pull or push_pull
        :return:
        '''

    ##############################################################################################
    def get_peers_push(self, torrent_hash, peer_ref):
        """
        Method to get peers for the push implementation
        :param torrent_hash: is the torrent hash
        :param peer_ref: is reference of the applicant peer
        :return:
        """
        if torrent_hash not in self.torrents:
            print "Error, Torrent not found"
            return []

        # get all the corresponding peers of torrent
        peers = self.torrents[torrent_hash]

        # check if exist the applicant peer
        if peer_ref.get_id() not in peers:
            return []

        #select peers with less punctuation
        result =  self.__select_peers_push(peers, peer_ref)
        print "resultado "
        print result
        return result

    def __select_peers_push(self, peers, peer_ref):
        """
        private method to select the corresponces peers to push implementation
        :param peers:
        :param peer_ref:
        :return:
        """
        result = self.__select_peers(False, peers, peer_ref, self.__is_smaller, self.__sort_peers_push)

        for pos in range(len(result)):
            result[pos].increment_points(1)
            result[pos] = result[pos]

        # activate applicant peer
        applicant_peer = peers[peer_ref]
        applicant_peer.activate

        return result

    def __is_smaller(self, peer1, peer2):
        """
        private method to compare the punctuation of two peers
        :param peer1:
        :param peer2:
        :return:
        """
        return peer1.points < peer2.points

    def __sort_peers_push(self, peers):
        """
        private method to sort the list of peers for push implementation
        :param peers:
        :return:
        """
        return sorted(peers, key=self.__getKey)

    def __getKey(self, peer):
        """
        private method to get the key of sort function
        :param peer:
        :return:
        """
        return peer.get_info_peer().points

    ##############################################################################################
    def get_peers_pull(self, torrent_hash, peer_ref):
        """
        Method to get peers for the push implementation
        :param torrent_hash:
        :return:
        """
        torrent_hash_code = self.__get_torrent_hash_code(torrent_hash)
        if torrent_hash_code not in self.torrents:
            return []

        # get all the corresponding peers of torrent
        peers = self.torrents[self.__get_torrent_hash_code(torrent_hash)]

        # check if exist the applicant peer
        if not self.__peer_in_list(peers, peer_ref):
            return []

        # select peers with less punctuation
        return self.__select_peers_pull(peers, peer_ref)

    def __select_peers_pull(self, peers, peer_ref):
        """
        private method to select peers for the pull implementation
        :param peers:
        :param peer_ref:
        :return:
        """
        seed = True
        if not self.__exist_seed(peers):
            seed = False

        result = self.__select_peers(seed, peers, peer_ref, self.__is_bigger, self.__sort_peers_pull)

        # obtain the id of the select peers and include the seed if is necessary
        if len(result) > 0 :
            for pos in range(len(result)-1):
                result[pos] = result[pos].id
            # change the Peer with fewer points by the Seed
            if len(result) == 3 and seed:
                result[2] = peers[0].id

        # increment applicant peer punctuation depending on selected peers and activate it
        applicant_peer = filter(lambda peer: peer.id == peer_ref, peers)[0]
        applicant_peer.increment_points(len(result))
        applicant_peer.activate

        return result

    def __is_bigger(self, peer1, peer2):
        """
        private method to compar two peers punctuations
        :param peer1:
        :param peer2:
        :return: true or false
        """
        return peer1.points > peer2.points

    def __sort_peers_pull(self, peers):
        """
        Private method to sort list peers to pull action
        :param peers:
        :return:
        """
        return sorted(peers, key=self.__getKey, reverse=True)

    ##############################################################################################
    def get_peers_push_pull(self, torrent_hash, peer_ref):
        '''
        Method to get peers for push-pull implementation
        :param torrent_hash:
        :return:
        '''
        print "TODO"
