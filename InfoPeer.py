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
        self.torrent_has  = torrent_hash
        self.points = points
        self.active = False

    def add_ini_pos(self, ini_pos):
        self.ini_pos = ini_pos

    def increment_points(self, points):
        '''

        :return:
        '''
        self.points = self.points + points

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