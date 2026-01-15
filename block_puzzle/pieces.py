# pieces.py
# Kõik plokid / kujundid ja juhuslik valik

from typing import List, Tuple
import random

Color = Tuple[int, int, int]
Block = Tuple[int, int]


class Shape:

    def __init__(self, name: str, blocks: List[Block], color: Color):
        self.name = name
        self.blocks = blocks
        self.color = color


SHAPES: List[Shape] = [
    Shape("2x2 ruut", [(0, 0), (1, 0), (0, 1), (1, 1)], (255, 215, 0)),
    Shape("3 joon", [(0, 0), (1, 0), (2, 0)], (0, 200, 255)),
    Shape("L-kuju", [(0, 0), (0, 1), (1, 1)], (255, 140, 0)),
    Shape("S-kuju", [(0, 0), (1, 0), (1, 1)], (50, 205, 50)),
    Shape("väike ruut", [(0, 0)], (220, 220, 220)),
    Shape("2 vert", [(0, 0), (0, 1)], (186, 85, 211)),
]


def get_random_shapes(count: int = 3) -> List[Shape]:
    """Tagastame 'count' juhuslikku kuju (võib korduda)."""
    return [random.choice(SHAPES) for _ in range(count)]

