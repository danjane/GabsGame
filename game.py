import random
import sys

import pygame

from config import (
    AXE_COST_WOOD,
    CUT_TIME_SECONDS,
    CUT_TIME_WITH_AXE,
    FPS,
    HEIGHT,
    HOME_AREA_OFFSET,
    HOME_AREA_SIZE,
    INITIAL_STONE_COUNT,
    INITIAL_TREE_COUNT,
    MINE_TIME_SECONDS,
    PICK_COST_STONE,
    PICK_COST_WOOD,
    PLAYER_HEIGHT,
    PLAYER_SPEED,
    PLAYER_WIDTH,
    QUEST_TEXT,
    RARE_DROP_CHANCE,
    START_POS,
    STONE_RESPAWN_SECONDS,
    STONE_SIZE,
    TREE_RESPAWN_SECONDS,
    TREE_SIZE,
    WIDTH,
    WINDOW_TITLE,
)
from ui import draw_craft_menu, draw_marker_line, draw_panel
from world import is_near, nearest_rect, random_spawn_rect


class Game:
    def __init__(self) -> None:
        pygame.init()

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(WINDOW_TITLE)
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 28)
        self.small_font = pygame.font.SysFont(None, 22)

        self.player = pygame.Rect(START_POS[0], START_POS[1], PLAYER_WIDTH, PLAYER_HEIGHT)
        self.home_area = pygame.Rect(
            START_POS[0] - HOME_AREA_OFFSET[0],
            START_POS[1] - HOME_AREA_OFFSET[1],
            HOME_AREA_SIZE[0],
            HOME_AREA_SIZE[1],
        )

        self.trees = [
            random_spawn_rect(WIDTH, HEIGHT, self.home_area, TREE_SIZE[0], TREE_SIZE[1])
            for _ in range(INITIAL_TREE_COUNT)
        ]
        self.stones = [
            random_spawn_rect(WIDTH, HEIGHT, self.home_area, STONE_SIZE[0], STONE_SIZE[1])
            for _ in range(INITIAL_STONE_COUNT)
        ]
        self.respawn_queue: list[dict[str, float | str]] = []

        self.inventory: dict[str, int | bool] = {
            "wood+branches": 0,
            "stone": 0,
            "rare_stone": 0,
            "axe": False,
            "pickaxe": False,
            "fire": 0,
        }
        self.resource_types: dict[str, dict[str, int]] = {
            "wood+branches": {"oak": 0, "pine": 0},
            "stone": {"granite": 0, "limestone": 0},
            "rare_stone": {"ruby": 0, "sapphire": 0},
        }

        self.house_built = False
        self.quest_text = QUEST_TEXT

        self.action_mode: str | None = None
        self.action_timer = 0.0
        self.action_target_index: int | None = None

        self.message = ""
        self.message_timer = 0.0

        self.inv_item_rects: dict[str, pygame.Rect] = {}
        self.selected_panel: str | None = None

        self.home_button = pygame.Rect(10, HEIGHT - 60, 60, 50)
        self.craft_menu_open = False
        self.craft_panel = pygame.Rect(10, 60, 310, 170)
        self.craft_btn_axe = pygame.Rect(20, 100, 290, 40)
        self.craft_btn_pick = pygame.Rect(20, 145, 290, 40)

    def show_message(self, text: str, seconds: float = 2.0) -> None:
        self.message = text
        self.message_timer = seconds

    def start_cutting(self) -> None:
        if self.action_mode is not None or self.craft_menu_open:
            return

        for i, tree in enumerate(self.trees):
            if is_near(self.player, tree, distance=25):
                self.action_mode = "cut"
                self.action_timer = 0.0
                self.action_target_index = i
                return

        self.show_message("No tree nearby!")

    def start_mining(self) -> None:
        if self.action_mode is not None or self.craft_menu_open:
            return

        if not self.inventory["pickaxe"]:
            self.show_message("You need a pickaxe to mine! (Craft at home: C)")
            return

        for i, stone in enumerate(self.stones):
            if is_near(self.player, stone, distance=25):
                self.action_mode = "mine"
                self.action_timer = 0.0
                self.action_target_index = i
                return

        self.show_message("No stone nearby!")

    def try_make_fire(self) -> None:
        if self.inventory["stone"] >= 2:
            self.inventory["stone"] -= 2
            self.inventory["fire"] += 1
            self.show_message("Fire made! (-2 stone)")
        else:
            self.show_message("Need 2 stone to make fire!")

    def go_home(self) -> None:
        self.action_mode = None
        self.action_target_index = None
        self.player.x, self.player.y = START_POS
        self.show_message("Back home!")

    def try_build_house(self) -> None:
        if self.house_built:
            self.show_message("House already built!")
            return

        if not self.player.colliderect(self.home_area):
            self.show_message("Build at home area (green square).")
            return

        if self.inventory["wood+branches"] >= 2:
            self.inventory["wood+branches"] -= 2
            self.house_built = True
            self.show_message("House built! (-2 wood+branches)")
        else:
            self.show_message("Need 2 wood+branches to build a house!")

    def quest_done(self) -> bool:
        return self.house_built and self.inventory["rare_stone"] >= 2

    def add_wood_drop(self) -> None:
        wood_type = random.choice(list(self.resource_types["wood+branches"].keys()))
        self.inventory["wood+branches"] += 1
        self.resource_types["wood+branches"][wood_type] += 1
        self.show_message(f"+1 wood ({wood_type})")

    def add_stone_drop(self) -> None:
        stone_type = random.choice(list(self.resource_types["stone"].keys()))
        self.inventory["stone"] += 1
        self.resource_types["stone"][stone_type] += 1

        got_rare = random.random() < RARE_DROP_CHANCE
        if got_rare:
            rare_type = random.choice(list(self.resource_types["rare_stone"].keys()))
            self.inventory["rare_stone"] += 1
            self.resource_types["rare_stone"][rare_type] += 1
            self.show_message(f"+1 stone ({stone_type}) and +1 rare ({rare_type})!")
        else:
            self.show_message(f"+1 stone ({stone_type})")

    def try_craft_axe(self) -> None:
        if self.inventory["axe"]:
            self.show_message("You already have an axe!")
            return

        if self.inventory["wood+branches"] >= AXE_COST_WOOD:
            self.inventory["wood+branches"] -= AXE_COST_WOOD
            self.inventory["axe"] = True
            self.show_message("Axe crafted! Cutting is now faster (3s).")
        else:
            self.show_message("Not enough wood for axe.")

    def try_craft_pickaxe(self) -> None:
        if self.inventory["pickaxe"]:
            self.show_message("You already have a pickaxe!")
            return

        if self.inventory["wood+branches"] >= PICK_COST_WOOD:
            self.inventory["wood+branches"] -= PICK_COST_WOOD
            self.inventory["pickaxe"] = True
            self.show_message("Pickaxe crafted! You can now mine stones (X).")
        else:
            self.show_message("Not enough wood for pickaxe.")

    def handle_keydown(self, key: int) -> None:
        if key == pygame.K_l:
            self.start_cutting()
        if key == pygame.K_x:
            self.start_mining()
        if key == pygame.K_f:
            self.try_make_fire()
        if key == pygame.K_b:
            self.try_build_house()
        if key == pygame.K_ESCAPE:
            self.selected_panel = None
            self.craft_menu_open = False
        if key == pygame.K_c:
            if self.player.colliderect(self.home_area):
                self.craft_menu_open = not self.craft_menu_open
            else:
                self.show_message("Go to home area to craft (green square).")

    def handle_mouse_down(self, pos: tuple[int, int]) -> None:
        mx, my = pos

        if self.home_button.collidepoint(mx, my):
            self.craft_menu_open = False
            self.go_home()

        for name, rect in self.inv_item_rects.items():
            if rect.collidepoint(mx, my):
                if self.selected_panel == name:
                    self.selected_panel = None
                else:
                    self.selected_panel = name

        if self.craft_menu_open:
            if self.craft_btn_axe.collidepoint(mx, my):
                self.try_craft_axe()
            if self.craft_btn_pick.collidepoint(mx, my):
                self.try_craft_pickaxe()

    def handle_events(self) -> bool:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.KEYDOWN:
                self.handle_keydown(event.key)

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.handle_mouse_down(event.pos)

        return True

    def update_movement(self) -> None:
        keys = pygame.key.get_pressed()
        if self.action_mode is None and not self.craft_menu_open:
            if keys[pygame.K_LEFT]:
                self.player.x -= PLAYER_SPEED
            if keys[pygame.K_RIGHT]:
                self.player.x += PLAYER_SPEED
            if keys[pygame.K_UP]:
                self.player.y -= PLAYER_SPEED
            if keys[pygame.K_DOWN]:
                self.player.y += PLAYER_SPEED

            self.player.x = max(0, min(WIDTH - self.player.width, self.player.x))
            self.player.y = max(0, min(HEIGHT - self.player.height, self.player.y))

    def update_message_timer(self, dt: float) -> None:
        if self.message_timer > 0:
            self.message_timer -= dt
            if self.message_timer <= 0:
                self.message = ""

    def update_respawns(self, dt: float) -> None:
        for item in self.respawn_queue[:]:
            item["time"] -= dt
            if item["time"] <= 0:
                if item["kind"] == "tree":
                    self.trees.append(random_spawn_rect(WIDTH, HEIGHT, self.home_area, TREE_SIZE[0], TREE_SIZE[1]))
                elif item["kind"] == "stone":
                    self.stones.append(random_spawn_rect(WIDTH, HEIGHT, self.home_area, STONE_SIZE[0], STONE_SIZE[1]))
                self.respawn_queue.remove(item)

    def update_cut_action(self, dt: float) -> None:
        if self.action_target_index is None or self.action_target_index >= len(self.trees):
            self.action_mode = None
            return

        target = self.trees[self.action_target_index]
        if not is_near(self.player, target, distance=35):
            self.action_mode = None
            self.show_message("Cut cancelled (too far).")
            return

        self.action_timer += dt
        total_time = CUT_TIME_WITH_AXE if self.inventory["axe"] else CUT_TIME_SECONDS
        if self.action_timer >= total_time:
            self.trees.pop(self.action_target_index)
            self.respawn_queue.append({"time": TREE_RESPAWN_SECONDS, "kind": "tree"})
            self.action_mode = None
            self.action_target_index = None
            self.add_wood_drop()

    def update_mine_action(self, dt: float) -> None:
        if self.action_target_index is None or self.action_target_index >= len(self.stones):
            self.action_mode = None
            return

        target = self.stones[self.action_target_index]
        if not is_near(self.player, target, distance=35):
            self.action_mode = None
            self.show_message("Mining cancelled (too far).")
            return

        self.action_timer += dt
        if self.action_timer >= MINE_TIME_SECONDS:
            self.stones.pop(self.action_target_index)
            self.respawn_queue.append({"time": STONE_RESPAWN_SECONDS, "kind": "stone"})
            self.action_mode = None
            self.action_target_index = None
            self.add_stone_drop()

    def update_actions(self, dt: float) -> None:
        if self.action_mode == "cut":
            self.update_cut_action(dt)
        if self.action_mode == "mine":
            self.update_mine_action(dt)

    def update(self, dt: float) -> None:
        self.update_movement()
        self.update_message_timer(dt)
        self.update_respawns(dt)
        self.update_actions(dt)

    def draw_world(self) -> None:
        self.screen.fill((34, 139, 34))
        pygame.draw.rect(self.screen, (20, 110, 20), self.home_area, 3)

        if self.house_built:
            house_rect = pygame.Rect(self.home_area.x + 15, self.home_area.y + 15, 70, 70)
            pygame.draw.rect(self.screen, (160, 120, 80), house_rect)
            pygame.draw.polygon(
                self.screen,
                (120, 60, 40),
                [
                    (house_rect.x, house_rect.y),
                    (house_rect.x + house_rect.width, house_rect.y),
                    (house_rect.x + house_rect.width // 2, house_rect.y - 25),
                ],
            )

        for tree in self.trees:
            pygame.draw.rect(self.screen, (0, 100, 0), tree)
            trunk = pygame.Rect(tree.x + 18, tree.y + 50, 14, 20)
            pygame.draw.rect(self.screen, (120, 70, 20), trunk)

        for stone in self.stones:
            pygame.draw.rect(self.screen, (110, 110, 110), stone)
            pygame.draw.rect(self.screen, (80, 80, 80), stone.inflate(-10, -10))

        pygame.draw.rect(self.screen, (139, 69, 19), self.player)

    def draw_inventory(self) -> None:
        self.inv_item_rects.clear()
        x0, y0 = 10, 10
        bar_h = 40
        pygame.draw.rect(self.screen, (0, 0, 0), (x0, y0, 660, bar_h))

        items = [
            ("wood+branches", self.inventory["wood+branches"]),
            ("stone", self.inventory["stone"]),
            ("rare_stone", self.inventory["rare_stone"]),
            ("fire", self.inventory["fire"]),
        ]

        cursor_x = x0 + 10
        pad = 8
        for name, value in items:
            label = f"{name}: {value}"
            surf = self.font.render(label, True, (255, 255, 255))
            rect = pygame.Rect(cursor_x - 6, y0 + 6, surf.get_width() + 12, bar_h - 12)

            if self.selected_panel == name:
                pygame.draw.rect(self.screen, (60, 60, 60), rect)
            pygame.draw.rect(self.screen, (255, 255, 255), rect, 1)

            self.screen.blit(surf, (cursor_x, y0 + 10))
            self.inv_item_rects[name] = rect
            cursor_x += rect.width + pad

        tool_text = f"Axe: {'yes' if self.inventory['axe'] else 'no'}   Pickaxe: {'yes' if self.inventory['pickaxe'] else 'no'}"
        tool_surf = self.small_font.render(tool_text, True, (255, 255, 255))
        self.screen.blit(tool_surf, (x0 + 10, y0 + 44))

    def draw_quest_banner(self) -> None:
        if self.quest_done():
            qt = "Quest complete! 🎉"
            qs = self.font.render(qt, True, (0, 0, 0))
            width = qs.get_width() + 16
            pygame.draw.rect(self.screen, (255, 255, 0), ((WIDTH - width) // 2, 10, width, 35))
            self.screen.blit(qs, ((WIDTH - qs.get_width()) // 2, 17))
        else:
            qs = self.font.render(self.quest_text, True, (255, 255, 0))
            width = qs.get_width() + 16
            pygame.draw.rect(self.screen, (0, 0, 0), ((WIDTH - width) // 2, 10, width, 35))
            self.screen.blit(qs, ((WIDTH - qs.get_width()) // 2, 17))

    def draw_help_and_message(self) -> None:
        help_text = "Move: arrows | Cut: L | Mine: X | Fire: F | Build: B (home) | Craft: C (home) | Click inventory | 🏠"
        help_surf = self.small_font.render(help_text, True, (255, 255, 255))
        pygame.draw.rect(self.screen, (0, 0, 0), (80, HEIGHT - 45, help_surf.get_width() + 10, 35))
        self.screen.blit(help_surf, (85, HEIGHT - 38))

        if self.message:
            msg_surf = self.font.render(self.message, True, (255, 255, 255))
            width = msg_surf.get_width() + 16
            height = 34
            x = (WIDTH - width) // 2
            y = 55
            pygame.draw.rect(self.screen, (0, 0, 0), (x, y, width, height))
            self.screen.blit(msg_surf, (x + 8, y + 7))

    def draw_action_progress(self) -> None:
        if self.action_mode is None:
            return

        bar_w, bar_h = 300, 18
        bx = (WIDTH - bar_w) // 2
        by = 95

        if self.action_mode == "cut":
            total = CUT_TIME_WITH_AXE if self.inventory["axe"] else CUT_TIME_SECONDS
            label = "Cutting..."
        else:
            total = MINE_TIME_SECONDS
            label = "Mining..."

        progress = max(0.0, min(1.0, self.action_timer / total))
        pygame.draw.rect(self.screen, (0, 0, 0), (bx - 2, by - 2, bar_w + 4, bar_h + 4))
        pygame.draw.rect(self.screen, (80, 80, 80), (bx, by, bar_w, bar_h))
        pygame.draw.rect(self.screen, (200, 200, 200), (bx, by, int(bar_w * progress), bar_h))

        status = self.font.render(label, True, (255, 255, 255))
        self.screen.blit(status, (bx, by - 26))

    def draw_home_and_panels(self) -> None:
        pygame.draw.rect(self.screen, (0, 0, 0), self.home_button)
        pygame.draw.rect(self.screen, (255, 255, 255), self.home_button, 2)
        home_surf = self.font.render("🏠", True, (255, 255, 255))
        self.screen.blit(home_surf, (self.home_button.x + 18, self.home_button.y + 12))

        if self.selected_panel in ("wood+branches", "stone", "rare_stone"):
            draw_panel(
                self.screen,
                self.font,
                self.small_font,
                WIDTH,
                self.resource_types,
                self.selected_panel,
            )

        if self.craft_menu_open:
            draw_craft_menu(
                self.screen,
                self.font,
                self.small_font,
                self.craft_panel,
                self.craft_btn_axe,
                self.craft_btn_pick,
                self.inventory,
                AXE_COST_WOOD,
                PICK_COST_WOOD,
                PICK_COST_STONE,
            )

    def draw_markers(self) -> None:
        if not self.house_built:
            draw_marker_line(
                self.screen,
                self.small_font,
                self.player,
                self.home_area.center,
                "Build house (B) at home",
                label_color=(255, 255, 0),
            )

        if not self.quest_done() and self.inventory["rare_stone"] < 2:
            nearest_stone = nearest_rect(self.player, self.stones)
            if nearest_stone is not None:
                draw_marker_line(
                    self.screen,
                    self.small_font,
                    self.player,
                    nearest_stone.center,
                    "Mine for rare stones",
                    label_color=(180, 80, 220),
                )

    def draw(self) -> None:
        self.draw_world()
        self.draw_inventory()
        self.draw_quest_banner()
        self.draw_help_and_message()
        self.draw_action_progress()
        self.draw_home_and_panels()
        self.draw_markers()
        pygame.display.flip()

    def run(self) -> None:
        running = True
        while running:
            dt = self.clock.tick(FPS) / 1000.0
            running = self.handle_events()
            self.update(dt)
            self.draw()

        pygame.quit()
        sys.exit()
