import pygame
import sys
from pygame.locals import *
import time
from game import *
import random
import os

def main():
    pygame.init()
    games = pygame.display.set_mode((GAME_WIDTH, GAME_HEIGHT))
    pygame.display.set_caption('Shooting')

    pygame.mixer.music.load("resources/sound/background.mp3")
    pygame.mixer.music.play(-1,0.0)
    pygame.mixer.music.set_volume(0.25)
    
    misile_sound = pygame.mixer.Sound(os.getcwd()+"\\resources\\sound\\bullet.wav")
    misile_sound.set_volume(0.15)
    
    enemy_sound = pygame.mixer.Sound(os.getcwd()+"\\resources\\sound\\enemy_down.wav")
    enemy_sound.set_volume(0.3)

    player_sound = pygame.mixer.Sound(os.getcwd()+"\\resources\\sound\\player_down.wav")
    player_sound.set_volume(0.3)

    item_sound = pygame.mixer.Sound(os.getcwd()+"\\resources\\sound\\effect.mp3")
    item_sound.set_volume(0.3)

    background = pygame.image.load('resources/image/background.png').convert()
    gameover = pygame.image.load('resources/image/gameover.png')
    cleared = pygame.image.load('resources/image/stageclear.png')

    plane_img = pygame.image.load('resources/image/plane.png')

    player_rect = []
    player_rect.append(pygame.Rect(50, 0, 50, 50))
    player_rect.append(pygame.Rect(0, 0, 33, 50))
    player_rect.append(pygame.Rect(113, 0, 33, 50))
    player_pos = [200, 600]
    player = Player(plane_img,player_rect,player_pos)

    misile_img = []
    misile_img.append(pygame.image.load("resources/image/misile1.png"))
    misile_img.append(pygame.image.load("resources/image/misile2.png"))
    misile_img.append(pygame.image.load("resources/image/misile3.png"))
    misile_img.append(pygame.image.load("resources/image/misile4.png"))

    enemy_img = pygame.image.load('resources/image/enemy.png')
    enemy_rect = pygame.Rect(0,0,32,32)
    enemy_down_img = pygame.image.load('resources/image/explosion1.png')
    enemy_down_imgs = []
    enemy_down_imgs.append(enemy_down_img.subsurface(pygame.Rect(0,0,32,32)))


    enemy2_img = pygame.image.load('resources/image/enemy2.png')
    enemy2_rect = pygame.Rect(0,0,96,96)

    enemy2_down_img = pygame.image.load('resources/image/explosion2.png')
    enemy2_down_imgs = []
    enemy2_down_imgs.append(enemy2_down_img.subsurface(pygame.Rect(0,0,96,96)))

    boss_img = pygame.image.load('resources/image/boss1.png')
    boss = Boss(boss_img,(0,-150))
    boss_group = pygame.sprite.Group()
    boss_hp = []
    boss_hp_img = pygame.image.load('resources/image/1.png')
    boss_explosion = pygame.image.load('resources/image/explosion3.png')
    boss_bullet = pygame.image.load('resources/image/boss_bullet.png')
    boss_bullet_rect = pygame.Rect(0,0,14,14)

    boss_bullets = pygame.sprite.Group()

    clear = False
    a = 440
    c=0
    d=10000
    while 1:
        if d < 0:
            break
        boss_hp.append(boss_hp_img.subsurface(pygame.Rect(0,0,a-22*c,22)))
        d=a-22*c
        c+=1


    enemies = pygame.sprite.Group()
    enemies2 = pygame.sprite.Group()

    enemies_down = pygame.sprite.Group()
    enemies2_down = pygame.sprite.Group()

    player_down_img = pygame.image.load('resources/image/explosion.png')
    player_down_imgs = []
    player_down_imgs.append(player_down_img.subsurface(pygame.Rect(0,0,50,50)))

    life_img = []
    life_img.append(pygame.image.load("resources/image/life1.png"))
    life_img.append(pygame.image.load("resources/image/life1.png").subsurface(pygame.Rect(0,0,70,38)))
    life_img.append(pygame.image.load("resources/image/life1.png").subsurface(pygame.Rect(0,0,35,38)))

    power_item_img = pygame.image.load('resources/image/power_item.png')
    life_item_img = pygame.image.load('resources/image/life_item.png')
    speed_item_img = pygame.image.load('resources/image/speed_item.png')
    
    shoot_frequency = 0
    shoot_range = 15
    enemy_frequemcy = 0
    enemy2_frequemcy = 0
    boss_frequency = 0

    score = 0

    clock = pygame.time.Clock()

    run = True
    lifes=0
    dmg=0

    stack=0
    boss_health = 200
    boss_appear = 30000

    while run:
        
        clock.tick(60)

        games.fill(0)
        games.blit(background, (0, 0))
        
        if not player.dead:
            games.blit(player.image[player.img_index], player.rect)
            player.img_index=0    
            ####### 총알 쏘기 및 속도 #######
            if shoot_frequency % shoot_range == 0:
                misile_sound.play()
                player.shoot(misile_img[dmg])
            shoot_frequency += 1

            if shoot_frequency >= shoot_range:
                shoot_frequency=0
        
            for misile in player.misiles:
                misile.move()
                if misile.rect.bottom < 0:
                    player.misiles.remove(misile)

            ####### 적 출현 #######
            if enemy2_frequemcy % 1000 == 0:
                enemy2_pos = [random.randint(0, GAME_WIDTH - enemy2_rect.width),0]
                enemy2 = Enemy(enemy2_img,enemy2_down_imgs, enemy2_pos)
                enemies2.add(enemy2)
            if score < boss_appear:
                enemy2_frequemcy += 1

            if enemy2_frequemcy >= 1000:
                enemy2_frequemcy = 0

            if enemy_frequemcy % 50 == 0:
                enemy_pos = [random.randint(0, GAME_WIDTH - enemy_rect.width), 0]
                enemy = Enemy(enemy_img,enemy_down_imgs, enemy_pos)
                enemies.add(enemy)
            if score < boss_appear:
                enemy_frequemcy += 1
            if enemy_frequemcy >=100:
                enemy_frequemcy = 0

            for enemy in enemies:
                enemy.move()
                if pygame.sprite.collide_circle(enemy, player):
                    player_sound.play()
                    enemies_down.add(enemy)
                    enemies.remove(enemy)
                    games.blit(player_down_imgs[0], (player.get_pos())) 
                    pygame.time.delay(30)

                    player.set_pos(200,600)
                    lifes += 1
                    dmg -= 1
                    shoot_range -= 1
                    if dmg < 0:
                        dmg = 0
                    if shoot_range > 15:
                        shoot_range = 15
                    if lifes > 2:
                        pygame.mixer.music.pause()
                        player.dead = True
                        lifes=0
                        break
            

                if enemy.rect.top > GAME_HEIGHT:
                    enemies.remove(enemy)
            
            for enemy in enemies2:
                enemy.move()
                if pygame.sprite.collide_circle(enemy, player):
                    player_sound.play()
                    enemies2_down.add(enemy)
                    enemies2.remove(enemy)
                    games.blit(player_down_imgs[0], (player.get_pos())) 
                    pygame.time.delay(30)

                    player.set_pos(200,600)
                    lifes += 1
                    dmg -= 1
                    shoot_range -= 1
                    if dmg < 0:
                        dmg = 0
                    if shoot_range > 15:
                        shoot_range = 15
                    if lifes > 2:
                        pygame.mixer.music.pause()
                        player.dead = True
                        lifes=0
                        break
                    

                if enemy.rect.top > GAME_HEIGHT:
                    enemies2.remove(enemy)

            enemies1_down = pygame.sprite.groupcollide(enemies, player.misiles, 1, 1)

            for enemy_down in enemies1_down:
                enemy_sound.play()
                enemies_down.add(enemy_down)

            for enemy_down in enemies_down:
                if enemy_down.down_index > 7:
                    enemies_down.remove(enemy_down)
                    score+=100
                    continue

                games.blit(enemy_down.down_imgs[0],enemy_down.rect)
                enemy_down.down_index += 1
            
            enemies3_down = pygame.sprite.groupcollide(enemies2, player.misiles, False, False)
            if enemies3_down != {}:
                if dmg == 0:
                    stack += 1
                    if stack >= 2:
                        enemies3_down = pygame.sprite.groupcollide(enemies2, player.misiles, True, True)
                    else:
                        enemies3_down = pygame.sprite.groupcollide(enemies2, player.misiles, False, True)
                else:
                    stack += 2
                    if stack >= 2:
                        enemies3_down = pygame.sprite.groupcollide(enemies2, player.misiles, True, True)
                    else:
                        enemies3_down = pygame.sprite.groupcollide(enemies2, player.misiles, False, True)

            for enemy_down in enemies3_down:
                enemy_sound.play()
                if stack >= 2:                   
                    stack = 0
                    enemies2_down.add(enemy_down)
                    rand = random.randint(1,6)
                    if rand == 6:
                        enemy2.give_power_item(power_item_img)
                    if rand == 5:
                        enemy2.give_life_item(life_item_img)
                    if rand == 4:
                        enemy2.give_speed_item(speed_item_img)
            ####### 보스 #######
            
            boss_group.add(boss)
            if boss_health <= 0:
                boss_a = 20
            elif boss_health <= 10:
                boss_a = 19
            elif boss_health <= 20:
                boss_a = 18
            elif boss_health <= 30:
                boss_a = 17
            elif boss_health <= 40:
                boss_a = 16
            elif boss_health <= 50:
                boss_a = 15
            elif boss_health <= 60:
                boss_a = 14
            elif boss_health <= 70:
                boss_a = 13
            elif boss_health <= 80:
                boss_a = 12
            elif boss_health <= 90:
                boss_a = 11
            elif boss_health <= 100:
                boss_a = 10
            elif boss_health <= 110:
                boss_a = 9
            elif boss_health <= 120:
                boss_a = 8
            elif boss_health <= 130:
                boss_a = 7
            elif boss_health <= 140:
                boss_a = 6
            elif boss_health <= 150:
                boss_a = 5
            elif boss_health <= 160:
                boss_a = 4
            elif boss_health <= 170:
                boss_a = 3
            elif boss_health <= 180:
                boss_a = 2
            elif boss_health <= 190:
                boss_a = 1
            elif boss_health <= 200:
                boss_a = 0
            if score > boss_appear:
                if boss_health > 0:
                    games.blit(boss.image,boss.rect)
                
                games.blit(boss_hp[boss_a], (20,50))
                if boss.rect.top < 0:
                    boss.move()
                else:
                    boss_bullet_pos = [random.randint(0, GAME_WIDTH - boss_bullet_rect.width),220]
                    boss_s = Enemy(boss_bullet,enemy2_down_imgs, boss_bullet_pos)
                    boss_frequency += 1
                    if boss_frequency%20 == 0:
                        boss_bullets.add(boss_s)
                        boss_bullets.add(boss_s)
                        boss_bullets.add(boss_s)
                        boss_bullets.add(boss_s)
                        boss_bullets.add(boss_s)
                        boss_frequency=0
                
                boss_down = pygame.sprite.groupcollide(boss_group, player.misiles, False, False)
                for bosses in boss_group:
                    if pygame.sprite.collide_rect(bosses, player):
                        player_sound.play()
                        games.blit(player_down_imgs[0], (player.get_pos())) 
                        pygame.time.delay(30)
                        player.set_pos(200,600)
                        lifes += 1
                        dmg -= 1
                        shoot_range -= 1
                        if dmg < 0:
                            dmg = 0
                        if shoot_range > 15:
                            shoot_range = 15                        
                        if lifes > 2:
                            pygame.mixer.music.pause()
                            player.dead = True
                            lifes=0
                            break   
                

                for bosses in boss_bullets:
                    bosses.move()
                    if pygame.sprite.collide_circle(bosses, player):
                        player_sound.play()
                        boss_bullets.remove(bosses)
                        games.blit(player_down_imgs[0], (player.get_pos())) 
                        pygame.time.delay(30)

                        player.set_pos(200,600)
                        lifes += 1
                        dmg -= 1
                        shoot_range -= 1
                        if dmg < 0:
                            dmg = 0
                        if shoot_range > 15:
                            shoot_range = 15                        
                        if lifes > 2:
                            pygame.mixer.music.pause()
                            player.dead = True
                            lifes=0
                            break
            

                    if bosses.rect.top > GAME_HEIGHT:
                        boss_bullets.remove(bosses)


                if boss_down != {}:
                    if dmg == 0:
                        boss_health -= 1
                        if boss_health < 0:
                            enemy_sound.play()
                            games.blit(boss_explosion,(96,0))
                            boss_down = pygame.sprite.groupcollide(boss_group, player.misiles, True, True)
                            clear = True
                            player.dead = True
                        else:
                            boss_down = pygame.sprite.groupcollide(boss_group, player.misiles, False, True)
                            
                    elif dmg == 1:
                        boss_health -= 2
                        if boss_health < 0:
                            enemy_sound.play()
                            games.blit(boss_explosion,(96,0))
                            boss_down = pygame.sprite.groupcollide(boss_group, player.misiles, True, True)
                            clear = True
                            player.dead = True
                        else:
                            boss_down = pygame.sprite.groupcollide(boss_group, player.misiles, False, True)

                    elif dmg == 2:
                        boss_health -= 3
                        if boss_health < 0:
                            enemy_sound.play()
                            games.blit(boss_explosion,(96,0))
                            boss_down = pygame.sprite.groupcollide(boss_group, player.misiles, True, True)
                            clear = True
                            player.dead = True
                        else:
                            boss_down = pygame.sprite.groupcollide(boss_group, player.misiles, False, True)

                    elif dmg == 3:
                        boss_health -= 4
                        if boss_health < 0:
                            enemy_sound.play()
                            games.blit(boss_explosion,(96,0))
                            boss_down = pygame.sprite.groupcollide(boss_group, player.misiles, True, True)
                            clear = True
                            player.dead = True
                        else:
                            boss_down = pygame.sprite.groupcollide(boss_group, player.misiles, False, True)



            ####### 아이템 #######
            for itema in enemy2.power_items:
                itema.move()
                if pygame.sprite.collide_circle(itema, player):
                    item_sound.play()
                    enemy2.power_items.remove(itema)
                    dmg += 1
                    if dmg > 3:
                        dmg=3

                if itema.rect.top > GAME_HEIGHT:
                    enemy2.power_items.remove(itema)
            
            for itema in enemy2.life_items:
                itema.move()
                if pygame.sprite.collide_circle(itema, player):
                    item_sound.play()
                    enemy2.life_items.remove(itema)
                    lifes -= 1
                    if lifes < 0:
                        lifes =0 

                if itema.rect.top > GAME_HEIGHT:
                    enemy2.life_items.remove(itema)            

            for itema in enemy2.speed_items:
                itema.move()
                if pygame.sprite.collide_circle(itema, player):
                    item_sound.play()
                    enemy2.speed_items.remove(itema)
                    shoot_range-=1
                    if shoot_range < 8:
                        shoot_range = 9

                if itema.rect.top > GAME_HEIGHT:
                    enemy2.speed_items.remove(itema)

            for enemy_down in enemies2_down:
                if enemy_down.down_index > 7:
                    enemies2_down.remove(enemy_down)
                    score+=1000
                    continue

                games.blit(enemy_down.down_imgs[0],enemy_down.rect)
                enemy_down.down_index += 1

            player.misiles.draw(games)
            enemies.draw(games)
            enemies2.draw(games)
            enemy2.power_items.draw(games)
            enemy2.speed_items.draw(games)
            enemy2.life_items.draw(games)
            boss_bullets.draw(games)
            
            games.blit(life_img[lifes], (375,0))
            

        score_font = pygame.font.Font(None, 36)
        score_text = score_font.render(str(score), True, (255, 255, 255))
        text_rect = score_text.get_rect()
        text_rect.topleft = [10, 10]

        games.blit(score_text, text_rect)

        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        
        
        ####### 플레이어 이동 #######
        
        key_pressed = pygame.key.get_pressed()
        
        if not player.dead:
            if key_pressed[K_w] or key_pressed[K_UP]:
                player.moveUp()
            if key_pressed[K_s] or key_pressed[K_DOWN]:
                player.moveDown()
            if key_pressed[K_a] or key_pressed[K_LEFT]:
                player.moveLeft()
                player.img_index=1
            if key_pressed[K_d] or key_pressed[K_RIGHT]:
                player.moveRight()
                player.img_index=2
        ####### 플레이어 사망 시 #######
        if player.dead:
            while 1:
                if clear == False:
                    games.blit(gameover,(0,0))
                else:
                    games.blit(cleared,(0,0))
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_r:
                            main()
                pygame.display.update()

if __name__ == "__main__":
    main()                

