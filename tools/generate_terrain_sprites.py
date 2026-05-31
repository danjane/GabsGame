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

    flower_colors = [(245, 224, 80), (238, 116, 144), (190, 140, 245), (245, 245, 245)]
    for index, color in enumerate(flower_colors):
        save(make_flower(color), f"flower_{index}.png")


if __name__ == "__main__":
    main()
