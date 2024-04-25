from pygame import *
from random import randint
 
# фонова музика
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')
 
# шрифти і написи
font.init()
font1 = font.Font(None, 80)

win = font1.render('YOU WIN!', True, (255, 255, 255))
lose = font1.render('YOU LOSE!', True, (180, 0, 0))

font2 = font.Font(None, 36)

# нам потрібні такі картинки:
img_back = "road.jpeg"  # фон гри
img_hero = "car.png"  # герой
img_bullet = "bullet.png" # куля
img_enemy1 = "car2.png"  # ворог
img_enemy2 = "car3.png" 
img_coin = "coin.png"

score = 0  # збито кораблів
goal = 10 # стільки кораблів потрібно збити для перемоги
#lost = 0  # пропущено кораблів
#max_lost = 3 # програли, якщо пропустили стільки

# клас-батько для інших спрайтів
class GameSprite(sprite.Sprite):
    # конструктор класу
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        # викликаємо конструктор класу (Sprite):
        sprite.Sprite.__init__(self)
 
        # кожен спрайт повинен зберігати властивість image - зображення
        self.image = transform.scale(
            image.load(player_image), (size_x, size_y))
        self.speed = player_speed
 
        # кожен спрайт повинен зберігати властивість rect - прямокутник, в який він вписаний
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
 
    # метод, що малює героя у вікні
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
 
# клас головного гравця
class Player(GameSprite):
    # метод для керування спрайтом стрілками клавіатури
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 130:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 180:
            self.rect.x += self.speed
        if keys[K_UP] and self.rect.y > 10:
            self.rect.y -= self.speed
        if keys[K_DOWN] and self.rect.y < win_height-100:
            self.rect.y += self.speed
    '''
    # метод "постріл" (використовуємо місце гравця, щоб створити там кулю)
    def fire(self):
        bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)
    '''
# клас спрайта-ворога
class Enemy(GameSprite):
    # рух ворога
    def update(self):
        self.rect.y += self.speed
        global lost
        # зникає, якщо дійде до краю екрана
        if self.rect.y > win_height:
            self.rect.x = randint(200, win_width - 200)
            self.rect.y = 0
            #lost = lost + 1

# клас спрайта-кулі   
class Bullet(GameSprite):
    # рух ворога
    def update(self):
        self.rect.y += self.speed
        # зникає, якщо дійде до краю екрана
        if self.rect.y > win_height:
            self.rect.x = randint(200, win_width - 200)
            self.rect.y = 0
            #self.kill()

# створюємо віконце
win_width = 700
win_height = 500
display.set_caption("Cars")
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load(img_back), (win_width, win_height))
 
# створюємо спрайти
car = Player(img_hero, 327, win_height - 100, 45, 90, 10)
 
monsters1 = sprite.Group()
for i in range(1, 2):
    monster = Enemy(img_enemy1, randint(
        200, win_width - 200), -40, 45, 90, randint(5, 10))
    monsters1.add(monster)

monsters2 = sprite.Group()
for i in range(1, 2):
    monster = Enemy(img_enemy2, randint(
        200, win_width - 200), -40, 45, 90, randint(5, 10))
    monsters2.add(monster)

coins = sprite.Group()
for i in range(1, 4):
    coin = Bullet(img_coin, randint(
        200, win_width - 200), -40, 45, 45, randint(1, 5))
    coins.add(coin)
#bullets = sprite.Group()

# змінна "гра закінчилася": як тільки вона стає True, в основному циклі перестають працювати спрайти
finish = False
# Основний цикл гри:
run = True  # прапорець скидається кнопкою закриття вікна
 
while run:
    # подія натискання на кнопку Закрити
    for e in event.get():
        if e.type == QUIT:
            run = False
        '''
        #подія натискання на пробіл - спрайт стріляє
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                fire_sound.play()
                #car.fire()
        '''
    # сама гра: дії спрайтів, перевірка правил гри, перемальовка
    if not finish:
        # оновлюємо фон
        window.blit(background, (0, 0))
        
        # пишемо текст на екрані
        text = font2.render("Score: " + str(score), 1, (0, 0, 0))
        window.blit(text, (10, 20))
        '''
        text_lose = font2.render("Пропущено: " + str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (10, 50))
        '''
        # рухи спрайтів
        car.update()
        monsters1.update()
        monsters2.update()
        coins.update()
        #bullets.update()

        # оновлюємо їх у новому місці при кожній ітерації циклу
        car.reset()
        monsters1.draw(window)
        monsters2.draw(window)
        coins.draw(window)
        #bullets.draw(window)
        '''
        # перевірка зіткнення кулі та монстрів (і монстр, і куля при зіткненні зникають)
        collides = sprite.groupcollide(coins, car, True, True)
        for c in collides:
            # цей цикл повториться стільки разів, скільки монстрів збито
            score = score + 1
            coin = Bullet(img_coin, randint(200, win_width - 200), -40, 45, 45, randint(1, 5))
            coins.add(coin)
        '''
        if sprite.spritecollide(car, coins, True):
            score = score + 1
            coin = Bullet(img_coin, randint(200, win_width - 200), -40, 45, 45, randint(1, 5))
            coins.add(coin)
            
        
        # можливий програш: пропустили занадто багато або герой зіткнувся з ворогом
        if sprite.spritecollide(car, monsters1, False): #or lost >= max_lost:
            finish = True # програли, ставимо тло і більше не керуємо спрайтами.
            window.blit(lose, (200, 200))
            
        if sprite.spritecollide(car, monsters2, False): #or lost >= max_lost:
            finish = True # програли, ставимо тло і більше не керуємо спрайтами.
            window.blit(lose, (200, 200))
            
        
        

        # перевірка виграшу: скільки очок набрали?
        if score >= goal:
            finish = True
            window.blit(win, (200, 200))

        display.update()
    # цикл спрацьовує кожні 0.05 секунд
    time.delay(50)