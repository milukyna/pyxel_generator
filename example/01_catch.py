import random

import pyxel

WIDTH, HEIGHT = 160, 120
MAX_LIVES = 3
SPAWN_INTERVAL = 20
SPEED = 2


class CoffeeJellyCatcher:
    def reset(self):
        self.cat_x = WIDTH // 2
        self.cat_y = HEIGHT - 20
        self.lives = MAX_LIVES
        self.score = 0
        self.beans = []  # list of [x, y]
        self.obstacles = []  # list of [x, y]
        self.spawn_counter = 0
        self.game_over = False

    def __init__(self):
        pyxel.init(WIDTH, HEIGHT, title="コーヒーゼリーキャッチャー")
        pyxel.image(0).load(0, 0, "./cat.png")
        pyxel.image(0).load(16, 0, "./bean.png")
        pyxel.image(0).load(32, 0, "./obstacle.png")
        self.reset()
        pyxel.run(self.update, self.draw)

    def update(self):
        if self.game_over:
            if pyxel.btnp(pyxel.KEY_R):
                self.reset()
            return

        # スペースキーでジャンプ
        if pyxel.btnp(pyxel.KEY_SPACE) and self.cat_y == HEIGHT - 20:
            self.cat_vy = -6
        else:
            if not hasattr(self, "cat_vy"):
                self.cat_vy = 0

        # 重力とジャンプ処理
        self.cat_vy += 0.3
        self.cat_y += self.cat_vy

        if self.cat_y >= HEIGHT - 20:
            self.cat_y = HEIGHT - 20
            self.cat_vy = 0

        # 出現処理
        self.spawn_counter += 1
        if self.spawn_counter > SPAWN_INTERVAL:
            self.spawn_counter = 0
            # 豆か障害物をランダムに生成
            if random.random() < 0.7:
                x = random.randint(0, WIDTH - 16)
                self.beans.append([x, 0])
            else:
                x = random.randint(0, WIDTH - 16)
                self.obstacles.append([x, 0])

        # 落下処理と当たり判定
        for b in self.beans[:]:
            b[1] += SPEED
            if self.check_collision(self.cat_x, self.cat_y, b[0], b[1]):
                self.beans.remove(b)
                self.score += 1
            elif b[1] > HEIGHT:
                self.beans.remove(b)

        for o in self.obstacles[:]:
            o[1] += SPEED
            if self.check_collision(self.cat_x, self.cat_y, o[0], o[1]):
                self.obstacles.remove(o)
                self.lives -= 1
                if self.lives <= 0:
                    self.game_over = True
            elif o[1] > HEIGHT:
                self.obstacles.remove(o)

    def check_collision(self, x1, y1, x2, y2):
        return x1 < x2 + 16 and x1 + 16 > x2 and y1 < y2 + 16 and y1 + 16 > y2

    def draw(self):
        pyxel.cls(7)  # 薄い背景色
        # ネコを描く
        pyxel.blt(self.cat_x, int(self.cat_y), 0, 0, 0, 16, 16, 0)
        # 豆を描く
        for b in self.beans:
            pyxel.blt(b[0], b[1], 0, 16, 0, 16, 16, 0)
        # 障害物を描く
        for o in self.obstacles:
            pyxel.blt(o[0], o[1], 0, 32, 0, 16, 16, 0)
        # ライフ表示
        pyxel.text(5, 5, f"Lives: {self.lives}", 8)
        # スコア表示
        pyxel.text(5, 15, f"Score: {self.score}", 8)
        # ゲームオーバー表示
        if self.game_over:
            pyxel.text(WIDTH // 2 - 40, HEIGHT // 2, "GAME OVER", 8)
            pyxel.text(
                WIDTH // 2 - 50,
                HEIGHT // 2 + 10,
                "Press R to Restart",
                pyxel.frame_count % 16,
            )


CoffeeJellyCatcher()
