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
    QUEST_COUNT,
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
        self.iso_scale_x = 0.9
        self.iso_scale_y = 0.45
        self.player_sprite: pygame.Surface | None = None
        self.load_player_sprite()

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
        self.stats = {
            "wood_collected": 0,
            "stone_collected": 0,
            "rare_collected": 0,
            "fires_made": 0,
            "trees_cut": 0,
            "stones_mined": 0,
            "home_returns": 0,
        }
        self.total_quests = QUEST_COUNT
        self.completed_quests = 0
        self.quest_ready_to_turn_in = False
        self.last_quest_kind: str | None = None
        self.current_quest: dict[str, int | str] | None = None
        self.assign_next_quest()

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

    def load_player_sprite(self) -> None:
        sprite_path = "assets/sprites/player/player.png"
        try:
            sprite = pygame.image.load(sprite_path).convert_alpha()
            self.player_sprite = pygame.transform.smoothscale(sprite, (96, 96))
        except (pygame.error, FileNotFoundError):
            self.player_sprite = None

    def iso_point(self, wx: float, wy: float) -> tuple[int, int]:
        dx = wx - self.player.centerx
        dy = wy - self.player.centery
        sx = int((dx - dy) * self.iso_scale_x + WIDTH / 2)
        sy = int((dx + dy) * self.iso_scale_y + HEIGHT * 0.48)
        return sx, sy

    def iso_rect_poly(self, rect: pygame.Rect) -> list[tuple[int, int]]:
        tl = self.iso_point(rect.left, rect.top)
        tr = self.iso_point(rect.right, rect.top)
        br = self.iso_point(rect.right, rect.bottom)
        bl = self.iso_point(rect.left, rect.bottom)
        return [tl, tr, br, bl]

    def draw_iso_prism(
        self,
        surface: pygame.Surface,
        base_rect: pygame.Rect,
        height: int,
        top_color: tuple[int, int, int],
        left_color: tuple[int, int, int],
        right_color: tuple[int, int, int],
    ) -> None:
        base = self.iso_rect_poly(base_rect)
        top = [(x, y - height) for x, y in base]
        pygame.draw.polygon(surface, left_color, [base[3], base[2], top[2], top[3]])
        pygame.draw.polygon(surface, right_color, [base[1], base[2], top[2], top[1]])
        pygame.draw.polygon(surface, top_color, top)

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
        if self.inventory["wood+branches"] >= 1 and self.inventory["stone"] >= 2:
            self.inventory["wood+branches"] -= 1
            self.inventory["stone"] -= 2
            self.inventory["fire"] += 1
            self.stats["fires_made"] += 1
            self.show_message("Fire made! (-1 wood, -2 stone)")
        else:
            self.show_message("Need 1 wood + 2 stone to make fire!")

    def go_home(self) -> None:
        self.action_mode = None
        self.action_target_index = None
        self.player.x, self.player.y = START_POS
        self.stats["home_returns"] += 1
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

    def metric_for_quest(self, kind: str) -> int:
        if kind == "build_house":
            return 1 if self.house_built else 0
        if kind == "collect_wood":
            return int(self.stats["wood_collected"])
        if kind == "collect_stone":
            return int(self.stats["stone_collected"])
        if kind == "collect_rare":
            return int(self.stats["rare_collected"])
        if kind == "craft_fire":
            return int(self.stats["fires_made"])
        if kind == "cut_trees":
            return int(self.stats["trees_cut"])
        if kind == "mine_stones":
            return int(self.stats["stones_mined"])
        if kind == "go_home":
            return int(self.stats["home_returns"])
        return 0

    def quest_progress(self) -> tuple[int, int]:
        if self.current_quest is None:
            return (0, 0)

        kind = str(self.current_quest["kind"])
        target = int(self.current_quest["target"])
        start = int(self.current_quest["start"])
        current = self.metric_for_quest(kind) - start
        current = max(0, min(current, target))
        return (current, target)

    def current_quest_completed(self) -> bool:
        if self.current_quest is None:
            return False
        current, target = self.quest_progress()
        return current >= target

    def quest_label(self, kind: str, target: int) -> str:
        if kind == "build_house":
            return "Build a house at home (B)"
        if kind == "collect_wood":
            return f"Collect {target} wood"
        if kind == "collect_stone":
            return f"Collect {target} stone"
        if kind == "collect_rare":
            return f"Collect {target} rare stone"
        if kind == "craft_fire":
            return f"Make {target} fire (F)"
        if kind == "cut_trees":
            return f"Cut {target} trees (L)"
        if kind == "mine_stones":
            return f"Mine {target} stones (X)"
        if kind == "go_home":
            return f"Return home {target} times (🏠)"
        return "Complete objective"

    def assign_next_quest(self) -> None:
        if self.completed_quests >= self.total_quests:
            self.current_quest = None
            return

        kinds = ["collect_wood", "collect_stone", "collect_rare", "craft_fire", "cut_trees", "mine_stones", "go_home"]
        if not self.house_built:
            kinds.append("build_house")
        if self.last_quest_kind in kinds and len(kinds) > 1:
            kinds.remove(str(self.last_quest_kind))

        kind = random.choice(kinds)
        if kind == "build_house":
            target = 1
        elif kind == "collect_rare":
            target = random.randint(1, 2)
        elif kind == "craft_fire":
            target = random.randint(1, 3)
        elif kind == "go_home":
            target = random.randint(2, 4)
        else:
            target = random.randint(2, 5)

        start = self.metric_for_quest(kind)
        label = self.quest_label(kind, target)
        self.current_quest = {"kind": kind, "target": target, "start": start, "label": label}
        self.last_quest_kind = kind

    def complete_and_turn_in_quest(self) -> None:
        if self.current_quest is None:
            return
        self.completed_quests += 1
        self.quest_ready_to_turn_in = False
        if self.completed_quests >= self.total_quests:
            self.current_quest = None
            self.show_message("All quests complete! 🎉", seconds=3.0)
            return

        self.assign_next_quest()
        if self.current_quest is not None:
            self.show_message(f"New quest: {self.current_quest['label']}", seconds=2.5)

    def update_quest_status(self) -> None:
        if self.current_quest is None or self.quest_ready_to_turn_in:
            return
        if self.current_quest_completed():
            self.quest_ready_to_turn_in = True
            self.show_message("Quest done! Press 🏠 to claim next quest.", seconds=3.0)

    def add_wood_drop(self) -> None:
        wood_type = random.choice(list(self.resource_types["wood+branches"].keys()))
        self.inventory["wood+branches"] += 1
        self.resource_types["wood+branches"][wood_type] += 1
        self.stats["wood_collected"] += 1
        self.show_message(f"+1 wood ({wood_type})")

    def add_stone_drop(self) -> None:
        stone_type = random.choice(list(self.resource_types["stone"].keys()))
        self.inventory["stone"] += 1
        self.resource_types["stone"][stone_type] += 1
        self.stats["stone_collected"] += 1

        got_rare = random.random() < RARE_DROP_CHANCE
        if got_rare:
            rare_type = random.choice(list(self.resource_types["rare_stone"].keys()))
            self.inventory["rare_stone"] += 1
            self.resource_types["rare_stone"][rare_type] += 1
            self.stats["rare_collected"] += 1
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
            if self.quest_ready_to_turn_in:
                self.complete_and_turn_in_quest()

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
            self.stats["trees_cut"] += 1
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
            self.stats["stones_mined"] += 1
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
        self.update_quest_status()

    def draw_world(self) -> None:
        self.screen.fill((22, 96, 42))

        ground = pygame.Rect(-2200, -2200, 4400, 4400)
        pygame.draw.polygon(self.screen, (34, 139, 34), self.iso_rect_poly(ground))

        home_base = self.iso_rect_poly(self.home_area)
        pygame.draw.polygon(self.screen, (20, 110, 20), home_base, 2)

        drawables: list[tuple[int, str, pygame.Rect]] = []
        for tree in self.trees:
            drawables.append((tree.bottom, "tree", tree))
        for stone in self.stones:
            drawables.append((stone.bottom, "stone", stone))
        if self.house_built:
            house_rect = pygame.Rect(self.home_area.x + 15, self.home_area.y + 15, 70, 70)
            drawables.append((house_rect.bottom, "house", house_rect))
        drawables.append((self.player.bottom, "player", self.player))
        drawables.sort(key=lambda item: item[0])

        for _, kind, rect in drawables:
            if kind == "tree":
                trunk = pygame.Rect(rect.x + 18, rect.y + 50, 14, 20)
                canopy = rect.inflate(10, 0).move(-5, -18)
                self.draw_iso_prism(
                    self.screen,
                    trunk,
                    height=26,
                    top_color=(145, 90, 35),
                    left_color=(95, 55, 20),
                    right_color=(120, 70, 30),
                )
                self.draw_iso_prism(
                    self.screen,
                    canopy,
                    height=24,
                    top_color=(30, 145, 45),
                    left_color=(18, 95, 28),
                    right_color=(22, 115, 34),
                )
            elif kind == "stone":
                self.draw_iso_prism(
                    self.screen,
                    rect,
                    height=14,
                    top_color=(145, 145, 145),
                    left_color=(95, 95, 95),
                    right_color=(115, 115, 115),
                )
            elif kind == "house":
                self.draw_iso_prism(
                    self.screen,
                    rect,
                    height=34,
                    top_color=(170, 130, 90),
                    left_color=(130, 90, 60),
                    right_color=(150, 110, 70),
                )
                roof = self.iso_rect_poly(rect)
                roof_peak = ((roof[0][0] + roof[1][0]) // 2, min(roof[0][1], roof[1][1]) - 24)
                pygame.draw.polygon(self.screen, (120, 60, 40), [roof[0], roof[1], roof_peak])
            elif kind == "player":
                if self.player_sprite is not None:
                    px, py = self.iso_point(rect.centerx, rect.centery)
                    # Anchor sprite so feet align near the character's world position.
                    sx = px - self.player_sprite.get_width() // 2
                    sy = py - self.player_sprite.get_height() + 22
                    self.screen.blit(self.player_sprite, (sx, sy))
                else:
                    self.draw_iso_prism(
                        self.screen,
                        rect,
                        height=20,
                        top_color=(170, 98, 38),
                        left_color=(110, 62, 24),
                        right_color=(138, 78, 30),
                    )

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
        if self.completed_quests >= self.total_quests:
            qs = self.font.render("All quests complete! 🎉", True, (0, 0, 0))
            width = qs.get_width() + 16
            pygame.draw.rect(self.screen, (255, 255, 0), ((WIDTH - width) // 2, 10, width, 35))
            self.screen.blit(qs, ((WIDTH - qs.get_width()) // 2, 17))
        elif self.quest_ready_to_turn_in:
            text = f"Quest {self.completed_quests + 1}/{self.total_quests} done! Press 🏠 for next."
            qs = self.font.render(text, True, (255, 255, 0))
            width = qs.get_width() + 16
            pygame.draw.rect(self.screen, (0, 0, 0), ((WIDTH - width) // 2, 10, width, 35))
            self.screen.blit(qs, ((WIDTH - qs.get_width()) // 2, 17))
        else:
            current, target = self.quest_progress()
            label = str(self.current_quest["label"]) if self.current_quest is not None else "No quest"
            text = f"Quest {self.completed_quests + 1}/{self.total_quests}: {label} ({current}/{target})"
            qs = self.font.render(text, True, (255, 255, 0))
            width = qs.get_width() + 16
            pygame.draw.rect(self.screen, (0, 0, 0), ((WIDTH - width) // 2, 10, width, 35))
            self.screen.blit(qs, ((WIDTH - qs.get_width()) // 2, 17))

    def draw_help_and_message(self) -> None:
        help_text = "Move: arrows | Cut: L | Mine: X | Fire: F (1 wood + 2 stone) | Build: B (home) | Craft: C (home) | Click inventory | 🏠"
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
        if self.current_quest is None:
            return

        kind = str(self.current_quest["kind"])
        player_screen = self.iso_point(self.player.centerx, self.player.centery)
        marker_player_rect = pygame.Rect(player_screen[0] - 2, player_screen[1] - 2, 4, 4)

        if self.quest_ready_to_turn_in or kind in ("build_house", "go_home"):
            draw_marker_line(
                self.screen,
                self.small_font,
                marker_player_rect,
                self.iso_point(self.home_area.centerx, self.home_area.centery),
                "Go home",
                label_color=(255, 255, 0),
            )

        if kind in ("mine_stones", "collect_rare"):
            nearest_stone = nearest_rect(self.player, self.stones)
            if nearest_stone is not None:
                draw_marker_line(
                    self.screen,
                    self.small_font,
                    marker_player_rect,
                    self.iso_point(nearest_stone.centerx, nearest_stone.centery),
                    "Mine for rare stones",
                    label_color=(180, 80, 220),
                )
        elif kind in ("cut_trees", "collect_wood"):
            nearest_tree = nearest_rect(self.player, self.trees)
            if nearest_tree is not None:
                draw_marker_line(
                    self.screen,
                    self.small_font,
                    marker_player_rect,
                    self.iso_point(nearest_tree.centerx, nearest_tree.centery),
                    "Find trees",
                    label_color=(100, 220, 120),
                )

    def draw(self) -> None:
        self.draw_world()
        self.draw_markers()

        self.draw_inventory()
        self.draw_quest_banner()
        self.draw_help_and_message()
        self.draw_action_progress()
        self.draw_home_and_panels()
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
