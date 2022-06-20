import random
import pygame as pg


# TODO: сделать кручение
#  сделать анимацию удаления
#  сделать склейки бобов
#  сделать анимацию соника


class Game:
    def __init__(self):
        pg.init()
        self.block = 60
        self.size = (self.block * 14, self.block * 16)
        self.screen = pg.display.set_mode(self.size)
        pg.display.set_caption('title')
        self.clock = pg.time.Clock()
        self.fps = 10
        self.next = pg.image.load('tempsnip.png')
        self.next = pg.transform.scale(self.next, (self.block * 5, self.block * 4))
        self.next_rect = self.next.get_rect()
        self.next_rect.x = self.block * 9
        self.next_rect.y = self.block * 2
        self.fon = pg.image.load('соник бум.PNG')
        self.fon = pg.transform.scale(self.fon, (self.block * 6, self.block * 12))
        self.fon_rect = self.fon.get_rect()
        self.fon_rect.x = self.block * 3
        self.fon_rect.y = self.block * 2
        self.lose = False
        self.all_sprites = pg.sprite.Group()
        self.fon2 = pg.image.load('Снимок (3).PNG')
        self.fon2 = pg.transform.scale(self.fon2, (self.block * 3, self.block * 16))
        self.fon2_rect = self.fon2.get_rect()
        self.fon2_rect.x = self.block * 0
        self.fon2_rect.y = self.block * 0
        self.fon3 = pg.image.load('фон 2.PNG')
        self.fon3 = pg.transform.scale(self.fon3, (self.block * 7, self.block * 2))
        self.fon3_rect = self.fon2.get_rect()
        self.fon3_rect.x = self.block * 3
        self.fon3_rect.y = self.block * 0
        self.fon6 = pg.image.load('нижний фон.png')
        self.fon6 = pg.transform.scale(self.fon6, (self.block * 6, self.block * 2))
        self.fon6_rect = self.fon6.get_rect()
        self.fon6_rect.x = self.block * 3
        self.fon6_rect.y = self.block * 14
        self.fon7 = pg.image.load('соня2.png')
        self.fon7 = pg.transform.scale(self.fon7, (self.block * 5, self.block * 10))
        self.fon7_rect = self.fon7.get_rect()
        self.fon7_rect.x = self.block * 9
        self.fon7_rect.y = self.block * 6
        self.fon5 = pg.image.load('вверх.PNG')
        self.fon5 = pg.transform.scale(self.fon5, (self.block * 4, self.block * 2))
        self.fon5_rect = self.fon5.get_rect()
        self.fon5_rect.x = self.block * 10
        self.fon5_rect.y = self.block * 0

        self.matrix = []
        for i in range(14):
            self.matrix.append([0, 0, 0, 0, 0, 0])
        self.create_next_beans()
        self.create_beans()
        self.create_next_beans()
        self.run()

    def run(self):
        while True:
            self.event()
            if self.lose == False:
                self.update()
            self.draw()
            self.clock.tick(self.fps)

    def event(self):
        self.events = pg.event.get()
        for event in self.events:
            if event.type == pg.QUIT:
                pg.quit()

    def search_same_color_beans(self, x, y):

        add = 1
        while y != 0 and self.matrix[y - add][x] != 0 and \
                self.matrix[y - add][x].type == self.matrix[y][x].type:
            if self.matrix[y - add][x] not in self.same_color_beans:
                self.same_color_beans.append(self.matrix[y - add][x])
                self.search_same_color_beans(x, y - add)
            add += 1
        add = 1
        while x != len(self.matrix[0]) - 1 and x + add != len(self.matrix[0]) and \
                self.matrix[y][x + add] != 0 and self.matrix[y][x + add].type == self.matrix[y][x].type:
            if self.matrix[y][x + add] not in self.same_color_beans:
                self.same_color_beans.append(self.matrix[y][x + add])
                self.search_same_color_beans(x + add, y)
            add += 1
        add = 1
        while x != 0 and x - add < 0 and self.matrix[y][x - add] != 0 and \
                self.matrix[y][x - add].type == self.matrix[y][x].type:
            if self.matrix[y][x - add] not in self.same_color_beans:
                self.same_color_beans.append(self.matrix[y][x - add])
                self.search_same_color_beans(x - add, y)
            add += 1
        add = 1
        while y != len(self.matrix) - 1 and y + add != len(self.matrix) and \
                self.matrix[y + add][x] != 0 and self.matrix[y + add][x].type == self.matrix[y][x].type:
            if self.matrix[y + add][x] not in self.same_color_beans:
                self.same_color_beans.append(self.matrix[y + add][x])
                self.search_same_color_beans(x, y + add)
            add += 1

    def update(self):
        self.all_sprites.update()
        if self.all_sprites.sprites()[-1].move == False and self.all_sprites.sprites()[-2].move == False:
            self.create_beans()
            self.create_next_beans()
        for y in range(len(self.matrix)):
            for x in range(len(self.matrix[0])):
                if self.matrix[y][x] != 0:
                    self.same_color_beans = []
                    self.search_same_color_beans(x, y)
                    self.same_color_beans.append(self.matrix[y][x])
                    self.same_color_beans = list(set(self.same_color_beans))
                    # print(len(self.same_color_beans) + 1)
                    if len(self.same_color_beans) >= 4:
                        for y1 in range(len(self.matrix)):
                            for x1 in range(len(self.matrix[0])):
                                if self.matrix[y1][x1] in self.same_color_beans:
                                    self.all_sprites.remove(self.matrix[y1][x1])
                                    self.matrix[y1][x1] = 0

    def draw(self):
        if self.lose == False:
            self.screen.fill(pg.Color('Gray'))
            self.screen.blit(self.fon, self.fon_rect)
            self.screen.blit(self.next, self.next_rect)
            self.screen.blit(self.fon2, self.fon2_rect)
            self.screen.blit(self.fon6, self.fon6_rect)
            self.screen.blit(self.fon7, self.fon7_rect)
            self.screen.blit(self.fon5, self.fon5_rect)
            self.all_sprites.draw(self.screen)
            self.screen.blit(self.next_beans[0].image, (self.block * 10, self.block * 3))
            self.screen.blit(self.next_beans[1].image, (self.block * 10, self.block * 4))

            self.screen.blit(self.fon3, self.fon3_rect)
        pg.display.flip()

    def create_beans(self):
        # bean1 = Bean(self, pos=1)
        # bean2 = Bean(self, pos=2)
        self.all_sprites.add(self.next_beans[1])
        self.all_sprites.add(self.next_beans[0])
        self.matrix[0][2] = self.next_beans[0]
        self.matrix[1][2] = self.next_beans[1]

    def create_next_beans(self):
        self.next_beans = []
        bean1 = Bean(self, pos=1)
        bean2 = Bean(self, pos=2)
        self.next_beans.append(bean1)
        self.next_beans.append(bean2)


class Bean(pg.sprite.Sprite):
    def __init__(self, game, pos, ):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.type = random.randint(0, 4)
        self.sprites_sheet = pg.image.load('95507.png')
        self.idle = []
        self.pos = pos
        self.move = True
        self.bean_spin = 'up'

        self.load_sprites(self.type)

        self.image = self.idle[0]
        self.rect = self.image.get_rect()
        if pos == 1:
            self.matrix_pos = [0, 2]
            self.rect.y = 0
        else:
            self.rect.y = self.game.block
            self.matrix_pos = [1, 2]
        self.rect.x = self.game.block * 5
        self.last_animation_update = pg.time.get_ticks()
        self.last_update = pg.time.get_ticks()
        self.frame_rate = 100
        self.animation_pause = 4000
        self.current_frame = 0
        self.last_move = pg.time.get_ticks()
        self.move_frame_rave = 230

    def load_sprites(self, y):
        for i in range(6):
            if y == 4:
                self.sprite = self.sprites_sheet.subsurface(12 + 16 * i + i, 11 + y * 2 * 17 + 17, 16, 16)
            else:
                self.sprite = self.sprites_sheet.subsurface(12 + 16 * i + i, 11 + y * 2 * 17, 16, 16)
            self.sprite = pg.transform.scale(self.sprite, (self.game.block, self.game.block))
            self.sprite.set_colorkey((255, 0, 255))
            self.idle.append(self.sprite)

    def update(self):
        now = pg.time.get_ticks()
        if self.matrix_pos[0] + 1 != len(self.game.matrix):
            if self.game.matrix[self.matrix_pos[0] + 1][self.matrix_pos[1]] == 0:
                self.move = True
                if now - self.last_move > self.move_frame_rave:
                    self.rect.y += self.game.block // 2
                    self.game.matrix[self.matrix_pos[0]][self.matrix_pos[1]] = 0
                    if self.rect.y % self.game.block == 0:
                        self.matrix_pos = [self.matrix_pos[0] + 1, self.matrix_pos[1]]
                        self.game.matrix[self.matrix_pos[0]][self.matrix_pos[1]] = self
                    self.last_move = pg.time.get_ticks()
            else:
                self.move = False
        else:
            self.move = False
        if self.move:
            for event in self.game.events:
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_a:
                        if self.matrix_pos[1] != 0:
                            if self.game.matrix[self.matrix_pos[0]][self.matrix_pos[1] - 1] == 0:
                                self.rect.x -= self.game.block
                                self.game.matrix[self.matrix_pos[0]][self.matrix_pos[1]] = 0
                                self.matrix_pos = [self.matrix_pos[0], self.matrix_pos[1] - 1]
                                self.game.matrix[self.matrix_pos[0]][self.matrix_pos[1]] = self
                    if event.key == pg.K_d:
                        if self.matrix_pos[1] != len(self.game.matrix[0]) - 1:
                            if self.game.matrix[self.matrix_pos[0]][self.matrix_pos[1] + 1] == 0:
                                self.rect.x += self.game.block
                                self.game.matrix[self.matrix_pos[0]][self.matrix_pos[1]] = 0
                                self.matrix_pos = [self.matrix_pos[0], self.matrix_pos[1] + 1]
                                self.game.matrix[self.matrix_pos[0]][self.matrix_pos[1]] = self
                    if event.key == pg.K_SPACE:
                        self.spin()
        if now - self.last_animation_update > self.animation_pause:
            if now - self.last_update > self.frame_rate:
                self.current_frame += 1
                if self.current_frame == len(self.idle):
                    self.last_animation_update = pg.time.get_ticks()
                    self.current_frame = 0
                self.image = self.idle[self.current_frame]

    def spin(self):
        #print(self.game.matrix)
        if self.bean_spin == 'up':
            if self.pos == 1:
                self.game.matrix[self.matrix_pos[0]][self.matrix_pos[1]] = 0
                self.matrix_pos = [self.matrix_pos[0] + 1, self.matrix_pos[1] + 1]
                self.game.matrix[self.matrix_pos[0]][self.matrix_pos[1]] = self
                self.rect.y += self.game.block
                self.rect.x += self.game.block
                self.bean_spin = 'right'
        elif self.bean_spin == 'right':
            if self.pos == 1:
                self.game.matrix[self.matrix_pos[0]][self.matrix_pos[1]] = 0
                self.matrix_pos = [self.matrix_pos[0] + 1, self.matrix_pos[1] - 1]
                self.game.matrix[self.matrix_pos[0]][self.matrix_pos[1]] = self
                self.rect.y += self.game.block
                self.rect.x -= self.game.block
                self.bean_spin = 'down'
        elif self.bean_spin == 'down':
            if self.pos == 1:
                self.game.matrix[self.matrix_pos[0]][self.matrix_pos[1]] = 0
                self.matrix_pos = [self.matrix_pos[0] - 1, self.matrix_pos[1] - 1]
                self.game.matrix[self.matrix_pos[0]][self.matrix_pos[1]] = self
                self.rect.y -= self.game.block
                self.rect.x -= self.game.block
                self.bean_spin = 'left'
        elif self.bean_spin == 'left':
            if self.pos == 1:
                self.game.matrix[self.matrix_pos[0]][self.matrix_pos[1]] = 0
                self.matrix_pos = [self.matrix_pos[0] - 1, self.matrix_pos[1] + 1]
                self.game.matrix[self.matrix_pos[0]][self.matrix_pos[1]] = self
                self.rect.y -= self.game.block
                self.rect.x += self.game.block
                self.bean_spin = 'up'




class Sonic(pg.sprite.Sprite):
    def __init__(self, game, pos):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.type = random.randint(0, 4)
        self.sprites_sheet = pg.image.load('95304.png')
        self.idle = []


g = Game()
