import random
from turtle import *

# CONST
ball_radius = 10
player_width = 20
player_height = 100

# GAME_SCORE
speed_g = 100
speed_b = 100
speed_p = 100

# COLOR_CONST
color_white = "white"
color_cyan = "cyan"
color_black = "black"
color_yellow = "yellow"
color_green = "green"


class GameObject:  # Ну такой общий класс, что бы было
    def __init__(self, start_point: tuple[int, int], end_point: tuple[int, int], velocity: tuple[int, int],
                 color=color_cyan):
        self.rect = [start_point, end_point]  # начальная точка "ректа"
        self.velocity = velocity  # вектор скорости изменения координат объекта
        self.update_()  # начальное вычисление центра
        self.color = color

    def update_(self) -> None:  # обновляем позицию по скорости
        self.rect[0] = (self.rect[0][0] + self.velocity[0] * (speed_g / 100),
                        self.rect[0][1] + self.velocity[1] * (speed_g / 100))
        self.rect[1] = (self.rect[1][0] + self.velocity[0] * (speed_g / 100),
                        self.rect[1][1] + self.velocity[1] * (speed_g / 100))
        self.center = (self.rect[0][0] + (self.rect[1][0] - self.rect[0][0]) / 2,
                       self.rect[0][1] + (self.rect[1][1] - self.rect[0][1]) / 2)

    def set_velocity(self, new_velocity: tuple[int, int]) -> None:  # установить скорость
        self.velocity = new_velocity

    def update_velocity(self, addition: tuple[int, int]) -> None:  # изменяем скорость
        self.velocity = (self.velocity[0] + addition[0], self.velocity[1] + addition[1])


class BallObject(GameObject):  # шарик я как и ты был на цепи
    def __init__(self, start_point: tuple[int, int], end_point: tuple[int, int], velocity: tuple[int, int]):
        super().__init__(start_point, end_point, velocity)
        self.radius = ball_radius

    def draw(self, turtle) -> None:
        turtle.penup()
        turtle.goto(self.center)
        turtle.pendown()
        turtle.dot(self.radius)


class Players(GameObject):  # игроки
    def update_(self) -> None:
        super().update_()
        self.velocity = 0, self.velocity[1]

    def draw(self, turtle):
        turtle.penup()
        turtle.goto(self.rect[0][0], self.rect[0][1])
        turtle.pendown()
        turtle.color(self.color)
        turtle.goto(self.rect[1][0], self.rect[0][1])
        turtle.goto(self.rect[1][0], self.rect[1][1])
        turtle.goto(self.rect[0][0], self.rect[1][1])
        turtle.goto(self.rect[0][0], self.rect[0][1])

    def set_velocity_up(self):
        print(1)
        self.set_velocity((0, 1))

    def set_velocity_down(self):
        print(2)
        self.set_velocity((0, -1))


class UI_Object:
    def __init__(self):
        pass

    def update_(self):
        pass

    def draw(self, turtle):
        turtle.color(color_white)
        turtle.penup()  # рисуем границы поля


class Border(UI_Object):
    def __init__(self, border):
        super(Border, self).__init__()
        self.coord = border

    def draw(self, turtle):
        super(Border, self).draw(turtle)
        turtle.goto(self.coord[0])
        turtle.pendown()
        turtle.goto(self.coord[1])
        turtle.goto(self.coord[2])
        turtle.goto(self.coord[3])
        turtle.goto(self.coord[0])
        turtle.color(color_cyan)


class Score(UI_Object):
    def __init__(self, score, sposition=(0, 350)):
        super(Score, self).__init__()
        self.score = score
        self.sposition = sposition

    def draw(self, turtle):
        super(Score, self).draw(turtle)
        score_p1 = self.score[0]
        score_p2 = self.score[1]
        turtle.goto(self.sposition)

        turtle.setheading(180)
        turtle.up()
        turtle.forward(10)
        turtle.color(color_yellow)
        for i in range(score_p1):
            turtle.down()
            for j in range(2):
                turtle.forward(10)
                turtle.right(90)
                turtle.forward(50)
                turtle.right(90)
            turtle.up()
            turtle.forward(20)

        turtle.up()
        turtle.goto(self.sposition)
        turtle.setheading(0)
        turtle.color(color_green)
        turtle.forward(10)
        for i in range(score_p2):
            turtle.down()
            for j in range(2):
                turtle.forward(10)
                turtle.right(-90)
                turtle.forward(50)
                turtle.right(-90)
            turtle.up()
            turtle.forward(20)

        turtle.color(color_cyan)


class Game(object):
    def __init__(self):
        self.player1 = Players((-330, 0), (player_width - 330, player_height), (0, 0), color=color_yellow)
        self.player2 = Players((330, 0), (player_width + 330, player_height), (0, 2), color=color_green)
        self.border = Border(((-400, 300), (400, 300), (400, -300), (-400, -300)))
        self.score = Score((0, 0))
        self.screen = Screen()
        self.turtle = Turtle()
        self.window = True

    def start_game(self):
        self.screen.bgcolor(color_black)
        self.screen.tracer(0)  # отключить отрисовку
        self.turtle.speed(0)
        self.turtle.hideturtle()  # отключить отрисовку черепахи
        self.update_objects()
        self.screen.listen()

    def update_objects(self):
        self.objects = (self.ball, self.player2, self.player1, self.border, self.score)

    def spawn_new_ball(self):
        vx = random.choice([x for x in range(-2, 3) if x != 0])  # выбираем случайное значение vx, исключая 0
        vy = random.random() * random.randint(-2, 2)
        vx, vy = (-0.675, 1)
        self.ball = BallObject((ball_radius * -1, 0), (ball_radius, ball_radius * 2), (vx, vy))
        self.update_objects()

    def run(self):
        while self.window:
            if max(self.score.score) >= 9:
                self.turtle.clear()
                self.turtle.up()
                self.turtle.goto((0, 0))
                self.turtle.down()
                if self.score.score[0] == 9:
                    self.turtle.write("win player 2", align="center", font=("Arial", 60, "normal"))
                else:
                    self.turtle.write("win player 1", align="center", font=("Arial", 60, "normal"))
            else:
                self.turtle.clear()  # отрисовка экрана

                self.check_collision_ball_and_border()
                # self.test_draw()
                self.check_collision_player_1_and_ball()
                self.check_collision_player_and_border(self.player1)
                self.check_collision_player_and_border(self.player2)

                self.screen.onkey(self.player1.set_velocity_up, "Up")
                self.screen.onkey(self.player1.set_velocity_down, "Down")

                for obj in self.objects:
                    obj.update_()
                    obj.draw(self.turtle)

                self.screen.update()  # отрисовка экрана

    def check_collision_player_1_and_ball(self):
        if (self.player1.rect[1][0] + ball_radius / 2 >= self.ball.center[0]) and (
                self.player1.rect[0][1] <= self.ball.center[1]) and (
                self.ball.center[1] <= self.player1.rect[1][1]):
            self.ball.set_velocity((-self.ball.velocity[0], self.ball.velocity[1]))

        if (self.player1.rect[0][1] - ball_radius / 2 <= self.ball.center[1] <= self.player1.rect[1][
            1] + ball_radius / 2) and (
                # y0 <= yb <= y1
                self.player1.rect[0][0] <= self.ball.center[0] <= self.player1.rect[1][0]):  # x0 <= xb <= x1
            self.ball.set_velocity((self.ball.velocity[0], -self.ball.velocity[1]))

    def check_collision_ball_and_border(self):
        hit_left = self.check_horizontal_left_collision()
        hit_right = self.check_horizontal_right_collision()
        hit_top_or_bottom = self.check_vertical_collision_ball_and_border()

        if hit_left or hit_right or hit_top_or_bottom:
            self.handle_collision(hit_left, hit_right, hit_top_or_bottom)

    def check_collision_player_and_border(self, player_):
        if (self.border.coord[2][1] >= player_.rect[0][1] or
         player_.rect[1][1] >= self.border.coord[0][1]):
            player_.set_velocity((player_.velocity[0], -player_.velocity[1]))



    def test_draw(self):
        self.turtle.color(color_white)
        self.turtle.up()
        self.turtle.goto(self.player1.rect[0])
        self.turtle.down()
        self.turtle.dot(5)
        self.turtle.up()
        self.turtle.goto((20, 20))
        self.turtle.down()
        self.turtle.dot(5)
        self.turtle.up()
        self.turtle.color(color_cyan)
        self.turtle.goto((100, 20))
        self.turtle.down()
        self.turtle.dot(5)
        self.turtle.up()
        self.turtle.color(color_cyan)
        self.turtle.goto(self.player1.rect[1])
        self.turtle.down()
        self.turtle.dot(5)

    def check_horizontal_left_collision(self):
        return self.border.coord[0][0] + ball_radius / 2 >= self.ball.center[0]

    def check_horizontal_right_collision(self):
        return self.ball.center[0] >= self.border.coord[1][0] - ball_radius / 2

    def check_vertical_collision_ball_and_border(self):
        return (self.border.coord[2][1] + ball_radius / 2 >= self.ball.center[1] or
                self.ball.center[1] >= self.border.coord[0][1] - ball_radius / 2)

    def handle_collision(self, hit_left, hit_right, hit_vertical):
        if hit_left or hit_right:
            self.ball.set_velocity((-self.ball.velocity[0], self.ball.velocity[1]))
            if hit_left:
                self.score.score = self.score.score[0] + 1, self.score.score[1]
                self.spawn_new_ball()
            if hit_right:
                self.score.score = self.score.score[0], self.score.score[1] + 1
                self.spawn_new_ball()
        if hit_vertical:
            self.ball.set_velocity((self.ball.velocity[0], -self.ball.velocity[1]))

    def event_handler(self):
        pass

    def move_player(self):
        pass

    def update(self):
        pass

    def game_over(self):
        pass


if __name__ == '__main__':
    game = Game()
    game.spawn_new_ball()
    game.start_game()
    game.run()
