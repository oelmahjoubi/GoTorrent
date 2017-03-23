import pyactor
from pyactor.context import set_context, create_host, serve_forever, Host, sleep, shutdown
from Peer import  Peer
from Tracker import Tracker


class Echo(object):

    def __init__(self):
        print "TODO"


if __name__ == "__main__":
    set_context()
    h = create_host()

    tracker = h.spawn('tracker', Tracker)
    peer = h.spawn('peer', Peer)

    peer.pull(tracker, "peer", "omar.jpg")
    sleep(1)
    peer.get_peersP(tracker,"peer")
    shutdown()
    prova = []

