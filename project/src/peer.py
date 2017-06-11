"""
@Authors: Omar El Mahjoubi & Youssef El Otmany
"""

from random import choice
from pyactor.context import interval, later


class Peer(object):
    _ask = ['print_data','get_num_chunks','set_tracker', 'be_seed','get_data',
            'pull_receive', 'get_urgent_chunks','get_lack_chunks','init_structs']
    _tell = ['init_start', 'announce', 'announce_set_peers', 'push',
             'push_receive', 'pull', 'stop_interval',  "save_result"]
    _ref = ['set_tracker']

    def __init__(self):
        self.torrent = {}
        self._KEY_TRACKER = 'tracker'
        self._KEY_HASH = 'torrent_hash'
        self._KEY_PEERS = 'peers'
        self._KEY_DATA = 'data'
        self._KEY_CHUNK_LACK = 'chunk'
        self._KEY_CHUNK_URGENT = 'chunk_urg'
        self._KEY_PUSH_ACTION = 1
        self._KEY_PULL_ACTION = 2
        self._KEY_PUSH_PULL_ACTION = 3
        self.seed = False
        self.ref_peers = {}
        self.file = None
        self.result_str = ""
        self.option = None
        self.announce__set_peers_interval = None
        self.push_interval = None
        self.result_interval = None


    def _set_tracker(self, tracker):
        if self._KEY_TRACKER not in self.torrent:
            self.torrent[self._KEY_TRACKER] = tracker

    def set_tracker(self, tracker):
        """
        Solo para test
        :param tracker: 
        :return: 
        """
        self._set_tracker(tracker)

    def _set_torrent_hash(self, torrent_hash):
        self.torrent[self._KEY_HASH] = torrent_hash

    def _get_tracker(self):
        if self._KEY_TRACKER in self.torrent:
            return self.torrent[self._KEY_TRACKER]

    def _get_torrent_hash(self):
        if self._KEY_HASH in self.torrent:
            return self.torrent[self._KEY_HASH]

    def _get_peers(self):
        if self._KEY_PEERS in self.torrent:
            return self.torrent[self._KEY_PEERS]

    def _get_data(self):
        if self._KEY_DATA in self.torrent:
            return self.torrent[self._KEY_DATA]

    def get_data(self):
        """
        Metodo para testing
        :return: 
        """
        return self._get_data()

    def _get_ref_peers(self):
        return self.ref_peers

    def _get_lack_chunks(self):
        if self._KEY_CHUNK_LACK in self.torrent:
            return self.torrent[self._KEY_CHUNK_LACK]

    def _get_urgent_chunks(self):
        if self._KEY_CHUNK_URGENT in self.torrent:
            return self.torrent[self._KEY_CHUNK_URGENT]

    def get_urgent_chunks(self):
        """
        Metodo usado solo en testing
        :return: la lista de trozos urgentes
        """
        return self._get_urgent_chunks()

    def get_lack_chunks(self):
        """
        Metodo usado solo en testing
        :return: la lista de trozos faltanes no urgentes
        """
        return self._get_lack_chunks()

    def _get_id(self):
        """
        Getter interno
        :return: 
        """
        return self.id

    def get_num_chunks(self):
        """
        Metodo usado solo en test
        :return: numero de trozos que tiene actualmente el peer
        """
        if (self._KEY_DATA in self.torrent) and (not self.seed):
            return len(self.torrent[self._KEY_DATA])

    def init_start(self, tracker, torrent_hash, time, option, file=None):
        """
        Metodo para inicializar el peer
        :param tracker: tracker
        :param torrent_hash: id torrent
        :param time: tiempo para parar el peer
        :param option: opcion a ejecutar
        :param file: fichero
        """
        if (option >= 1) and (option <= 3):
            self._set_tracker(tracker)
            self._set_torrent_hash(torrent_hash)
            self.option = option
            self.file = file
            if not self._KEY_DATA in self.torrent:
                self.torrent[self._KEY_DATA] = {}
            if ((option == self._KEY_PULL_ACTION) or (option == self._KEY_PUSH_PULL_ACTION)) and (not self.seed):
                self._init_structs()
            self.announce__set_peers_interval = interval(self.host, 5, self.proxy, 'announce_set_peers')
            if option == self._KEY_PUSH_ACTION:
                self.push_interval = interval(self.host, 1, self.proxy, 'push')
            elif option == self._KEY_PULL_ACTION:
                if not self.seed: # if not seed
                    self.pull_interval = interval(self.host, 1, self.proxy, 'pull')
            else:
                self.push_interval = interval(self.host, 1, self.proxy, 'push')
                if not self.seed:
                    self.pull_interval = interval(self.host, 1, self.proxy, 'pull')
            self.result_interval = interval(self.host, 1, self.proxy, 'save_result')
            later(time, self.proxy, 'stop_interval')

    def stop_interval(self):
        """
        Metodo para parar los intervalos
        """
        self.announce__set_peers_interval.set()
        if self.option == self._KEY_PUSH_ACTION:
            self.push_interval.set()
        elif (self.option == self._KEY_PULL_ACTION) and (not self.seed):
            self.pull_interval.set()
        elif (self.option == self._KEY_PUSH_PULL_ACTION):
            self.push_interval.set()
            if not self.seed:
                self.pull_interval.set()
        self.result_interval.set()
        if not self.seed and self.file:
            self.file.write(self.result_str + "\n")

    def announce_set_peers(self):
        self.announce_periodically()
        self.set_peers()

    def init_structs(self):
        """
        Metodo para testing
        :return: 
        """
        self._init_structs()

    def _init_structs(self):
        """
        Metodo para inicilizar estructuras en caso de pull y push_pull
        """
        self.torrent[self._KEY_CHUNK_LACK] = []
        self.torrent[self._KEY_CHUNK_URGENT] = []
        chunks = self.torrent[self._KEY_CHUNK_LACK]
        for i in range(1, 10, 1):
            chunks.append(i)


    def print_data(self):
        """
        Metodo para imprimir los trozos que tiene el peer
        :return: 
        """
        if self.torrent[self._KEY_DATA]:
            print self.id, ' ',self.torrent[self._KEY_DATA]

    def announce(self, torrent_hash):
        '''
        Method use in testing only
        :param torrent_hash:
        :return:
        '''
        self.torrent[self._KEY_HASH] = torrent_hash
        self.announce_periodically()

    def announce_periodically(self):
        '''

        :return:
        '''
        if self._KEY_TRACKER not in self.torrent:
            return
        tracker = self._get_tracker()
        tracker.announce(self._get_torrent_hash(), self._get_id())

    def set_peers(self):
        tracker = self._get_tracker()
        if tracker:
            future = tracker.get_peers(self._get_torrent_hash(), future=True)
            future.add_callback('_save_peers')

    def _save_peers(self, future):
        '''
        
        :param future: 
        :return: 
        '''
        peers = future.result()

        if not peers:
            return

        if self._KEY_PEERS in self.torrent:
            del(self.torrent[self._KEY_PEERS])
        self.torrent[self._KEY_PEERS] = []
        for peer_id in peers:
            if peer_id != self._get_id():
                if peer_id not in self.ref_peers:
                    future = self.host.lookup(peer_id, future=True)
                    self.ref_peers[peer_id] = future
                    future.add_callback('_process_peer')
                else:
                    self._get_peers().append(self.ref_peers[peer_id])

    def _process_peer(self, future):
        '''
        
        :param future: 
        :return: 
        '''
        peer = future.result()
        key = [key for key, value in self.ref_peers.iteritems() if value == future][0]
        self.ref_peers[key] = peer
        self._get_peers().append(peer)


    def push(self):
        '''
        
        :return: 
        '''
        data = self._get_data()
        if not data:
            return
        peers = self._get_peers()
        if not peers:
            return
        chunk_to_send = choice(data.keys())
        for peer in peers:
            peer.push_receive(chunk_to_send, data.get(chunk_to_send))

    def push_receive(self, chunk_id, chunk_data):
        """
        :param chunk_id: is the identifier of the chunk
        :param chunk_data: is the actual data in the chunk
        :return:
        """
        data = self._get_data()
        if chunk_id not in data:
            data[chunk_id] = chunk_data
            if (self.option == 3):
                if chunk_id in self._get_urgent_chunks():
                    self._get_urgent_chunks().remove(chunk_id)
                else:
                    self._get_lack_chunks().remove(chunk_id)

    def be_seed(self):
        """
        
        :return: 
        """
        self.seed = True
        self.torrent[self._KEY_DATA] = {1: 'G', 2: 'O', 3: 'T', 4: 'O', 5: 'R', 6: 'R', 7: 'E', 8: 'N', 9: 'T'}

    def pull (self):
        """
        
        :return: 
        """
        peers = self._get_peers()
        if not peers:
            return

        chunks_lack = self._get_urgent_chunks()
        if not chunks_lack:
            chunks_lack = self._get_lack_chunks()
        if chunks_lack:
            for peer in peers:
                chunk_id = choice(chunks_lack)
                future = peer.pull_receive(chunk_id, future=True)
                future.add_callback('process_chunk')

    def process_chunk(self, future):
        """
        
        :param future: 
        :return: 
        """
        result = future.result()
        if result:
            chunk_id = result[0]
            chunk_data = result[1]
            if chunk_id in self._get_urgent_chunks():
                chunks_lack = self._get_urgent_chunks()
            elif chunk_id in self._get_lack_chunks():
                chunks_lack = self._get_lack_chunks()
            else:
                chunks_lack = []
            if chunks_lack:
                data = self._get_data()
                data[chunk_id] = chunk_data
                chunks_lack.remove(chunk_id)

    def pull_receive (self, chunk_id):
        """
        Metodo para recibir peticiones pull
        :param chunk_data: is the actual data in the chunk
        :return:
        """
        data = self._get_data()
        if (data) and (chunk_id in data.keys()):
            return [chunk_id,data[chunk_id]]
        urgent_chunks = self._get_urgent_chunks()
        if chunk_id not in urgent_chunks:
            urgent_chunks.append(chunk_id)
            lack_chunks = self._get_lack_chunks()
            lack_chunks.remove(chunk_id)
            return

    def save_result(self):
        if (self._KEY_DATA in self.torrent) and (not self.seed):
            self.result_str = self.result_str + str(len(self.torrent[self._KEY_DATA]))
