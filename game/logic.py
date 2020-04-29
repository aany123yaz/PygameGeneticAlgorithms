import time
import random
import pygame


class Ball:

    def __init__(self, initial_position=None, velocity=1):
        if initial_position is None:
            initial_position = [-1, -1]

        self.rect = pygame.Rect(initial_position[0], initial_position[1], 30, 30)
        self.initial_position = initial_position
        self.position = initial_position
        self.movement = [0, 0]
        self.velocity = velocity
        self.spawned = False

    def Reset(self):
        self.spawned = False
        self.position = self.initial_position
        self.rect.x = self.initial_position[0]
        self.rect.y = self.initial_position[1]
        self.movement = [0, 0]

    def IsSpawned(self):
        return self.spawned

    def Spawn(self):
        self.spawned = True

    def GetPosition(self):
        return self.position

    def SetPosition(self, x, y):
        self.position = [x, y]
        self.rect.x = x
        self.rect.y = y

    def SetMovement(self, movement_vector):
        self.movement = movement_vector

    def SetMovementDirectionX(self, direction):
        self.movement[0] = direction

    def SetMovementDirectionY(self, direction):
        self.movement[1] = direction

    def Move(self):
        self.position[0] += self.movement[0] * self.velocity
        self.position[1] += self.movement[1] * self.velocity
        self.rect.x += self.movement[0] * self.velocity
        self.rect.y += self.movement[1] * self.velocity

    def Collide(self, obj):
        return self.rect.colliderect(obj.rect)


class Board:

    LEFT = 0
    RIGHT = 1
    NULL = 2

    def __init__(self, size=(500, 500), id=0, number_of_enemies=5, spawn_rate=2, spawned_enemies=1):
        self.size = size
        self.balls = [Ball() for i in range(number_of_enemies)]
        self.player = Ball([int(size[0] / 2), int(size[1] - 50)], velocity=5)
        self.number_of_enemies = number_of_enemies
        self.spawned_enemies = spawned_enemies
        self.spawn_rate = spawn_rate
        self.game_over = False
        self.start_time = time.time()
        self.spawn_time = time.time()
        self.score = 0
        self.id = id

    def Reset(self):
        for i in range(len(self.balls)):
            self.balls[i].Reset()

        self.player.SetPosition(int(self.size[0] / 2), int(self.size[1] - 50))
        self.spawned_enemies = 1
        self.game_over = False
        self.start_time = time.time()
        self.spawn_time = time.time()
        self.score = 0

    def IsGameOver(self):
        return self.game_over

    def GetScore(self):
        return self.score

    def GetID(self):
        return self.id

    def Tick(self):

        for i in range(self.spawned_enemies):
            ball = self.balls[i]
            position = ball.GetPosition()

            if not ball.IsSpawned():
                random_x = random.randrange(100, self.size[0] - 100)

                ball.SetPosition(random_x, 0)
                ball.SetMovementDirectionY(1)
                ball.Spawn()

            elif position[1] >= self.size[1] + 300:
                self.game_over = True

            ball.Move()

            if self.player.Collide(ball):
                random_x = random.randrange(100, self.size[0] - 100)
                ball.SetPosition(random_x, 0)
                self.score += 1

    def MovePlayer(self, direction):
        position = self.player.GetPosition()

        if direction == self.LEFT:
            self.player.SetMovementDirectionX(-1)

        elif direction == self.RIGHT:
            self.player.SetMovementDirectionX(1)

        else:
            self.player.SetMovement([0, 0])

        if position[0] - 100 <= 0 or position[0] + 100 >= self.size[0]:
            # self.player.SetMovementDirectionX(0)
            self.game_over = True

        self.player.Move()

    def Get1DPositions(self):
        player_position = self.player.GetPosition()

        enemy_positions = []

        for ball in self.balls:
            enemy_positions.append(ball.GetPosition()[0])

        positions = [player_position[0], sorted(enemy_positions)[-1]]

        return positions

    def GetEnemiesPositions(self):
        return [ball.GetPosition() for ball in self.balls]

    def GetPlayerPosition(self):
        return self.player.GetPosition()


def CreateBoards(pop_size=5, board_size=(500, 500)):
    boards = []

    for i in range(pop_size):
        boards.append(Board(size=board_size, id=i))

    return boards


def ResetBoards(boards):
    for i in range(len(boards)):
        boards[i].Reset()

    return boards
