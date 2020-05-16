import numpy as np


class Forest:
    defaultOptions = {}

    def __init__(self, height=20, width=20, options=defaultOptions):
        self.grid = np.empty(shape=(height, width), dtype='object')

