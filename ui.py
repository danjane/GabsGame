import math

import pygame


def draw_marker_line(
    screen: pygame.Surface,
    small_font: pygame.font.Font,
    player_rect: pygame.Rect,
    target_pos: tuple[int, int],
    label: str,
    label_color: tuple[int, int, int] = (255, 255, 255),
) -> None:
    px, py = player_rect.center
    tx, ty = target_pos

    pygame.draw.line(screen, label_color, (px, py), (tx, ty), 4)

    angle = math.atan2(ty - py, tx - px)
    head_len = 14
    left = (tx - head_len * math.cos(angle - 0.5), ty - head_len * math.sin(angle - 0.5))
    right = (tx - head_len * math.cos(angle + 0.5), ty - head_len * math.sin(angle + 0.5))
    pygame.draw.polygon(screen, label_color, [(tx, ty), left, right])

    surf = small_font.render(label, True, (0, 0, 0))
    pad = 6
    bg = pygame.Rect(tx + 10, ty - 12, surf.get_width() + pad * 2, 26)
    pygame.draw.rect(screen, label_color, bg)
    screen.blit(surf, (bg.x + pad, bg.y + 6))


def draw_panel(
    screen: pygame.Surface,
    font: pygame.font.Font,
    small_font: pygame.font.Font,
    width: int,
    resource_types: dict[str, dict[str, int]],
    resource_name: str,
) -> None:
    panel_w = 260
    panel_h = 160
    x = width - panel_w - 10
    y = 10

    pygame.draw.rect(screen, (0, 0, 0), (x, y, panel_w, panel_h))
    pygame.draw.rect(screen, (255, 255, 255), (x, y, panel_w, panel_h), 2)

    title = font.render(f"Details: {resource_name}", True, (255, 255, 255))
    screen.blit(title, (x + 10, y + 10))

    lines_y = y + 45
    if resource_name in resource_types:
        for key, value in resource_types[resource_name].items():
            line = small_font.render(f"- {key}: {value}", True, (255, 255, 255))
            screen.blit(line, (x + 12, lines_y))
            lines_y += 24

    hint = small_font.render("Click item again (or ESC) to close.", True, (200, 200, 200))
    screen.blit(hint, (x + 10, y + panel_h - 28))


def draw_craft_menu(
    screen: pygame.Surface,
    font: pygame.font.Font,
    small_font: pygame.font.Font,
    craft_panel: pygame.Rect,
    craft_btn_axe: pygame.Rect,
    craft_btn_pick: pygame.Rect,
    inventory: dict[str, int | bool],
    axe_cost_wood: int,
    pick_cost_wood: int,
    pick_cost_stone: int,
) -> None:
    pygame.draw.rect(screen, (0, 0, 0), craft_panel)
    pygame.draw.rect(screen, (255, 255, 255), craft_panel, 2)

    title = font.render("Crafting (only at home)", True, (255, 255, 255))
    screen.blit(title, (craft_panel.x + 10, craft_panel.y + 10))

    axe_label = f"Craft Axe (cost: {axe_cost_wood} wood)  [{'OWNED' if inventory['axe'] else 'click'}]"
    pick_label = (
        f"Craft Pickaxe (cost: {pick_cost_wood} wood + {pick_cost_stone} stone)  "
        f"[{'OWNED' if inventory['pickaxe'] else 'click'}]"
    )

    can_axe = (not inventory["axe"]) and (inventory["wood+branches"] >= axe_cost_wood)
    can_pick = (
        (not inventory["pickaxe"])
        and (inventory["wood+branches"] >= pick_cost_wood)
        and (inventory["stone"] >= pick_cost_stone)
    )

    pygame.draw.rect(screen, (40, 40, 40), craft_btn_axe)
    pygame.draw.rect(screen, (255, 255, 255), craft_btn_axe, 1)
    pygame.draw.rect(screen, (40, 40, 40), craft_btn_pick)
    pygame.draw.rect(screen, (255, 255, 255), craft_btn_pick, 1)

    axe_color = (255, 255, 255) if can_axe else (170, 170, 170)
    pick_color = (255, 255, 255) if can_pick else (170, 170, 170)
    axe_surf = small_font.render(axe_label, True, axe_color)
    pick_surf = small_font.render(pick_label, True, pick_color)

    screen.blit(axe_surf, (craft_btn_axe.x + 8, craft_btn_axe.y + 10))
    screen.blit(pick_surf, (craft_btn_pick.x + 8, craft_btn_pick.y + 10))

    hint = small_font.render("Press C to close.", True, (200, 200, 200))
    screen.blit(hint, (craft_panel.x + 10, craft_panel.y + craft_panel.height - 28))
