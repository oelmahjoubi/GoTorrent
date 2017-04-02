'''

'''


class InfoPeer(object):
    points = int
    ini_pos = int


    def __init__(self, id, torrent_hash, points):
        '''

        :param id:
        :param points:
        '''
        self.id = id
        self.torrent_hash = torrent_hash
        self.points_seed = 0
        self.active = False
        self.points = points

    def add_ini_pos(self, ini_pos):
        self.ini_pos = ini_pos

    def increment_points_peer(self):
        '''

        :return:
        '''
        self.points = self.points + 1

    def increment_points_seed(self):
        self.points_seed = self.points_seed + 1
    def activate(self):
        '''

        :return: void
        '''
        if not self.active:
            self.active = True

    def deactivate(self):
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