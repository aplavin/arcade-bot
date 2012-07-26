import socket
from subprocess import Popen
from time import sleep
from world import World
from math import sqrt
from vec import vec

def dot(v1, v2):
    return v1.x * v2.x + v1.y * v2.y

def cross(v1, v2):
    return v1.x * v2.y - v1.y * v2.x

def move_to(p):
    world.run(p - world.player.Position)

def nearest_path_point(path):
    return min(enumerate(path), key = lambda p: world.player.Position.dist(p[1]))[0]

def move_path(path):
    move_to(path[(nearest_path_point(path) + 1) % len(path)])

def calc_time_approx(mon, neg = False):
    # TODO: better algorithm, take player path into account
    rel_pos = mon.Position - world.player.Position
    rel_v = mon.Velocity - world.player.Velocity * (-1 if neg else 1)
    # t = |rel_pos| / ((rel_v, rel_pos) / |rel_pos|), simplified
    try:
        t = dot(rel_pos, rel_pos) / dot(rel_v, rel_pos)
    except ZeroDivisionError:
        return 1e10
    # TODO: why abs(t) works, but +-t don't?
    return abs(t)

def shoot(mon):
    mon_rel_pos = mon.Position - world.player.Position
    mon_v = mon.Velocity
    mis_v_abs2 = world.player.BulletVelocity ** 2
    # TODO: simplify formulae (this taken from Mathematica)
    t = (dot(mon_rel_pos, mon_v) + sqrt(mis_v_abs2 * mon_rel_pos.abs2() - cross(mon_rel_pos, mon_v) ** 2)) / (mis_v_abs2 - mon_v.abs2())
    # seem to be more accurate with this
    t += 0.01
    mis_v = mon_rel_pos / t + mon.Velocity
    world.shoot(mis_v)

def run():
    global world

    sleep(0.1)
    Popen('run_serv.bat')
    sleep(0.1)

    EPS = 1e-2

    # TODO: may be circle isn't the best path? or not path at all, dynamic direction calculation
    # about 1000 runs with different rpath showed that 0.42 is the best, but diff isn't great
    global rpath
    rpath = 0.42
    floats = [x / 20 for x in range(-20, 21)]
    path = [vec(0.5, 0.5) + vec(x, sqrt(1 - x ** 2)) * rpath for x in floats]
    path += [vec(0.5, 0.5) + vec(x, -sqrt(1 - x ** 2)) * rpath for x in reversed(floats[1:-1])]

    world = World()
    world.make_move()

    were104 = False

    try:
        while True:
            world.make_move()

            move_path(path)

            mons = [mon for mon in world.monsters if mon.ClassName != -1]
            if len(mons) == 0:
                continue


#            ms = [(calc_time_approx(m), m) for m in mons]
#            if len(ms) > 10:
#                ms = ms[:10]
#            sum_next = sum(t for t, m in ms)
#
#            ms = [(calc_time_approx(m, True), m) for m in mons]
#            if len(ms) > 10:
#                ms = ms[:10]
#            sum_prev = sum(t for t, m in ms)
#
#            if sum_next < sum_prev:
#                print(sum_prev - sum_next)
#                path = path[::-1]

            ids = {mon.ClassName for mon in mons}
            if ids == {104}:
                were104 = False
                for mon in mons:
                    shoot(mon)
                    move_path(path)
                    world.make_move()
                    shoot(mon)
                    move_path(path)
                    world.make_move()
            elif 104 in ids and not were104:
                were104 = True
                for mon in (m for m in mons if m.ClassName == 104):
                    shoot(mon)
                    move_path(path)
                    world.make_move()
                    shoot(mon)
                    move_path(path)
                    world.make_move()
            else:
                nearest_mon = min(mons, key = calc_time_approx)
                shoot(nearest_mon)
    except socket.error:
        return int(open('score.txt').read())


def run_many(n):
    scores = []
    for i in range(n):
        scores.append(run())

    return sum(scores) / n

if __name__ == '__main__':
#    run()
    with open('res.txt', 'w') as file:
        while True:
            file.write('%d\n' % run())
            file.flush()
