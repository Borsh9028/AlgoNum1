from pygame import *
from random import *

font.init()
font = font.SysFont('Times New Roman', 50)

# Загрузка изображений
img_back = 'space.png'
img_hero = 'amogus.png'
img_enemy = 'amogus2.png'
img_bullet = 'bullet.png'
img_goal = 'black_hole.png'

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, width, height, player_speed):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(player_image), (width, height))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
        if keys[K_w] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_s] and self.rect.y < win_height - 80:
            self.rect.y += self.speed
    
    def fire(self, direction):
        bullet = Bullet(img_bullet, self.rect.centerx, self.rect.centery, 24, 25, 10, direction)
        bullets.add(bullet)

class Enemy(GameSprite):
    side = 'left'
    def update(self):
        if self.rect.x <= 470:
            self.side = 'right'
        if self.rect.x >= win_width - 85:
            self.side = 'left'
        if self.side == 'left':
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed

class Enemy2(GameSprite):
    side = 'up'
    def update(self):
        if self.rect.y <= 130:
            self.side = 'up'
        if self.rect.y >= win_height - 270:
            self.side = 'down'
        if self.side == 'down':
            self.rect.y -= self.speed
        else:
            self.rect.y += self.speed

class Wall(sprite.Sprite):
    def __init__(self, red, green, blue, wall_x, wall_y, wall_width, wall_height):
        super().__init__()
        self.red = red
        self.green = green
        self.blue = blue
        self.w = wall_width
        self.h = wall_height
        self.image = Surface((self.w, self.h))
        self.image.fill((red,green,blue))
        self.rect = self.image.get_rect()
        self.rect.x = wall_x
        self.rect.y = wall_y

class Bullet(GameSprite):
    def __init__(self, player_image, player_x, player_y, width, height, player_speed, direction):
        super().__init__(player_image, player_x, player_y, width, height, player_speed)
        self.direction = direction

    def update(self):
        if self.direction == 'up':
            self.rect.y -= self.speed
        elif self.direction == 'down':
            self.rect.y += self.speed
        elif self.direction == 'left':
            self.rect.x -= self.speed
        elif self.direction == 'right':
            self.rect.x += self.speed
        
        if self.rect.x > win_width or self.rect.x < 0 or self.rect.y > win_height or self.rect.y < 0:
            self.kill()

win_width = 700
win_height = 500
display.set_caption('2+2 = 3')
window = display.set_mode((win_width, win_height))
back = transform.scale(image.load(img_back), (win_width, win_height))

hero = Player(img_hero, 5, win_height - 80, 40, 40, 10)
monster = Enemy(img_enemy, win_width - 80, 280, 65, 65, 2)
final = GameSprite(img_goal, win_width - 120, win_height - 80, 65, 65, 0)
monster2 = Enemy2(img_enemy, win_width - 600, 60, 65, 65, 2)

walls = sprite.Group()
w1 = Wall(154, 205, 50, 100, 20 , 450, 10)
w2 = Wall(154, 205, 50, 100, 480, 350, 10)
w3 = Wall(154, 205, 50, 100, 20 , 10, 380)
w4 = Wall(154, 205, 50, 550, 100, 10, 400)
w5 = Wall(154, 205, 50, 250, 200, 10, 400)
w6 = Wall(154, 205, 50, 450, 10, 10, 400)

monsters = sprite.Group()
walls = sprite.Group()
bullets = sprite.Group()

monsters.add(monster)
monsters.add(monster2)

walls.add(w1, w2, w3, w4, w5, w6)

game = True
finish = False
clock = time.Clock()
FPS = 60
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        
        elif e.type == KEYDOWN:
            if e.key == K_RIGHT:
                hero.fire('right')  # Стрельба вправо при нажатии пробела
            elif e.key == K_UP:
                hero.fire('up')  # Стрельба вверх при нажатии стрелки вверх
            elif e.key == K_DOWN:
                hero.fire('down')  # Стрельба вниз при нажатии стрелки вниз
            elif e.key == K_LEFT:
                hero.fire('left')  # Стрельба влево при нажатии стрелки влево
    if finish != True:
        window.blit(back, (0, 0))
        walls.draw(window)
        hero.reset()
        final.reset()
        monsters.update()
        monsters.draw(window)
        hero.update()
        bullets.draw(window)
        bullets.update()
        sprite.groupcollide(bullets, walls, True, False)
        sprite.groupcollide(bullets, monsters, True, True)

        if sprite.spritecollide(hero, walls, False) or sprite.spritecollide(hero, monsters, False):
            finish = True
            window.blit(lose, (200, 200))
        
        if sprite.collide_rect(hero, final):
            finish = True
            window.blit(win, (200, 200))

    display.update()
    clock.tick(FPS)
