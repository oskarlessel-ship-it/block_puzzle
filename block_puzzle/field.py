# Välja  logika: ruudustik, asetamine, ridade/veergude kustutamine, käikude kontroll.

from typing import List, Optional, Tuple
from pieces import Shape

GRID_WIDTH = 10   
GRID_HEIGHT = 10
CELL_SIZE = 40 

Color = Tuple[int, int, int]
Field = List[List[Optional[Color]]]


def create_field() -> Field:
    """Loome tühja välja: None = tühi ruut, muu = värv."""
    return [[None for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]


def inside(x: int, y: int) -> bool:
    return 0 <= x < GRID_WIDTH and 0 <= y < GRID_HEIGHT


def can_place(field: Field, shape: Shape, gx: int, gy: int) -> bool:
    for dx, dy in shape.blocks:
        x = gx + dx
        y = gy + dy
        if not inside(x, y):
            return False
        if field[y][x] is not None:
            return False
    return True


def place_shape(field: Field, shape: Shape, gx: int, gy: int) -> None:
    for dx, dy in shape.blocks:
        x = gx + dx
        y = gy + dy
        field[y][x] = shape.color


def clear_full_lines(field: Field) -> int:

    lines_cleared = 0


    for y in range(GRID_HEIGHT):
        if all(field[y][x] is not None for x in range(GRID_WIDTH)):
            for x in range(GRID_WIDTH):
                field[y][x] = None
            lines_cleared += 1

    for x in range(GRID_WIDTH):
        if all(field[y][x] is not None for y in range(GRID_HEIGHT)):
            for y in range(GRID_HEIGHT):
                field[y][x] = None
            lines_cleared += 1

    return lines_cleared


def has_any_moves(field: Field, shapes) -> bool:
    """Kas mõne antud kujuga on üldse võimalik käiku teha?"""
    for shape in shapes:
        if shape is None:
            continue
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                if can_place(field, shape, x, y):
                    return True
    return False

