import pyxel
import random

WIDTH, HEIGHT = 160, 120
CAT_Y = HEIGHT - 20
LEFT_LANE = WIDTH // 4
RIGHT_LANE = WIDTH * 3 // 4
MOVING_SPEED = 2

class DripCoffeeGame:
    def reset(self):
        self.cat_x = LEFT_LANE
        self.cat_y = CAT_Y
        self.cat_vh = 0
        self.moving = False
        self.position = "LEFT"  # "LEFT" or "RIGHT"
        self.beans = []  # list of (x, y)
        self.obstacles = []  # list of (x, y)
        self.score = 0
        self.game_over = False

    def __init__(self):
        pyxel.init(WIDTH, HEIGHT, title="ドリップコーヒードリーム")
        pyxel.image(0).load(0, 0, "../assets/img/cat.png")
        pyxel.image(0).load(16, 0, "../assets/img/bean.png")
        pyxel.image(0).load(32, 0, "../assets/img/obstacle.png")

        self.reset()
        self.spawn_timer = 0
        pyxel.run(self.update, self.draw)

    def update(self):
        if self.game_over:
            if pyxel.btnp(pyxel.KEY_R):
                self.reset()
            return

        if pyxel.btnp(pyxel.KEY_SPACE):
            if self.position == "LEFT":
                self.cat_vx = MOVING_SPEED
                self.position = "RIGHT"
                self.moving = True
            else:
                self.cat_vx = -MOVING_SPEED
                self.position = "LEFT"
                self.moving = True

        # 猫のジャンプ更新
        if self.moving:
            self.cat_x += self.cat_vx
            if self.cat_x < LEFT_LANE and self.position == "LEFT":
                self.cat_x = LEFT_LANE
                self.cat_vx = 0
            elif self.cat_x > RIGHT_LANE and self.position == "RIGHT":
                self.cat_x = RIGHT_LANE
                self.cat_vx = 0

        # アイテムと障害物をスポーン
        self.spawn_timer += 1
        if self.spawn_timer > 30:
            self.spawn_timer = 0
            L = random.randint(0, 3)
            if L == 0:
                xs = [LEFT_LANE]
            elif L == 1:
                xs = [RIGHT_LANE]
            else:
                xs = [LEFT_LANE, RIGHT_LANE]
            for x in xs:
                if random.random() < 0.7:
                    self.beans.append([x, 0])
                else:
                    self.obstacles.append([x, 0])

        # 落下と衝突判定
        for bean in self.beans[:]:
            bean[1] += 3
            if bean[1] > HEIGHT:
                self.beans.remove(bean)
            elif self.check_collision(self.cat_x, self.cat_y, bean[0], bean[1]):
                self.beans.remove(bean)
                self.score += 1

        for obs in self.obstacles[:]:
            obs[1] += 4
            if obs[1] > HEIGHT:
                self.obstacles.remove(obs)
            elif self.check_collision(self.cat_x, self.cat_y, obs[0], obs[1]):
                self.obstacles.remove(obs)
                self.game_over = True

        # 猫の移動はスペースキーのみなので固定x

    def check_collision(self, x1, y1, x2, y2):
        # 簡単な矩形衝突判定
        return (x1 < x2 + 16 and x1 + 16 > x2 and
                y1 < y2 + 16 and y1 + 16 > y2)

    def draw(self):
        pyxel.cls(7)
        # 猫の描画
        pyxel.blt(self.cat_x, self.cat_y - 16, 0, 0, 0, 16, 16, 0)

        # 豆の描画
        for bean in self.beans:
            pyxel.blt(bean[0], bean[1], 0, 16, 0, 16, 16, 0)

        # 障害物の描画
        for obs in self.obstacles:
            pyxel.blt(obs[0], obs[1], 0, 32, 0, 16, 16, 0)

        pyxel.text(5, 5, f"Score: {self.score}", 0)

        if self.game_over:
            pyxel.text(WIDTH // 2 - 30, HEIGHT // 2, "GAME OVER", 8)
            pyxel.text(WIDTH // 2 - 50, HEIGHT // 2 + 10, "Press R to Restart", pyxel.frame_count % 16)

DripCoffeeGame()
