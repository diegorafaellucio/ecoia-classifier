from enum import Enum

class ImageStateEnum(Enum):
    WAITING_PROCESSING = 0
    PROCESSED = 1
    PROCESSING = 2
    WAITING_INTEGRATION = 3
    INTEGRATING = 4
    INTEGRATED = 5
