"""
GameEngine: owns the hook and the fish, and runs one frame's worth of
game logic.

Starter version: the hook casts and retracts automatically in a
continuous loop - there's no player control over casting yet (that's
Task 3), only one fish type exists (Task 2 adds more), and there's no
round timer (Task 4). Catch detection also has a known bug (see
game/catch.py) that Task 1 asks you to fix.

Task 4 adds a 30-second round timer, Game Over state, and restart support.
"""

import pygame

from game.hook import Hook, IDLE
from game.fish import Fish
from game.catch import check_catch
from game.renderer import WIDTH, HEIGHT, SURFACE_Y, MAX_DEPTH_Y


class GameEngine:
    def __init__(self):
        self.hook = Hook(
            x=WIDTH / 2,
            surface_y=SURFACE_Y,
            max_depth_y=MAX_DEPTH_Y,
            speed=5
        )

        self.round_duration = 30
        self.start_time = pygame.time.get_ticks()
        self.time_left = self.round_duration
        self.game_over = False

        self.fish_list = [
            # Small, fast fish — 10 points
            Fish(
                x=100, y=180,
                speed=3,
                width=36, height=18,
                point_value=10,
                color=(80, 180, 220)
            ),

            # Large, slow fish — 20 points
            Fish(
                x=400, y=280,
                speed=-1,
                width=50, height=26,
                point_value=20,
                color=(220, 100, 80)
            ),

            # Medium, faster fish — 30 points
            Fish(
                x=250, y=380,
                speed=4,
                width=30, height=15,
                point_value=30,
                color=(100, 220, 120)
            ),
        ]

        self.hooked_fish = None
        self.score = 0

    def update(self):
        # Do nothing after the timer reaches zero
        if self.game_over:
            return

        elapsed = (pygame.time.get_ticks() - self.start_time) / 1000
        self.time_left = max(0, self.round_duration - elapsed)

        # Stop the game when the timer reaches zero
        if self.time_left <= 0:
            self.game_over = True
            return

        self.hook.update()

        for fish in self.fish_list:
            fish.update(WIDTH)

        if self.hooked_fish is not None:
            self.hooked_fish.x = self.hook.x
            self.hooked_fish.y = self.hook.y

            if self.hook.state == IDLE:
                self.score += self.hooked_fish.point_value
                self.hooked_fish = None

        else:
            caught = check_catch(self.hook, self.fish_list)

            if caught is not None:
                self.fish_list.remove(caught)
                self.hooked_fish = caught
                self.hooked_fish.x = self.hook.x
                self.hooked_fish.y = self.hook.y
                self.hook.catch_fish()

    def restart(self):
        self.hook.state = IDLE
        self.hook.y = self.hook.surface_y

        self.fish_list = [
            # Small, fast fish — 10 points
            Fish(
                x=100, y=180,
                speed=3,
                width=36, height=18,
                point_value=10,
                color=(80, 180, 220)
            ),

            # Large, slow fish — 20 points
            Fish(
                x=400, y=280,
                speed=-1,
                width=50, height=26,
                point_value=20,
                color=(220, 100, 80)
            ),

            # Medium, faster fish — 30 points
            Fish(
                x=250, y=380,
                speed=4,
                width=30, height=15,
                point_value=30,
                color=(100, 220, 120)
            ),
        ]

        self.hooked_fish = None
        self.score = 0
        self.start_time = pygame.time.get_ticks()
        self.time_left = self.round_duration
        self.game_over = False

    def draw(self, surface, font):
        from game import renderer

        draw_list = list(self.fish_list)

        if self.hooked_fish is not None:
            draw_list.append(self.hooked_fish)

        renderer.draw_scene(surface, self.hook, draw_list)

        renderer.draw_text(
            surface,
            font,
            f"Score: {self.score}",
            (10, 10)
        )

        renderer.draw_text(
            surface,
            font,
            f"Time: {max(0, int(self.time_left))}",
            (560, 10)
        )

        if self.game_over:
            renderer.draw_game_over(surface, font, self.score)