# Void Kitten - A LetThereBeLemons creation
# Liscenced under DONT STEAL MY CODE YOU ASSHOLE (DSMCYA)

#TODO: Make enemies into a list, and add one every 5000 or so ticks.
#TODO: Implement main menu / pause menu

#! === Import & Init === !#
import pygame, random, time
pygame.init()

#! === Varables === !#
debug = 0
exitc = 'error'
boost_tick = -501
boost_length = 0
slowdown_tick = -1001
boost_readymessageon = 1
slowdown_readymessageon = 1
rendertext = ['Ready!','Set!','Go!']
fullscreen = 0
state = 'game'

#! === User Setup === !#
print('\nUse WASD to move, ESC to quit, E to boost, Q to slow time, R to randomly teleport and F to print the current tick.')
print('Hint: For fullscreen, don\'t enter anything.')
scrw = input('Enter width: ')
scrh = input('Enter height: ')
print('Add modifiers here, seperated by spaces, or press enter to continue.')
print(' superfast (sf): runs at 1000 tps instead of 100.\n superslow (ss): runs at 10 tps instead of 100.\n debug (db): prints debug info, may cause lag.\n bigglitches (bg): makes glitches 5x bigger.\n massiveglitches (mg): makes glitches 10x bigger.\n extraglitch (eg): adds an extra glitch at the start.\n tinyglitches (tg): makes glitches 10x smaller.\n noplayer (np): removes the player, for some reason.\n randomteleport (rt): randomly teleports you.')
mods = input('[sf, ss, db, bg, mg, tg, eg, np, rt]: ')
mods = mods.split()
if 'sf' in mods:
    print('You have about 1000 ticks (1 second) until the glitch starts to spread. Good luck.')
else:
    print('You have about 1000 ticks (10 seconds) until the glitch starts to spread. Good luck.')
if 'db' in mods:
    debug = 1

#! === Screen Setup === !#
if scrw == '':
    scrw = pygame.display.Info().current_w
    fullscreen = 1
else:
    scrw = int(scrw)
    fullscreen = 0

if scrh == '':
    scrh = pygame.display.Info().current_h
    fullscreen = 1
else:
    scrh = int(scrh)
    fullscreen = 0

if fullscreen:
    window = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
else:
    window = pygame.display.set_mode((scrw, scrh))

pygame.display.set_caption('Glitch Kitten')

#! === Classes === !#
class controllable_entity(pygame.sprite.Sprite):
    def __init__(self):
        super(controllable_entity, self).__init__()
        self.size = (50, 50)
        self.image = 'playercat_50x50.jpg'
        self.speed = 1
        self.surf = pygame.Surface(self.size)
        self.surf.blit(pygame.image.load(self.image), (0, 0))
        self.rect = self.surf.get_rect()

    def update(self, key, boost):
        if boost:
            if key[pygame.K_w]:
                self.rect.move_ip(0, -self.speed * 5)
            if key[pygame.K_s]:
                self.rect.move_ip(0, self.speed * 5)
            if key[pygame.K_a]:
                self.rect.move_ip(-self.speed * 5, 0)
            if key[pygame.K_d]:
                self.rect.move_ip(self.speed * 5, 0)
        else:
            if key[pygame.K_w]:
                self.rect.move_ip(0, -self.speed)
            if key[pygame.K_s]:
                self.rect.move_ip(0, self.speed)
            if key[pygame.K_a]:
                self.rect.move_ip(-self.speed, 0)
            if key[pygame.K_d]:
                self.rect.move_ip(self.speed, 0)
            
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > scrw:
            self.rect.right = scrw
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > scrh:
            self.rect.bottom = scrh

class evil_entity(pygame.sprite.Sprite):
    def __init__(self):
        super(evil_entity, self).__init__()
        if 'mg' in mods:
            self.size = (100, 100)
        elif 'bg' in mods:
            self.size = (50, 50)
        elif 'tg' in mods:
            self.size = (1, 1)
        else:
            self.size = (10, 10)
        self.speed = 1
        self.surf = pygame.Surface(self.size)
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect()
        if 'mg' in mods:
            self.rect.center = (scrw - 100, scrh - 100)
        elif 'bg' in mods:
            self.rect.center = (scrw - 50, scrh - 50)
        elif 'tg' in mods:
            self.rect.center = (scrw - 1, scrh - 1)
        else:
            self.rect.center = (scrw - 10, scrh - 10)

    def update(self, player):
        if player:
            if self.rect.colliderect(player.rect):
                global game, exitc
                game = 0
                exitc = 'enemy_collision'
            
            else:
                self.rect.move_ip(random.randint(-self.speed, self.speed), random.randint(-self.speed, self.speed))
            
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > scrw:
            self.rect.right = scrw
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > scrh:
            self.rect.bottom = scrh
            
        self.surf.fill((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
        
#! === Text Setup === !#
def alert(text):
    global rendertext
    if len(rendertext) > 2:
        rendertext.pop(0)
    rendertext.append(text)
    

#! === Game setup === !#
if not 'np' in mods:
    player = controllable_entity()
else:
    player = 0
enemy = evil_entity()
if 'eg' in mods:
    enemy3 = evil_entity()

game = 1
tick = 0

font = pygame.font.Font('freesansbold.ttf', 32)

if debug:
    print('GAME START TICK: ' + str(tick))

#! === Main Loop === !#
while game:
    if state == 'menu':
        None
    elif state == 'game':
        tick += 1
        stick = str(tick) + ': '

        #! === Colour === !#
        if (enemy.speed / 2) > 255:
            redcolor = 255
        else:
            redcolor = enemy.speed / 2
        if not 'np' in mods:
            if player.speed > 255:
                bluecolor = 255
            else:
                bluecolor = player.speed
        else:
            bluecolor = 0
        window.fill((redcolor, 0, bluecolor))

        #! === Text === !#
        text1 = font.render(rendertext[0], True, (255, 255, 255))
        text1rect = text1.get_rect()
        text1rect.center = (int(scrw / 2), int(scrh / 2) - 32)
        window.blit(text1, text1rect)

        text2 = font.render(rendertext[1], True, (255, 255, 255))
        text2rect = text2.get_rect()
        text2rect.center = (int(scrw / 2), int(scrh / 2))
        window.blit(text2, text2rect)

        text3 = font.render(rendertext[2], True, (255, 255, 255))
        text3rect = text3.get_rect()
        text3rect.center = (int(scrw / 2), int(scrh / 2) + 32)
        window.blit(text3, text3rect)

        #! === Blit === !#
        if not 'np' in mods:
            window.blit(player.surf, player.rect)
        window.blit(enemy.surf, enemy.rect)
        if tick > 5000:
            window.blit(enemy2.surf, enemy2.rect)
        if tick > 10000:
            window.blit(enemy4.surf, enemy4.rect)
        if 'eg' in mods:
            window.blit(enemy3.surf, enemy3.rect)

        #! === Powerups === !#
        if boost_tick + boost_length + 1000 < tick and boost_readymessageon:
            alert(stick + 'BOOST READY')
            boost_readymessageon = 0

        if slowdown_tick + 2000 < tick and slowdown_readymessageon:
            alert(stick + 'SLOWDOWN READY')
            slowdown_readymessageon = 0

        #! === Input === !#
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game = 0
                exitc = 'user_quit'
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game = 0
                    exitc = 'user_quit'
                elif event.key == pygame.K_e:
                    if boost_tick + boost_length + 1000 < tick:
                        boost_tick = tick
                        boost_length = tick / 10
                        alert(stick + 'BOOST!')
                        boost_readymessageon = 1
                    else:
                        alert(stick + 'BOOST NOT READY')
                elif event.key == pygame.K_f:
                    alert(stick + 'Ping!')
                elif event.key == pygame.K_q:
                    if slowdown_tick + 2000 < tick:
                        slowdown_tick = tick
                        alert(stick + 'SLOWDOWN!')
                        slowdown_readymessageon = 1
                    else:
                        alert(stick + 'SLOWDOWN NOT READY')
                elif event.key == pygame.K_r and 'np' not in mods:
                    player.rect.center = (random.randint(0, scrw - 50), random.randint(0, scrh - 50))

        pressedkeys = pygame.key.get_pressed()

        #! === Update === !#
        if not 'np' in mods:
            if 'rt' in mods and tick % 10 == 0:
                if random.randint(1, 3) == 1:
                    player.rect.center = (random.randint(0, scrw - 50), random.randint(0, scrh - 50))

            if boost_tick + boost_length > tick:
                player.update(pressedkeys, 1)
            else:
                player.update(pressedkeys, 0)

        if tick == 5_000:
            enemy2 = evil_entity()
            alert(stick + 'A new glitch has appeared!')

        if tick == 10_000:
            enemy4 = evil_entity()
            alert(stick + 'A new glitch has appeared!')

        if tick > 4999:
            enemy2.update(player)
        if tick > 9999:
            enemy4.update(player)
        if 'eg' in mods:
            enemy3.update(player)

        enemy.update(player)

        #! === Speed === !#
        if tick % 50 == 0 and random.randint(1, 10) > 6:
            enemy.speed += 1
            if enemy.speed % 10 == 0:
                alert(stick + 'Glitch speed is now ' + str(enemy.speed) + ' pixels per tick!')

        if tick % 50 == 0 and random.randint(1, 10) > 6 and 'eg' in mods:
            enemy3.speed += 1
            if enemy.speed % 10 == 0:
                alert(stick + 'Glitch2 speed is now ' + str(enemy.speed) + ' pixels per tick!')

        if tick % 50 == 0 and random.randint(1, 10) > 4 and tick > 4999:
            enemy2.speed += 1
            if enemy2.speed % 10 == 0:
                alert(stick + 'New glitch speed is now ' + str(enemy2.speed) + ' pixels per tick!')

        if tick % 50 == 0 and random.randint(1, 10) > 2 and tick > 9999:
            enemy4.speed += 1
            if enemy4.speed % 10 == 0:
                alert(stick + 'New new glitch speed is now ' + str(enemy4.speed) + ' pixels per tick!')

        if not 'np' in mods:
            if tick % 500 == 0 and random.randint(1, 10) > 7:
                player.speed += 1
                if player.speed % 5 == 0:
                    alert(stick + 'Player speed is now ' + str(player.speed) + ' pixels per tick!')

        #! === Display === !#
        pygame.display.update()

        if debug:
            print('TICK ' + str(tick) + ':')
            print('ENEMY: ' + str(enemy.rect).replace('<rect(', '').replace(')>', '').replace(', 10, 10', ''))
            print('ENEMYSPEED: ' + str(enemy.speed))
            if tick > 4999:
                print('ENEMY2: ' + str(enemy2.rect).replace('<rect(', '').replace(')>', '').replace(', 10, 10', ''))
                print('ENEMY2SPEED: ' + str(enemy2.speed))
            if 'eg' in mods:
                print('ENEMY3: ' + str(enemy3.rect).replace('<rect(', '').replace(')>', '').replace(', 10, 10', ''))
                print('ENEMY3SPEED: ' + str(enemy3.speed))
            if tick > 9999:
                print('ENEMY4: ' + str(enemy4.rect).replace('<rect(', '').replace(')>', '').replace(', 10, 10', ''))
                print('ENEMY4SPEED: ' + str(enemy4.speed))
            if not 'np' in mods:
                print('PLAYER: ' + str(player.rect).replace('<rect(', '').replace(')>', '').replace(', 50, 50', ''))
                print('PLAYERSPEED: ' + str(player.speed))
            print('BOOSTTICK: ' + str(boost_tick))
            print('SLOWDOWNTICK: ' + str(slowdown_tick))
            print('-')

        #! === Tick === !#
        if slowdown_tick + 100 > tick:
            if 'sf' in mods:
                time.sleep(0.01)
            elif 'ss' in mods:
                time.sleep(1)
            else:
                time.sleep(0.1)
        else:
            if 'sf' in mods:
                time.sleep(0.001)
            elif 'ss' in mods:
                time.sleep(0.1)
            else:
                time.sleep(0.01)

#! === Score === !#
score = int(tick / 100)
if 'sf' in mods:
    score = int(score * 1.25)
if 'mg' in mods:
    score = int(score * 1.1)
elif 'bg' in mods:
    score = int(score * 1.02)
elif 'tg' in mods:
    score = int(score * 0.9)
if 'eg' in mods:
    score = int(score * 1.1)

#! === Exit === !#
if debug:
    print('GAME END TICK: ' + str(tick))
    print('EXIT CODE: ' + exitc)
    print('SCORE: ' + str(score))
else:
    print()
    
    if exitc == 'enemy_collision':
        print('You lost.')
        print('Score: ' + str(score))
        
    elif exitc == 'error':
        print('Error, quit.')
        print('Score: ' + str(score))
        
    elif exitc == 'user_quit':
        print('Quit.')
        print('Score: ' + str(score))