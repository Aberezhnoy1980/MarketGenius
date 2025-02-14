from typing import List, Tuple, Set


class InvalidListLevelError(ValueError):
    def __init__(self, message="Invalid list level provided."):
        self.message = message
        super().__init__(self.message)
