# Разработай свою игру в этом файле!
from pygame import *
font.init()
mw = display.set_mode((900, 600))
BG = transform.scale(image.load('12345.jpg'), (900, 600))
display.set_caption('моя игра')
win_txt = font.SysFont('Verdana', 50).render('ты прошел', True,(220, 40, 50))
lose_txt = font.SysFont('Verdana', 50).render('Ты проиграл', True,(50, 230, 50))
clock = time.Clock()
surf = Surface((895, 595))
class GameSprite(sprite.Sprite):
    def __init__(self, x, y, w, h, filename):
        super().__init__()
        self.image = transform.scale(image.load(filename), (w, h))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def reset(self):
        mw.blit(self.image,(self.rect.x, self.rect.y))
        self.rect.clamp_ip(surf.get_rect())
class Player(GameSprite):
    def __init__(self, x, y, w, h, filename, speed=0):
        super().__init__(x, y, w, h, filename)
        self.speed_x = speed
        self.speed_y = speed
    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        walls_touch = sprite.spritecollide(self, walls, False)
        if self.speed_x > 0:
            for wall in walls_touch:
                self.rect.right = min(self.rect.right, wall.rect.left)
        elif self.speed_x < 0:
            for wall in walls_touch:
                self.rect.left = max(self.rect.left, wall.rect.right)
        if self.speed_y < 0:
            for wall in walls_touch:
                self.rect.top = max(self.rect.top, wall.rect.bottom)
        elif self.speed_y > 0:
            for wall in walls_touch:
                self.rect.bottom = min(self.rect.bottom, wall.rect.top)
        if self.speed_x > 0:
            for wall in walls_touch:
                self.rect.right = min(self.rect.right, wall.rect.left)
    def fire(self):
        bullets.add(Bullet(self.rect.right, self.rect.centery, 100, 100, 'bullet.png'))
class Bullet(GameSprite):
    def __init__(self, x, y, w, h, filename, speed=10):
        super().__init__(x,  y,  w, h, filename)
        self.speed_x = speed 
    def update(self):
        self.rect.x += self.speed_x
        if self.rect.x >= 900:
            self.kill()
class Enemy(GameSprite):
    def __init__(self, x, y, w, h, filename):
        super().__init__(x, y,  w, h, filename)
        self.direction = 'left'
    def update(self):
        if self.rect.x <= 0:
            self.direction = 'right'
        elif self.rect.x >= 430:
            self.direction = 'left'
        if self.direction == 'left':
            self.rect.x -=3
        else:
            self.rect.x += 3
bullets = sprite.Group()
enemies = sprite.Group()
walls = sprite.Group()
walls.add(GameSprite(400, 0, 30, 200, 'p.png'))
walls.add(GameSprite(400, 200, 100, 30, 'p.png'))
walls.add(GameSprite(500, 200, 30, 200, 'p.png'))
player = Player(400, 10, 100, 60, 'p.png')
goal = GameSprite(850, 550, 50, 50, 'p.png')
enemies.add(Enemy(300, 240, 70, 70, 'p.png')) 
run = True
finish = False
while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        if e.type == KEYDOWN:
            if e.key == K_s:
                player.speed_y = 5
            elif e.key == K_a:
                player.speed_x -= 5
            if e.key == K_d:
                player.speed_x = 5
            elif e.key == K_w:
                player.speed_y = -5
            elif e.key == K_SPACE:
                player.fire()
        if e.type == KEYUP:
            if e.key == K_s:
                player.speed_y = 0
            elif e.key == K_a:
                player.speed_x = 0
            if e.key == K_w:
                player.speed_y = 0
            elif e.key == K_d:
                player.speed_x = 0
    if not finish:
        mw.blit(BG, (0, 0))
        walls.draw(mw)
        goal.reset()
        player.reset()
        player.update()
        enemies.draw(mw)
        enemies.update()
        bullets.draw(mw)
        bullets.update()
        if sprite.collide_rect(player, goal):
            mw.blit(win_txt, (200, 250))
            finish = True
        sprite.groupcollide(bullets, walls, True, False)
        sprite.groupcollide(bullets, enemies, True, True)
        if sprite.spritecollide(player, enemies, False):
            mw.blit(lose_txt, (200, 250))
            finish = True
    display.update()
    clock.tick(60)
