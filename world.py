import random

import pygame


def random_spawn_rect(width, height, home_area: pygame.Rect, w: int, h: int, margin: int = 20) -> pygame.Rect:
    # Avoid spawning too near the home area and keep clear of UI bars.
    while True:
        x = random.randint(margin, width - margin - w)
        y = random.randint(margin + 80, height - margin - h - 70)
        rect = pygame.Rect(x, y, w, h)
        if not rect.colliderect(home_area.inflate(140, 140)):
            return rect


def is_near(rect_a: pygame.Rect, rect_b: pygame.Rect, distance: int = 20) -> bool:
    expanded = rect_b.inflate(distance * 2, distance * 2)
    return rect_a.colliderect(expanded)


def dist2(ax: int, ay: int, bx: int, by: int) -> int:
    dx = ax - bx
    dy = ay - by
    return dx * dx + dy * dy


def nearest_rect(from_rect: pygame.Rect, rect_list: list[pygame.Rect]) -> pygame.Rect | None:
    if not rect_list:
        return None

    fx, fy = from_rect.center
    best = rect_list[0]
    best_d = dist2(fx, fy, best.centerx, best.centery)

    for rect in rect_list[1:]:
        d = dist2(fx, fy, rect.centerx, rect.centery)
        if d < best_d:
            best = rect
            best_d = d

    return best
