import pyxel
import random

WIDTH, HEIGHT = 160, 120
SWITCH_TIME = 30
CAT_TIME = 15

class Game:
    def __init__(self):
        pyxel.init(WIDTH, HEIGHT, title="Press Space to Catch Beans")

        pyxel.image(0).load(0, 0, "../assets/img/cat.png")
        pyxel.image(0).load(16, 0, "../assets/img/bean.png")
        pyxel.image(0).load(32, 0, "../assets/img/obstacle.png")

        self.reset()
        self.next_state()

        pyxel.run(self.update, self.draw)

    def next_state(self):
        if self.state == "cat":
            self.state = random.choice(["bean", "obstacle"])
            self.timer = SWITCH_TIME
        else:
            self.prev_state = self.state
            self.state = "cat"
            self.timer = CAT_TIME

    def reset(self):
        self.score = 0
        self.timer = 60
        self.state = "cat"
        self.prev_state = None
        self.game_over = False

    def update(self):
        if self.game_over:
            if pyxel.btnp(pyxel.KEY_R):
                self.reset()
            return

        self.timer -= 1

        if self.state != "cat" and pyxel.btnp(pyxel.KEY_SPACE):
            if self.state == "bean":
                self.score += 1
                self.next_state()
            else:
                print("Game Over! You hit an obstacle!")
                self.game_over = True
        elif self.state == "cat" and self.timer <= 0:
                self.next_state()
        elif self.state == "bean" and self.timer <= 0:
            self.game_over = True
            print("Game Over! You dont catch the bean!")
        elif self.state == "obstacle" and self.timer <= 0:
            self.score += 1
            self.next_state()

    def draw(self):
        pyxel.cls(0)

        if self.state == "cat":
            pyxel.blt(WIDTH / 2 - 8, HEIGHT / 2 - 24, 0, 0, 0, 16, 16, 0)
        elif self.state == "bean":
            pyxel.blt(WIDTH / 2 - 8, HEIGHT / 2, 0, 16, 0, 16, 16, 0)
        else:
            pyxel.blt(WIDTH / 2 - 8, HEIGHT / 2, 0, 32, 0, 16, 16, 0)

        pyxel.text(5, 5, f"Score: {self.score}", 7)

        if self.game_over:
            pyxel.text(WIDTH / 2 - 20, HEIGHT / 2 + 30, "GAME OVER", pyxel.frame_count % 16)
            pyxel.text(WIDTH / 2 - 35, HEIGHT / 2 + 40, "Press R to Retry", 7)

Game()