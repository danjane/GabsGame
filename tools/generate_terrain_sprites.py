from pathlib import Path

import pygame


OUT_DIR = Path("assets/sprites/terrain")


def save(surface: pygame.Surface, name: str) -> None:
    pygame.image.save(surface, OUT_DIR / name)


def ellipse_sprite(size: tuple[int, int], color: tuple[int, int, int], rim: tuple[int, int, int] | None = None) -> pygame.Surface:
    sprite = pygame.Surface(size, pygame.SRCALPHA)
    rect = pygame.Rect(0, 0, *size)
    if rim is not None:
        pygame.draw.ellipse(sprite, rim, rect)
        rect = rect.inflate(-4, -3)
    pygame.draw.ellipse(sprite, color, rect)
    return sprite


def make_reeds() -> pygame.Surface:
    sprite = pygame.Surface((40, 42), pygame.SRCALPHA)
    for i, x in enumerate((9, 14, 19, 24, 29)):
        height = 22 + (i % 3) * 5
        pygame.draw.line(sprite, (31, 89, 38), (x, 35), (x + 2, 35 - height), 3)
        pygame.draw.line(sprite, (68, 130, 58), (x + 1, 35), (x + 3, 36 - height), 1)
        pygame.draw.ellipse(sprite, (93, 75, 43), (x - 2, 11 + i, 5, 13))
    return sprite


def make_pebbles() -> pygame.Surface:
    sprite = pygame.Surface((38, 24), pygame.SRCALPHA)
    pebbles = [
        (8, 12, 4, (111, 116, 107)),
        (15, 9, 3, (135, 139, 128)),
        (22, 14, 4, (96, 101, 94)),
        (29, 10, 3, (124, 129, 119)),
        (18, 17, 2, (152, 155, 143)),
    ]
    for x, y, radius, color in pebbles:
        pygame.draw.circle(sprite, color, (x, y), radius)
        pygame.draw.circle(sprite, (70, 74, 70), (x, y), radius, 1)
    return sprite


def make_flower(color: tuple[int, int, int]) -> pygame.Surface:
    sprite = pygame.Surface((24, 30), pygame.SRCALPHA)
    pygame.draw.line(sprite, (35, 112, 48), (12, 26), (12, 12), 2)
    for dx, dy in ((0, -5), (5, 0), (0, 5), (-5, 0)):
        pygame.draw.circle(sprite, color, (12 + dx, 10 + dy), 4)
    pygame.draw.circle(sprite, (232, 190, 60), (12, 10), 3)
    return sprite


def make_river_segment() -> pygame.Surface:
    sprite = pygame.Surface((180, 58), pygame.SRCALPHA)
    pygame.draw.ellipse(sprite, (61, 105, 58), (0, 4, 180, 50))
    pygame.draw.ellipse(sprite, (126, 106, 68), (4, 8, 172, 42))
    pygame.draw.ellipse(sprite, (20, 92, 112), (8, 12, 164, 34))
    pygame.draw.ellipse(sprite, (46, 146, 185), (11, 15, 158, 28))
    pygame.draw.arc(sprite, (124, 204, 226), (26, 18, 118, 17), 0.1, 2.9, 3)
    pygame.draw.arc(sprite, (85, 176, 210), (54, 28, 88, 12), 0.2, 2.8, 2)
    return sprite


def make_hill_patch() -> pygame.Surface:
    sprite = pygame.Surface((180, 118), pygame.SRCALPHA)
    pygame.draw.ellipse(sprite, (30, 70, 30, 80), (12, 72, 156, 26))
    pygame.draw.polygon(sprite, (52, 108, 46), [(16, 78), (88, 22), (166, 78), (118, 103), (42, 98)])
    pygame.draw.polygon(sprite, (92, 156, 64), [(16, 78), (88, 22), (166, 78), (88, 89)])
    pygame.draw.polygon(sprite, (64, 126, 50), [(88, 89), (166, 78), (118, 103), (42, 98)])
    pygame.draw.line(sprite, (137, 185, 86), (50, 63), (126, 58), 4)
    for y in (67, 78, 88):
        pygame.draw.arc(sprite, (75, 137, 58), (38, y - 18, 105, 28), 0.2, 2.8, 2)
    pygame.draw.line(sprite, (38, 92, 42), (50, 95), (135, 92), 3)
    return sprite


def main() -> None:
    pygame.init()
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    save(ellipse_sprite((160, 72), (39, 132, 50)), "meadow_0.png")
    save(ellipse_sprite((160, 72), (49, 142, 56)), "meadow_1.png")
    save(ellipse_sprite((160, 72), (72, 148, 58)), "meadow_2.png")
    save(ellipse_sprite((80, 34), (41, 126, 48)), "grass_patch.png")
    save(ellipse_sprite((90, 42), (126, 112, 70), (101, 92, 62)), "dirt_patch.png")
    save(ellipse_sprite((86, 34), (174, 149, 89), (139, 118, 75)), "sand_bar.png")
    save(make_reeds(), "reeds.png")
    save(make_pebbles(), "pebble_cluster.png")
    save(make_river_segment(), "river_segment.png")
    save(make_hill_patch(), "hill_patch.png")

    flower_colors = [(245, 224, 80), (238, 116, 144), (190, 140, 245), (245, 245, 245)]
    for index, color in enumerate(flower_colors):
        save(make_flower(color), f"flower_{index}.png")


if __name__ == "__main__":
    main()
