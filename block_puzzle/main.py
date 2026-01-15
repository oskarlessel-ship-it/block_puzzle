# main.py
# Põhifail: pygame aken, hiirega juhtimine, mängutsükkel.

import pygame
import sys

from field import (
    create_field,
    can_place,
    place_shape,
    clear_full_lines,
    has_any_moves,
    GRID_WIDTH,
    GRID_HEIGHT,
    CELL_SIZE,
)
from pieces import get_random_shapes, Shape

# Värvid
BG_COLOR = (15, 15, 30)
GRID_LINE = (60, 60, 90)
WHITE = (230, 230, 230)

WINDOW_WIDTH = GRID_WIDTH * CELL_SIZE
INFO_HEIGHT = 160
WINDOW_HEIGHT = GRID_HEIGHT * CELL_SIZE + INFO_HEIGHT

PREVIEW_CELL = CELL_SIZE // 2  # plokkide suurus all eelvaates


def draw_field(screen, field, font, score, shapes, selected_index, game_over):
    """Joonistame välja, täidetud plokid ja all kujundid."""
    screen.fill(BG_COLOR)

    # Ruudustik
    for x in range(GRID_WIDTH):
        for y in range(GRID_HEIGHT):
            rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, GRID_LINE, rect, 1)

    # Täidetud plokid
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            color = field[y][x]
            if color is not None:
                rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(screen, color, rect)

    # Ülemine tekst
    text = font.render(f"Reasid/veerud eemaldatud: {score}", True, WHITE)
    screen.blit(text, (10, 10))

    if game_over:
        msg = font.render("Mäng läbi - vajuta R uuesti alustamiseks", True, WHITE)
        screen.blit(msg, (10, 40))
    else:
        msg = font.render(
            "Vali kuju (hiirega) ja kliki väljale, kuhu panna.", True, WHITE
        )
        screen.blit(msg, (10, 40))

    # All eelvaated
    for i, shape in enumerate(shapes):
        draw_shape_preview(screen, shape, i, selected_index)

    pygame.display.flip()


def draw_shape_preview(screen, shape: Shape, index: int, selected_index: int):
    """Joonistame ühe kujundi eelvaate all (kolm pesa)."""
    slot_width = WINDOW_WIDTH // 3
    base_x = index * slot_width
    area_y = GRID_HEIGHT * CELL_SIZE + 20

    # raami ümber pesa
    rect_slot = pygame.Rect(base_x + 5, area_y - 5, slot_width - 10, INFO_HEIGHT - 30)
    border_color = (120, 120, 160)
    if index == selected_index:
        border_color = (255, 255, 0)
    pygame.draw.rect(screen, border_color, rect_slot, 2)

    if shape is None:
        return

    # leiame kuju laiuse/kõrguse
    min_dx = min(dx for dx, dy in shape.blocks)
    max_dx = max(dx for dx, dy in shape.blocks)
    min_dy = min(dy for dx, dy in shape.blocks)
    max_dy = max(dy for dx, dy in shape.blocks)

    shape_w = (max_dx - min_dx + 1) * PREVIEW_CELL
    shape_h = (max_dy - min_dy + 1) * PREVIEW_CELL

    start_x = base_x + (slot_width - shape_w) // 2
    start_y = area_y + (INFO_HEIGHT - 40 - shape_h) // 2

    # plokid eelvaates
    for dx, dy in shape.blocks:
        x = start_x + (dx - min_dx) * PREVIEW_CELL
        y = start_y + (dy - min_dy) * PREVIEW_CELL
        rect = pygame.Rect(x, y, PREVIEW_CELL, PREVIEW_CELL)
        pygame.draw.rect(screen, shape.color, rect)


def grid_pos_from_mouse(pos):
    """Muudame hiire koordinaadi (px) ruudustiku koordinaatideks (gx, gy)."""
    mx, my = pos
    if my >= GRID_HEIGHT * CELL_SIZE:
        return None
    gx = mx // CELL_SIZE
    gy = my // CELL_SIZE
    if 0 <= gx < GRID_WIDTH and 0 <= gy < GRID_HEIGHT:
        return gx, gy
    return None


def preview_index_from_mouse(pos):
    """Millisest kolmest pesast klikk tuli? (0, 1 või 2)"""
    mx, my = pos
    if my < GRID_HEIGHT * CELL_SIZE:
        return None
    slot_width = WINDOW_WIDTH // 3
    index = mx // slot_width
    if 0 <= index < 3:
        return index
    return None


def reset_game():
    """Alustame uut mängu."""
    field = create_field()
    shapes = get_random_shapes(3)
    score = 0
    selected = None
    game_over = False
    return field, shapes, score, selected, game_over


def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Block puzzle - lihtsustatud versioon")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Arial", 20)

    field, shapes, score, selected_index, game_over = reset_game()

    running = True
    while running:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if event.key == pygame.K_r:
                    field, shapes, score, selected_index, game_over = reset_game()

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if not game_over:
                    # 1) vali all olev kuju
                    idx = preview_index_from_mouse(event.pos)
                    if idx is not None:
                        if shapes[idx] is not None:
                            selected_index = idx
                    else:
                        # 2) klikk väljal – proovime asetada valitud kuju
                        if selected_index is not None:
                            gp = grid_pos_from_mouse(event.pos)
                            if gp is not None:
                                gx, gy = gp
                                shape = shapes[selected_index]
                                if shape is not None and can_place(field, shape, gx, gy):
                                    place_shape(field, shape, gx, gy)
                                    cleared = clear_full_lines(field)
                                    score += cleared

                                    # kasutatud kuju eemaldame
                                    shapes[selected_index] = None
                                    selected_index = None

                                    # kui kõik 3 kuju kasutatud -> uued
                                    if all(s is None for s in shapes):
                                        shapes = get_random_shapes(3)

                                    # kas enam on võimalik käike teha?
                                    if not has_any_moves(field, shapes):
                                        game_over = True

        draw_field(screen, field, font, score, shapes, selected_index, game_over)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
