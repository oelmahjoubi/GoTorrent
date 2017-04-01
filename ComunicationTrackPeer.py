import pyactor
from pyactor.context import set_context, create_host, serve_forever, Host, sleep, shutdown

from Leech import Leech
from Tracker import Tracker
from Seed import Seed

if __name__ == "__main__":
    set_context()
    h = create_host()

    tracker = h.spawn('tracker', Tracker)
    seed = h.spawn('seed', Seed)
    peer1 = h.spawn('peer1', Leech)
    '''peer2 = h.spawn('peer2', Leech)
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

    #tracker.announce("Youssef", seed)

    #seed.printHola()
    #seed.recibir_peer(peer1)
'''
    tracker.announce("Fichero youssef", seed)
    tracker.announce("Fichero youssef", peer1)

    print tracker.get_peers_push("Fichero youssef", seed)
    '''
    tracker.announce("Fichero youssef", peer2)
    tracker.announce("Fichero youssef", peer3)
    tracker.announce("Fichero youssef", peer4)
    tracker.announce("Fichero youssef", peer5)
    tracker.announce("Fichero youssef", peer6)
    tracker.announce("Fichero youssef", peer7)
    tracker.announce("Fichero youssef", peer8)
    tracker.announce("Fichero youssef", peer9)
    tracker.announce("Fichero youssef", peer10)
    tracker.announce("Fichero youssef", peer11)
    tracker.announce("Fichero youssef", peer12)
    tracker.announce("Fichero youssef", peer13)
    tracker.announce("Fichero youssef", peer14)

    '''

    sleep(5)
    shutdown()

