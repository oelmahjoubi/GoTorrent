import pyactor
from pyactor.context import set_context, create_host, serve_forever, Host, sleep, shutdown

from Leech import Leech
from Tracker import Tracker
from Seed import Seed
from random import randint

if __name__ == "__main__":

    set_context()
    h = create_host()

    tracker = h.spawn('tracker', Tracker)
    seed = h.spawn('seed', Seed)
    peer1 = h.spawn('peer1', Leech)
    peer2 = h.spawn('peer2', Leech)

    peer3 = h.spawn('peer3', Leech)
    peer4 = h.spawn('peer4', Leech)
    peer5 = h.spawn('peer5', Leech)
    peer6 = h.spawn('peer6', Leech)
    peer7 = h.spawn('peer7', Leech)
    peer8 = h.spawn('peer8', Leech)
    peer9 = h.spawn('peer9', Leech)
    peer10 = h.spawn('peer10', Leech)
    peer11 = h.spawn('peer11', Leech)
    peer12 = h.spawn('peer12', Leech)
    peer13 = h.spawn('peer13', Leech)
    peer14 = h.spawn('peer14', Leech)

    tracker.announce("Fichero youssef", seed)
    sleep(1)
    tracker.announce("Fichero youssef", peer1)
    tracker.announce("Fichero youssef", peer2)

    tracker.announce("Fichero youssef", peer3)
    tracker.announce("Fichero youssef", peer4)
    tracker.announce("Fichero youssef", peer5)
    sleep(3)
    print tracker.get_torrent()
    result = tracker.get_peers_push("Fichero youssef", seed)
    print result
    sleep(3)
    seed.pushear()


    sleep(5)
    shutdown()

    '''
    tracker.announce("Fichero youssef", peer6)
    tracker.announce("Fichero youssef", peer7)
    tracker.announce("Fichero youssef", peer8)
    tracker.announce("Fichero youssef", peer9)
    tracker.announce("Fichero youssef", peer10)
    tracker.announce("Fichero youssef", peer11)
    tracker.announce("Fichero youssef", peer12)
    tracker.announce("Fichero youssef", peer13)
    tracker.announce("Fichero youssef", peer14)

    tracker = Tracker()
    seed = Seed('seed1')
    seed2 = Seed('seed2')
    leech = Leech('leech1')
    leech2 = Leech('leech2')
    leech3 = Leech('leech3')
    leech4 = Leech('leech4')
    leech5 = Leech('leech5')
    leech6 = Leech('leech6')


    tracker.announce("youssef", seed)
    tracker.announce("youssef", leech)
    tracker.announce("youssef", leech2)
    tracker.announce("youssef", leech3)
    tracker.announce("youssef", leech4)
    tracker.announce("youssef", leech5)
    #tracker.announce("youssef", leech6)
    tracker.announce("torrent", seed2)
    tracker.announce("torrent", leech)
    tracker.announce("torrent", leech2)
    result = tracker.get_peers_push("youssef", seed)

    seed.add_peers(result)
    result2 = tracker.get_peers_push("youssef", leech5)
    print result2
    seed.pushear()
    leech5.add_peers(result2)
    leech5.pushear()
    '''

