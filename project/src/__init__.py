"""
@Authors: Omar El Mahjoubi & Youssef El Otmany
"""
from pyactor.context import set_context, create_host, sleep, shutdown
from tqdm import tqdm
from tracker import Tracker
from peer import Peer

class Grafics(object):

    _ask = ['print_stat']
    _tell = ['init_start']
    _ref = ['init_start']

    def __init__(self):
        self.peers = None

    def init_start(self, peers, time):
        self.peers = peers
        self.print_stat(time)

    def print_stat(self,time):
        total = 0
        with tqdm(total=9*(len(self.peers)-1)) as pbar:
            for i in range(time):
                new_total = 0
                for peer in self.peers:
                    num_ch = peer.get_num_chunks()
                    if num_ch:
                        new_total = new_total + num_ch
                        if new_total > total:
                            pbar.update(new_total - total)
                            total = new_total
                sleep(1)

if __name__ == "__main__":

    set_context()
    h = create_host()
    num_peers = 10
    torrent_hash = 'file'
    peers = []
    time = 10  # is used to stop the intervals
    option = 3
    if option == 1:
        file_name = "push.txt"
    elif option == 2:
        file_name = "pull.txt"
    else:
        file_name = "push_pull.txt"
    file = open(file_name, 'w')


    tracker = h.spawn('tracker', Tracker)
    tracker._init_start(time)

    for i in range(0, num_peers, 1):
        peers.append(h.spawn("peer" + str(i), Peer))

    seed = peers[0]
    seed.be_seed()

    grafic = h.spawn('grafic', Grafics)
    grafic.init_start(peers, time)

    for peer in peers:
        peer.init_start(tracker, torrent_hash, time, option, file)

    sleep(time+2)

    for peer in peers:
        peer.print_data()
    file.close()
    shutdown()

