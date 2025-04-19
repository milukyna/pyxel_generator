import random

import pyxel

WIDTH, HEIGHT = 160, 120
LANES = [40, 72, 104, 136]
CAT_Y = HEIGHT - 24
MAX_LIVES = 3


class CafeAuLaitGame:
    def reset(self):
        self.cat_lane = 1
        self.beans = []  # Each is [lane, y]
        self.obstacles = []
        self.score = 0
        self.lives = MAX_LIVES
        self.game_over = False
        self.frame = 0

    def __init__(self):
        pyxel.init(WIDTH, HEIGHT, title="カフェオレキャットの豆キャッチ！")

        pyxel.image(0).load(0, 0, "./cat.png")
        pyxel.image(0).load(16, 0, "./bean.png")
        pyxel.image(0).load(32, 0, "./obstacle.png")

        self.reset()
        pyxel.run(self.update, self.draw)

    def update(self):
        if self.game_over:
            if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
                self.reset()
            return

        # クリックでレーン移動（左右循環）
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            self.cat_lane = (self.cat_lane + 1) % len(LANES)

        self.frame += 1

        # 新しいアイテム生成（豆と障害物）
        if self.frame % 20 == 0:
            lane = random.randint(0, len(LANES) - 1)
            if random.random() < 0.7:
                self.beans.append([lane, -16])
            else:
                self.obstacles.append([lane, -16])

        # アイテム移動
        speed = 2

        for b in self.beans[:]:
            b[1] += speed
            if b[1] > HEIGHT:
                self.beans.remove(b)

        for o in self.obstacles[:]:
            o[1] += speed
            if o[1] > HEIGHT:
                self.obstacles.remove(o)

        # 衝突判定
        cat_x = LANES[self.cat_lane]
        cat_y = CAT_Y
        cat_rect = (cat_x, cat_y, 16, 16)

        def rects_intersect(r1, r2):
            x1, y1, w1, h1 = r1
            x2, y2, w2, h2 = r2
            return x1 < x2 + w2 and x1 + w1 > x2 and y1 < y2 + h2 and y1 + h1 > y2

        for b in self.beans[:]:
            bean_x = LANES[b[0]]
            bean_y = b[1]
            if rects_intersect(cat_rect, (bean_x, bean_y, 16, 16)):
                self.beans.remove(b)
                self.score += 1

        for o in self.obstacles[:]:
            obs_x = LANES[o[0]]
            obs_y = o[1]
            if rects_intersect(cat_rect, (obs_x, obs_y, 16, 16)):
                self.obstacles.remove(o)
                self.lives -= 1
                if self.lives <= 0:
                    self.game_over = True

    def draw(self):
        pyxel.cls(10)  # 明るいクリーム色背景

        # 柱やコーヒー層っぽくレーン区切りライン描画
        for x in [56, 88, 120]:
            pyxel.line(x, 0, x, HEIGHT, 7)

        # キャット描画
        cat_x = LANES[self.cat_lane]
        pyxel.blt(cat_x, CAT_Y, 0, 0, 0, 16, 16, 0)

        # 豆描画
        for b in self.beans:
            x = LANES[b[0]]
            y = b[1]
            pyxel.blt(x, y, 0, 16, 0, 16, 16, 0)

        # 障害物描画
        for o in self.obstacles:
            x = LANES[o[0]]
            y = o[1]
            pyxel.blt(x, y, 0, 32, 0, 16, 16, 0)

        # スコアと残機表示
        pyxel.text(5, 5, f"SCORE: {self.score}", 7)
        pyxel.text(5, 15, f"LIVES: {self.lives}", 8)

        # ゲームオーバー
        if self.game_over:
            pyxel.text(WIDTH // 2 - 40, HEIGHT // 2, "GAME OVER", 8)
            pyxel.text(
                WIDTH // 2 - 70,
                HEIGHT // 2 + 10,
                "Click to Restart",
                pyxel.frame_count % 16,
            )


if __name__ == "__main__":
    CafeAuLaitGame()
