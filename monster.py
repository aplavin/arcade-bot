from vec import vec

class Monster:
    def __init__(self):
        # initialize only vectors, it's needed to assign them later without creating new ones
        self.Position = vec(0.0, 0.0)
        self.Velocity = vec(0.0, 0.0)

    def read(self, sock):
        self.ClassName = sock.next_int()
        if self.ClassName == -1:
            # optimization: don't read what is known to be empty
            sock.skip_read(18 * 4)
            return

        # unpack all floats at once and use multiple assignment
        self.Position.x, self.Position.y, \
        self.Velocity.x, self.Velocity.y, \
        self.Radius, self.HitPoints, self.MaxHitPoints, \
        self.MaxVelocity, self.MaxAcceleration, \
        self.GunCooldownRemaining, self.GunCooldownPeriod, \
        self.BulletDamage, self.BulletHitPoints, self.BulletVelocity, self.BulletRadius, \
        self.TeethCooldownRemaining, self.TeethCooldownPeriod, self.BiteDamage = \
        sock.next_floats(18)
