"""
@Authors: Omar El Mahjoubi & Youssef El Otmany
"""
import unittest
from pyactor.context import set_context, create_host, sleep, shutdown
from src.peer import Peer
from src.tracker import Tracker


class Test(unittest.TestCase):

    def setUp(self):
        set_context()
        self.h = create_host()

    def tearDown(self):
        shutdown()

    def test_tracker(self):
        num_peers = 6
        torrent_hash = 'file'
        peers = []
        time = 4            #is used to stop the intervals
        expel_time= 1       # time to expel interval

        tracker = self.h.spawn('tracker', Tracker)
        tracker._init_start(time, expel_time)

        for i in range(0, num_peers, 1):
            peers.append(self.h.spawn("peer" + str(i), Peer))

        for i in range(0, num_peers, 1):
            peers[i].set_tracker(tracker)

        for peer in peers:
            peer.announce(torrent_hash)
        sleep(2)

        self.assertIsNotNone(tracker._get_peers(torrent_hash))
        sleep(time)
        self.assertEqual(tracker._get_announce_state(torrent_hash), {})

    def test_seed(self):
        seed = self.h.spawn("seed", Peer)
        seed.be_seed()
        self.assertIsNotNone(seed.get_data())
        self.assertIsNone(seed.get_urgent_chunks())
        self.assertIsNone(seed.get_lack_chunks())

    def test_peer(self):
        peer = self.h.spawn("peer", Peer)
        peer.init_structs()
        self.assertIsNone(peer.get_data())
        self.assertIsNotNone(peer.get_urgent_chunks())
        self.assertIsNotNone(peer.get_lack_chunks())

    def test_push(self):
        num_peers = 6
        torrent_hash = 'file'
        peers = []
        time = 2
        option = 1

        tracker = self.h.spawn('tracker', Tracker)
        tracker._init_start(time)

        for i in range(0, num_peers, 1):
            peers.append(self.h.spawn("peer" + str(i), Peer))

        seed = peers[0]
        seed.be_seed()

        for peer in peers:
            peer.init_start(tracker, torrent_hash, time, option)

        sleep(time)

        for peer in peers:
            self.assertIsNotNone(peer.get_data())

    def test_pull(self):
        num_peers = 6
        torrent_hash = 'file'
        peers = []
        time = 2            #is used to stop the intervals
        option = 2

        tracker = self.h.spawn('tracker', Tracker)
        tracker._init_start(time)

        for i in range(0, num_peers, 1):
            peers.append(self.h.spawn("peer" + str(i), Peer))

        seed = peers[0]
        seed.be_seed()

        for peer in peers:
            peer.init_start(tracker,torrent_hash,time, option)
        sleep(time)

        for peer in peers:
            self.assertIsNotNone(peer.get_data())

    def test_push_pull(self):
        num_peers = 6
        torrent_hash = 'file'
        peers = []
        time = 2            #is used to stop the intervals
        option = 3

        tracker = self.h.spawn('tracker', Tracker)
        tracker._init_start(time)

        for i in range(0, num_peers, 1):
            peers.append(self.h.spawn("peer" + str(i), Peer))

        seed = peers[0]
        seed.be_seed()

        for peer in peers:
            peer.init_start(tracker, torrent_hash, time, option)
        sleep(time)

        for peer in peers:
            self.assertIsNotNone(peer.get_data())

if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(Test)
    unittest.TextTestRunner(verbosity=2).run(suite)
