# !/usr/bin/python
# -*- coding: utf-8 -*-
import datetime
import modi
import os
import random
import threading
import time

import pygame
bundle = modi.MODI()
bundle.modules
# Global Constants

btn = bundle.buttons[0]
#speaker =bundle.speakers[0]
led= bundle.leds[0]
dial = bundle.dials[0]
pygame.init()

endMenuGameMusic = False
playGameMusic= False
startMenuGameMusic= False
SCREEN_HEIGHT = 600
SCREEN_WIDTH = 1100
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

pygame.display.set_caption("Chrome Dino Runner")

Ico = pygame.image.load("assets/DinoWallpaper.png")
pygame.display.set_icon(Ico)

RUNNING = [
    pygame.image.load(os.path.join("assets/Dino", "DinoRun1.png")),
    pygame.image.load(os.path.join("assets/Dino", "DinoRun2.png")),
]
JUMPING = pygame.image.load(os.path.join("assets/Dino", "DinoJump.png"))
DUCKING = [
    pygame.image.load(os.path.join("assets/Dino", "DinoDuck1.png")),
    pygame.image.load(os.path.join("assets/Dino", "DinoDuck2.png")),
]

SMALL_CACTUS = [
    pygame.image.load(os.path.join("assets/Cactus", "SmallCactus1.png")),
    pygame.image.load(os.path.join("assets/Cactus", "SmallCactus2.png")),
    pygame.image.load(os.path.join("assets/Cactus", "SmallCactus3.png")),
]
LARGE_CACTUS = [
    pygame.image.load(os.path.join("assets/Cactus", "LargeCactus1.png")),
    pygame.image.load(os.path.join("assets/Cactus", "LargeCactus2.png")),
    pygame.image.load(os.path.join("assets/Cactus", "LargeCactus3.png")),
]

BIRD = [
    pygame.image.load(os.path.join("assets/Bird", "Bird1.png")),
    pygame.image.load(os.path.join("assets/Bird", "Bird2.png")),
]

CLOUD = pygame.image.load(os.path.join("assets/Other", "Cloud.png"))

BG = pygame.image.load(os.path.join("assets/Other", "Track.png"))

FONT_COLOR=(0,0,0)

class Dinosaur:

    X_POS = 80
    Y_POS = 310
    Y_POS_DUCK = 340
    JUMP_VEL = 8.5

    def __init__(self):
        self.duck_img = DUCKING
        self.run_img = RUNNING
        self.jump_img = JUMPING

        self.dino_duck = False
        self.dino_run = True
        self.dino_jump = False

        self.step_index = 0
        self.jump_vel = self.JUMP_VEL
        self.image = self.run_img[0]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS

    def update(self, userInput,clickInput,dialDegree):
        if self.dino_duck:
            self.duck()
        if self.dino_run:
            self.run()
        if self.dino_jump:
            self.jump()

        if self.step_index >= 10:
            self.step_index = 0
            
#   ___|   _ \   __ \   ____| 
#  |      |   |  |   |  __|   
#  |      |   |  |   |  |     
# \____| \___/  ____/  _____| 
########################################################################################################  
# 공룡이 움직이는 방법을 설정해봐요 . 현재는 클릭 시 점프 , 다이얼이 50이상일 때 고개를 숙여요. 나만의 코드를 작성해보세요. (추가로 마이크 모듈이나 환경 모듈도 추가할 수 있어요!)                
        if(clickInput == True )and not self.dino_jump:
            self.dino_jump= True
            self.dino_run = False
            self.dino_jump = True
        elif (dialDegree>50) and not self.dino_jump:
            self.dino_duck = True
            self.dino_run = False
            self.dino_jump = False
        elif(dialDegree<50) and not self.dino_jump:
            self.dino_duck = False
            self.dino_run = True
            self.dino_jump = False

##############################################################################################            

    def duck(self):
        self.image = self.duck_img[self.step_index // 5]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS_DUCK
        self.step_index += 1

    def run(self):
        self.image = self.run_img[self.step_index // 5]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS
        self.step_index += 1

    def jump(self):
        self.image = self.jump_img
        if self.dino_jump:
            self.dino_rect.y -= self.jump_vel * 4
            self.jump_vel -= 0.8
        if self.jump_vel < -self.JUMP_VEL:
            self.dino_jump = False
            self.jump_vel = self.JUMP_VEL

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.dino_rect.x, self.dino_rect.y))


class Cloud:
    def __init__(self):
        self.x = SCREEN_WIDTH + random.randint(800, 1000)
        self.y = random.randint(50, 100)
        self.image = CLOUD
        self.width = self.image.get_width()

    def update(self):
        self.x -= game_speed
        if self.x < -self.width:
            self.x = SCREEN_WIDTH + random.randint(2500, 3000)
            self.y = random.randint(50, 100)

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.x, self.y))


class Obstacle:
    def __init__(self, image, type):
        self.image = image
        self.type = type
        self.rect = self.image[self.type].get_rect()
        self.rect.x = SCREEN_WIDTH

    def update(self):
        self.rect.x -= game_speed
        if self.rect.x < -self.rect.width:
            obstacles.pop()

    def draw(self, SCREEN):
        SCREEN.blit(self.image[self.type], self.rect)


class SmallCactus(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = 325


class LargeCactus(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = 300


class Bird(Obstacle):
    BIRD_HEIGHTS = [250, 290, 320]

    def __init__(self, image):
        self.type = 0
        super().__init__(image, self.type)
        self.rect.y = random.choice(self.BIRD_HEIGHTS)
        self.index = 0

    def draw(self, SCREEN):
        if self.index >= 9:
            self.index = 0
        SCREEN.blit(self.image[self.index // 5], self.rect)
        self.index += 1


def main():
    global game_speed, x_pos_bg, y_pos_bg, points, obstacles
#   ___|   _ \   __ \   ____| 
#  |      |   |  |   |  __|   
#  |      |   |  |   |  |     
# \____| \___/  ____/  _____| 
                            
 #################################################################################
#게임 플레이 중 LED를 색상을 설정해주세요. 현재는 파란색으로 시작해요.나만의 코드를 작성해보세요. (추가로 디스플레이 모듈, 모터 모듈도 추가할 수 있어요!)
#                                                                                    
    led.rgb = (0,0,100) # 시작시 파란색                                                                                    

            

##################################################################################      
    
    run = True
    clock = pygame.time.Clock()
    player = Dinosaur()
    cloud = Cloud()
    game_speed = 20
    x_pos_bg = 0
    y_pos_bg = 380
    points = 0
    font = pygame.font.Font("freesansbold.ttf", 20)
    obstacles = []
    death_count = 0
    pause = False
   
    def score():
        global points, game_speed
        points += 1
        if points % 100 == 0:
            game_speed += 1
        current_time = datetime.datetime.now().hour
        with open("score.txt", "r") as f:
            score_ints = [int(x) for x in f.read().split()]  
            highscore = max(score_ints)
            if points > highscore:
                highscore=points 
            text = font.render("High Score: "+ str(highscore) + "  Points: " + str(points), True, FONT_COLOR)
        textRect = text.get_rect()
        textRect.center = (900, 40)
        SCREEN.blit(text, textRect)

    def background():
        global x_pos_bg, y_pos_bg
        image_width = BG.get_width()
        SCREEN.blit(BG, (x_pos_bg, y_pos_bg))
        SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg))
        if x_pos_bg <= -image_width:
            SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg))
            x_pos_bg = 0
        x_pos_bg -= game_speed

    def unpause():
        nonlocal pause, run
        pause = False
        run = True

    def paused():
      
        nonlocal pause
        pause = True
        font = pygame.font.Font("freesansbold.ttf", 30)
        text = font.render("Game Paused, Press 'u' to Unpause", True, FONT_COLOR)
        textRect = text.get_rect()
        textRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT  // 3)
        SCREEN.blit(text, textRect)
        pygame.display.update()

        while pause:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_u:
                    unpause()
   
    while run:
       
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                run = False
                paused()

        current_time = datetime.datetime.now().hour
        if 7 < current_time < 19:
            SCREEN.fill((255, 255, 255))
        else:
            SCREEN.fill((0, 0, 0))
        userInput = pygame.key.get_pressed() #
#   ___|   _ \   __ \   ____| 
#  |      |   |  |   |  __|   
#  |      |   |  |   |  |     
# \____| \___/  ____/  _____| 
########################################################################################################  
# 공룡이 움직이는 방법을 설정해봐요 . 현재는 클릭 시 점프 , 다이얼이 50이상일 때 고개를 숙여요. 나만의 코드를 작성해보세요. (추가로 마이크 모듈이나 환경 모듈도 추가할 수 있어요!)    
                                                                                                                                                                                             
        clickInput = btn.clicked
        dialDegree = dial.degree
        player.draw(SCREEN)
        player.update(userInput,clickInput,dialDegree)

##########################################################################################################
        if len(obstacles) == 0:
            if random.randint(0, 2) == 0:
                obstacles.append(SmallCactus(SMALL_CACTUS)) 
            elif random.randint(0, 2) == 1:
                obstacles.append(LargeCactus(LARGE_CACTUS))
            elif random.randint(0, 2) == 2:
                obstacles.append(Bird(BIRD))
   
        for obstacle in obstacles:
            obstacle.draw(SCREEN)
            obstacle.update()
            if player.dino_rect.colliderect(obstacle.rect):
                pygame.time.delay(2000)
                death_count += 1
               
                print("speker")
                menu(death_count)      
        
        background()   
        cloud.draw(SCREEN)
        cloud.update()
        score()

        clock.tick(30)
        pygame.display.update()


def menu(death_count):
    global points, speakerFlag
    global FONT_COLOR
    run = True

    while run:
        endMenuGameMusic = False
        playGameMusic= True 
        startMenuGameMusic = False

        current_time = datetime.datetime.now().hour
        if 7 < current_time < 19:
            FONT_COLOR=(0,0,0)
            SCREEN.fill((255, 255, 255))
        else:
            FONT_COLOR=(255,255,255)
            SCREEN.fill((128, 128, 128))
        font = pygame.font.Font("freesansbold.ttf", 30)

        if death_count == 0:
            text = font.render("Press any Key to Start", True, FONT_COLOR)
         
                                                                                             
#   ___|   _ \   __ \   ____| 
#  |      |   |  |   |  __|   
#  |      |   |  |   |  |     
# \____| \___/  ____/  _____| 
                            
 #################################################################################
#처음 시작 시 메뉴 상태에서 LED를 색상을 설정해주세요. 현재는 파란색으로 시작해요.나만의 코드를 작성해보세요. (추가로 디스플레이 모듈, 모터 모듈도 추가할 수 있어요!)                                                                                   
                                                                                    

            led.rgb = (0,0,100) # 시작시 파란색

##################################################################################            
        elif death_count > 0:
            text = font.render("Press any Key to Restart", True, FONT_COLOR)
             #기능 추가 점수 -> 피할 때 소리 -> 일시정지 -> 게임 종료 
            score = font.render("Your Score: " + str(points), True, FONT_COLOR)

                                                                                                                    
#   ___|   _ \   __ \   ____| 
#  |      |   |  |   |  __|   
#  |      |   |  |   |  |     
# \____| \___/  ____/  _____| 
#################################################################################################### 
# 게임 재시작 시 메뉴 화면에서의 LED 색상 설정해주세요 . 나만의 코드를 작성해보세요. (추가로 디스플레이 모듈, 모터 모듈도 추가할 수 있어요!)                                                                                                        
                                                                                                        

            led.rgb = (100,0,0) # 시작시 빨간색
####################################################################################################
            
            scoreRect = score.get_rect()
            scoreRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50)
            SCREEN.blit(score, scoreRect)
            f = open("score.txt", "a")
            f.write(str(points) + "\n")
            f.close()
            with open("score.txt", "r") as f:
                score = (
                    f.read()
                )  
                score_ints = [int(x) for x in score.split()]  
            highscore = max(score_ints)  
            hs_score_text = font.render(
                "High Score : " + str(highscore), True, FONT_COLOR
            )
            hs_score_rect = hs_score_text.get_rect()
            hs_score_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100)
            SCREEN.blit(hs_score_text, hs_score_rect)
            

           
        textRect = text.get_rect()
        textRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        SCREEN.blit(text, textRect)
        SCREEN.blit(RUNNING[0], (SCREEN_WIDTH // 2 - 20, SCREEN_HEIGHT // 2 - 140))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                main()
        
t1 = threading.Thread(target=menu(death_count=0), daemon=True)
t1.start()
