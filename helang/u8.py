from typing import *


class U8:
    """
    The Saint He's specific type.
    """
    def __init__(self, value: Optional[List[int]] = None):
        self.value = [] if value is None else value

    def __str__(self) -> str:
        return ' | '.join(str(element) for element in self.value)

    def increment(self):
        self.value = [v+1 for v in self.value]
