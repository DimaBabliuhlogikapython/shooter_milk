from pygame import *
from random import randint
import sys
from pygame.locals import *
display.init()
mixer.init()
mixer.music.load("barhat.ogg")
mixer.music.play()
fire_sound = mixer.Sound("sound_zavertin!.ogg")


img_back = "vanna.png"
img_hero = "ilya_mzlf.png"
img_enemy = "zavertin.png"

img_bullet = "milk_mzlf.png"




win_width = 700
win_height = 500
display.set_caption("fire with the milk")

#! win_width, win_height = display.get_desktop_sizes()[0][0], display.get_desktop_sizes()[0][1]
mw = display.set_mode((win_width, win_height))
background = transform.scale(image.load(img_back), (win_width, win_height))


class GameSprite(sprite.Sprite):
    def __init__(self, player_image,  player_x, player_y, size_x, size_y, player_speed):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(
            image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        mw.blit(self.image, (self.rect.x, self.rect.y))


class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 35:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width-80:
            self.rect.x += self.speed

    def fire(self):
        bullet = Bullet(img_bullet, self.rect.centerx,
                        self.rect.top, 15, 20, 15)
        bullets.add(bullet)

    def fire2(self):
        bullet = Bullet(img_bullet, self.rect.centerx,
                        self.rect.top, 15, 20, 15)
        bullets.add(bullet)


class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width-80)
            self.rect.y = 0
            lost += 5


class Enemy_2(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width-80)
            self.rect.y = 0
            lost += 1


class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()


class Bullet2(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()

lose2 = mixer.music.load("rugat_zavertina.ogg")
font.init()
text1 = font.Font(None, 80)
text2 = font.Font(None, 36)
win = text1.render("YOU WIN!", True, (0, 255, 0))
lose1 = text1.render("ENEMY WIN!", True, (180, 0, 0)) 
lose2 
mixer.music.load("rugat_zavertina.ogg")
mixer.music.play()



ship = Player(img_hero, 200, win_height-100, 80, 100, 10)


monsters = sprite.Group()
monsters2 = sprite.Group()
bullets = sprite.Group()
for i in range(1, 6):
    monster = Enemy(img_enemy, randint(80, win_width-80), 10,
                    80, 50, randint(1, 4))

    monsters.add(monster)
  
    
#monster = Enemy(img_enemy, randint(80, win_width-80), 0,80, 50, randint(1, 5))
lost = 3
score = 9999
max_lost = 500
goal = 99999

finish = False
run = True

while run:
    for e in event.get():
        if e.type == QUIT or key.get_pressed()[K_ESCAPE]:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                fire_sound.play()
                ship.fire()

    if not finish:
        mw.blit(background, (0, 0))
        ship.update()
        ship.reset()
        monsters.draw(mw)
        monsters.update()
        monsters2.draw(mw)
        monsters.update()
        
        bullets.draw(mw)
        bullets.update()

        collides = sprite.groupcollide(monsters, bullets, True, True)
        for collide in collides:
            score += 1
        
            monster = Enemy(img_enemy, randint(80, win_width-80), 10,
                            80, 50, randint(1, 5))
            monsters.add(monster)
         

        if sprite.spritecollide(ship, monsters, False) or lost >= max_lost:
            finish = True
            mw.blit(lose1, (200, 200))

        if score >= goal:
            finish = True
            mw.blit(win, (200, 200))

        #coutt_score = text2.render("Score")

    display.update()
    time.delay(50)
