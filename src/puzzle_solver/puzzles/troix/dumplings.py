import numpy as np
from .troix import Board as TroixBoard


class Board(TroixBoard):
    def __init__(self, board: np.array):
        super().__init__(board=board, illegal_run=None)
