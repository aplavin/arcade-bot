from vec import vec

class Player:
    # both reading and writing are not optimized: they are called 256 times less than Monster.read or Missile.read
    def __init__(self):
        self.ClassName = 0
        self.Position = vec(0, 0)
        self.Velocity = vec(0, 0)
        self.Radius = 0
        self.HitPoints = 0
        self.MaxHitPoints = 0
        self.MaxVelocity = 0
        self.MaxAcceleration = 0
        self.GunCooldownRemaining = 0
        self.GunCooldownPeriod = 0
        self.BulletDamage = 0
        self.BulletHitPoints = 0
        self.BulletVelocity = 0
        self.BulletRadius = 0
        self.Shoot = vec(0, 0)
        self.Run = vec(0, 0)
        self.Time = 0

    def read(self, sock):
        self.ClassName = sock.next_int()
        self.Position = vec(sock.next_float(), sock.next_float())
        self.Velocity = vec(sock.next_float(), sock.next_float())
        self.Radius = sock.next_float()
        self.HitPoints = sock.next_float()
        self.MaxHitPoints = sock.next_float()
        self.MaxVelocity = sock.next_float()
        self.MaxAcceleration = sock.next_float()
        self.GunCooldownRemaining = sock.next_float()
        self.GunCooldownPeriod = sock.next_float()
        self.BulletDamage = sock.next_float()
        self.BulletHitPoints = sock.next_float()
        self.BulletVelocity = sock.next_float()
        self.BulletRadius = sock.next_float()
        self.Shoot = vec(sock.next_float(), sock.next_float())
        self.Run = vec(sock.next_float(), sock.next_float())
        self.Time = sock.next_int()

    def write(self, sock):
        sock.write_int(self.ClassName)
        sock.write_float(self.Position.x)
        sock.write_float(self.Position.y)
        sock.write_float(self.Velocity.x)
        sock.write_float(self.Velocity.y)
        sock.write_float(self.Radius)
        sock.write_float(self.HitPoints)
        sock.write_float(self.MaxHitPoints)
        sock.write_float(self.MaxVelocity)
        sock.write_float(self.MaxAcceleration)
        sock.write_float(self.GunCooldownRemaining)
        sock.write_float(self.GunCooldownPeriod)
        sock.write_float(self.BulletDamage)
        sock.write_float(self.BulletHitPoints)
        sock.write_float(self.BulletVelocity)
        sock.write_float(self.BulletRadius)
        sock.write_float(self.Shoot.x)
        sock.write_float(self.Shoot.y)
        sock.write_float(self.Run.x)
        sock.write_float(self.Run.y)
        sock.write_int(self.Time)
