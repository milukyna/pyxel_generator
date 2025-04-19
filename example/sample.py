import pyxel
import random

# 画面定数
WIDTH, HEIGHT = 160, 120
GROUND_Y = 96

# 生成率
BEAN_SPAWN_RATE = 0.05
OBS_SPAWN_RATE  = 0.025

# スクロール速度
SCROLL_SPEED = 1
SCROLL_SPEED_INC = 0.25
UPDATE_SPEED_DELTA = 900

class App:
    def __init__(self):
        pyxel.init(WIDTH, HEIGHT, title="Coffee Flight")
        # 画像読み込み (同じフォルダに cat.png, bean.png, obstacle.png を置く)
        pyxel.load("my_assets.pyxres")
        # pyxel.image(0).load(0,  0, "../assets/img/cat.png")
        # pyxel.image(0).load(16, 0, "../assets/img/bean.png")
        # pyxel.image(0).load(32, 0, "../assets/img/obstacle.png")

        self.reset()
        pyxel.run(self.update, self.draw)

    def reset(self):
        self.cat_y      = GROUND_Y
        self.cat_vy     = 0
        self.beans      = []   # [(x,y), ...]
        self.obs        = []   # [(x,y), ...]
        self.score      = 0
        self.frame_count = 0
        self.scroll_speed = SCROLL_SPEED
        self.game_over  = False

    def update(self):
        if self.game_over:
            if pyxel.btnp(pyxel.KEY_R):
                self.reset()
            return

        # --- キャットの動き ---
        if pyxel.btn(pyxel.KEY_SPACE):
            self.cat_vy = -4
        # 重力
        self.cat_vy += 0.25
        self.cat_y  += self.cat_vy

        # 地面と画面上部制限
        if self.cat_y > GROUND_Y:
            self.cat_y = GROUND_Y
            self.cat_vy = 0
        elif self.cat_y < 0:  # 上端の制限を追加
            self.cat_y = 0
            self.cat_vy = 0


        # --- 豆と障害物の生成 ---
        if random.random() < BEAN_SPAWN_RATE:
            y = random.randint(0, GROUND_Y+16)
            self.beans.append([WIDTH, y])
        if random.random() < OBS_SPAWN_RATE:
            y = random.randint(0, GROUND_Y+16)
            self.obs.append([WIDTH, y])

        # --- オブジェクト移動・衝突判定 ---
        new_beans = []
        for x, y in self.beans:
            x -= self.scroll_speed
            # 衝突？
            if abs(x + 8 - 16) < 12 and abs(y + 8 - self.cat_y - 8) < 12:
                self.score += self.scroll_speed
            elif x > -16:
                new_beans.append([x, y])
        self.beans = new_beans

        new_obs = []
        for x, y in self.obs:
            x -= self.scroll_speed
            if abs(x + 8 - 16) < 12 and abs(y + 8 - self.cat_y - 8) < 12:
                self.game_over = True
            elif x > -16:
                new_obs.append([x, y])
        self.obs = new_obs
        self.frame_count += 1
        if self.frame_count % int(UPDATE_SPEED_DELTA * self.scroll_speed) == 0:
            # スコア表示
            self.scroll_speed += SCROLL_SPEED_INC
    def draw(self):
        pyxel.cls(6)  # 背景色
        # 地面
        pyxel.line(0, GROUND_Y + 16, WIDTH, GROUND_Y + 16, 3)
        # キャット (バンク0, (0,0) サイズ16×16), 常に X=16
        pyxel.blt(16, int(self.cat_y), 0, 0,  0, 16, 16, 0)

        # 豆描画 (バンク0, (16,0))
        for x, y in self.beans:
            pyxel.blt(x, y, 0, 16, 0, 16, 16, 0)
        # 障害物描画 (バンク0, (32,0))
        for x, y in self.obs:
            pyxel.blt(x, y, 0, 32, 0, 16, 16, 0)

        # スコア・状態表示
        pyxel.text(5, 5, f"SCORE: {self.score}", 7)
        if self.game_over:
            pyxel.text(WIDTH//2 - 30, HEIGHT//2, "GAME OVER", 8)
            pyxel.text(WIDTH//2 - 40, HEIGHT//2 + 10, "PRESS R TO RESTART", 8)

if __name__ == "__main__":
    App()
