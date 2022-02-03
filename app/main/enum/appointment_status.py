from enum import Enum

class AppointmentStatus(Enum):

    pending = 1
    consulting = 2
    finished = 3
    cancelled = 4
    expired = 5

