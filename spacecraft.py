import math

class Spacecraft:
    def __init__(self, name, mass, fuel, x=0, y=0, vx=0, vy=0):
        """
        Initialize the spacecraft with basic parameters.
        """
        self.name = name
        self.mass = mass  # in kilograms
        self.fuel = fuel  # in kilograms
        self.x = x  # position in meters
        self.y = y
        self.vx = vx  # velocity in m/s
        self.vy = vy
        self.thrust = 0  # thrust in newtons

    def apply_thrust(self, thrust, angle, duration, fuel_consumption_rate):
        """
        Apply thrust to the spacecraft at a given angle for a specified duration.
        """
        if self.fuel <= 0:
            print(f"{self.name}: Out of fuel! No thrust applied.")
            return

        self.thrust = thrust
        angle_rad = math.radians(angle)
        ax = (thrust / self.mass) * math.cos(angle_rad)
        ay = (thrust / self.mass) * math.sin(angle_rad)

        self.vx += ax * duration
        self.vy += ay * duration

        fuel_used = fuel_consumption_rate * duration
        self.fuel = max(self.fuel - fuel_used, 0)  # Ensure fuel doesn't go negative

    def update_position(self, dt):
        """
        Update position based on velocity, gravity, and time delta (dt).
        """
        gravity = -9.8  # Earth's gravity in m/s^2
        self.vy += gravity * dt
        self.x += self.vx * dt
        self.y += self.vy * dt

        if self.y < 0:
            self.y = 0
            self.vy = max(self.vy, 0)  # Reset velocity on ground impact

    def check_landing(self):
        """
        Check if the spacecraft landed safely or crashed.
        Safe landing: Vertical velocity <= -5 m/s
        Crash landing: Vertical velocity > -5 m/s
        """
        if self.vy <= -5:
            return "Crash Landing"
        else:
            return "Safe Landing"

    def status(self):
        """
        Return the spacecraft's current status.
        """
        return {
            "x": self.x,
            "y": self.y,
            "vx": self.vx,
            "vy": self.vy,
            "fuel": self.fuel
        }