from socketlib import Sock
from player import Player
from monster import Monster
from missile import Missile

class World:
    def __init__(self):
        self.WORLD_BEGIN_MARKER = 1243635
        self.WORLD_END_MARKER = 5365456
        self.CLIENT_BEGIN_MARKER = 42345
        self.CLIENT_END_MARKER = 8752845

        self.MAXMONSTERS = 256
        self.MAXMISSILES = 256

        self.player = Player()
        # initialize arrays, they will be modified inplace
        self.monsters = [Monster() for _ in range(self.MAXMONSTERS)]
        self.missiles = [Missile() for _ in range(self.MAXMISSILES)]

        self.sock = Sock()
        self.sock.connect()

    def make_move(self):
        self.sock.write_int(self.CLIENT_BEGIN_MARKER)
        self.player.write(self.sock)
        self.sock.write_int(self.CLIENT_END_MARKER)
        self.sock.flush()

        # receive all data from socket at once
        self.sock.recv_prepare(7191 * 4)

        marker = self.sock.next_int()
        if marker < self.WORLD_BEGIN_MARKER:
            raise Exception('Wrong begin marker')

        self.player.read(self.sock)
        if self.player.HitPoints < 0:
            return

        for i in range(self.MAXMONSTERS):
            self.monsters[i].read(self.sock)

        for i in range(self.MAXMISSILES):
            self.missiles[i].read(self.sock)

        marker = self.sock.next_int()
        if marker < self.WORLD_END_MARKER:
            raise Exception('Wrong end marker')

    def run(self, v):
        self.player.Run = v

    def shoot(self, v):
        self.player.Shoot = v
