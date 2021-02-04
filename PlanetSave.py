import pygame
import math
import random
from tkinter import *

pygame.init()


#행성 범위 설정 (131,88),(410,138) <-- 클릭 시 행성 변경.

#play 범위 (131, 426), (353, 483)

#quit 범위 (457, 432), (631, 477)



size   = [800, 600]
screen = pygame.display.set_mode(size)
angle=None


#이미지 로드 시작
logo=pygame.image.load('image/logo.png')
play=[pygame.image.load('image/play.png'),pygame.image.load('image/play2.png')]
quitt=[pygame.image.load('image/quit.png'),pygame.image.load('image/quit2.png')]

cursor=[pygame.image.load('image/cursor/cursor1.png'),pygame.image.load('image/cursor/cursor2.png'),pygame.image.load('image/cursor/cursor3.png')]
pygame.display.set_caption("Planet Save")

ship=[pygame.image.load('image/ship/ship'+str(random.randrange(0,3)+1)+'.png'),pygame.image.load('image/ship/ship'+str(random.randrange(0,3)+1)+'_1.png')]
shot=pygame.image.load('image/shot.png')
planet=[]
for i in range(4) :
    planet.append(pygame.image.load('image/planet/planet'+str(i+1)+'.png'))
eyes=[]
for i in range(4) :
    eyes.append(pygame.image.load('image/eyes/eyes'+str(i+1)+'.png'))


bg=pygame.image.load('image/background.png')
shadow=pygame.image.load('image/planet/shadow.png')

healthbar=pygame.image.load('image/health/healthbar.png')
healthbarin=[]
for i in range(5) :
    healthbarin.append(pygame.image.load('image/health/health_bar'+str(i)+'.png'))

#이미지 로드 끝


# 사운드
crush_sound=pygame.mixer.Sound('sound/crush.wav')
hits=pygame.mixer.Sound('sound/hits.wav')
pygame.mixer.music.load('sound/background.mp3')
gameover=pygame.mixer.Sound('sound/gameover.wav')
#pygame.mixer.music.load('sound/background2.wav')
pygame.mixer.music.play(-1) #-1무한 재생

#사운드 끝

screen.blit(bg, (0,0))
centerX=size[0]/2
centerY=size[1]/2

pygame.mouse.set_visible(0)


done  = False
clock = pygame.time.Clock()
FPS = 60
click = 0
planet_speed = 0.0
shot_speed = 85
ship_state=0
position=[0,0]

play_state=0
quit_state=0
eyes_state=0
start_state=0
check=0

moving=25

planet_char=random.randrange(0,4)
shot_state=[]

star_angle=[0.0,0.0,0.0,0.0]
t=0
q=0
area=5
st=0

ti=0
time=0
checktime=0
shot_sw=0
level=0

HP=4

score=[]
score_name=[]

myfont=pygame.font.Font('avant_pixel.ttf',25)


#운석 클래스
class starClass:
    hap=0
    rotate=None
    def __init__(self,num):
        self.image = [pygame.image.load('image/star/star'+str(num+1)+'_1.png'),pygame.image.load('image/star/star'+str(num+1)+'_2.png'),pygame.image.load('image/star/star'+str(num+1)+'_3.png')]
        self.angle=random.randrange(1,36)+random.random()
        self.crush=random.randrange(0,3)
        self.speed=random.random()+0.1
        self.distance=random.randrange(450,5000)
        self.t=random.randrange(2,6)

cometru=[]

#스크린 위치 함수
def pos(img_position):
    position=img_position.get_size()
    return centerX-position[0]/2,centerY-position[1]/2

#앵글 방향으로 회전 함수
def vision(shape,angle,radius):
    return centerX-(shape.get_size()[0]/2)+(math.cos(angle)*radius),centerY-(shape.get_size()[1]/2)+(math.sin(angle)*radius)

#운석 회전 함수
def star_rotate(shape):
    global t
    return pygame.transform.rotate(shape,t)

#충돌 판정 함수
def crush(shape1,shape2,star):
    global area
    if (shape1[0]-area<shape2[0] and shape2[0]<shape1[0]+(star[0]-area)) and (shape1[1]-area<shape2[1] and shape2[1]<shape1[1]+(star[1]-area)) : 
        return 1
    return 0

#시간 함수
def timegender(time):
    HH,MM,SS=0,0,0
    HH=time//3600
    if HH!=0: time=time%3600
    MM=time//60
    if MM!=0: time=time%60
    SS=time
    if HH<10:HH='0'+str(HH)
    else: HH=str(HH)
    if MM<10:MM='0'+str(MM)
    else: MM=str(MM)
    if SS<10:SS='0'+str(SS)
    else: SS=str(SS)
    return HH+":"+MM+":"+SS


#랭크 화면
def rank(score,score_name):
    global cursor,click,clock,FPS,position,myfont
    bg=pygame.image.load('image/rankbackground.png')
    size   = [400, 600]
    done=0
    screen2 = pygame.display.set_mode(size)
    ranktxt=myfont.render(u'RANK',True,(255,255,255))
    ranking=[]
    tmp=0;
    text=None
    print(len(score))
    if(len(score)>1):
        lent=len(score)
        for i in (0,lent-2):
            for j in (0,(lent-i)-2):
                if score[j]<score[j+1] :
                    tmp=score[j]
                    score[j]=score[j+1]
                    score[j+1]=tmp
                    text=score_name[j]
                    score_name[j]=score_name[j+1]
                    score_name[j+1]=text
    j=len(score)
    if len(score)>5:
        j=5
    #print(score)
    while not done:
        clock.tick(FPS)
        screen2.blit(bg, (0,0))
        screen2.blit(ranktxt, (200-(ranktxt.get_size()[0]/2),75))
        #score.sort(reverse=True)
        for i in range(0,j):
            ranking.append(myfont.render(u''+str(i+1)+' Rank : '+timegender(score[i])+"  "+score_name[i],True,(255,255,255)))
            screen2.blit(ranking[i], (200-(ranking[i].get_size()[0]/2),200+(i*50)))
        #마우스 모양
        if click == 0 :
            screen2.blit(cursor[0],(position[0],position[1]))
        elif click == 1:
            screen2.blit(cursor[1],(position[0],position[1]))
            
        #마우스 모션
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.MOUSEMOTION:
                position=pygame.mouse.get_pos()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button==1:
                    click=1
            elif event.type == pygame.MOUSEBUTTONUP:
                click=0
        pygame.display.flip()


def rankname():
    def close():
        global score_name
        score_name.append(txt.get())
        root.quit()
        root.destroy()
    root = Tk()

    root.geometry('250x100')
    root.title("랭크 이름을 입력하세요.")
    root.resizable(True, True)

    label01 = Label(root, text="랭크 이름 : ")
    label01.pack()
    txt=Entry(root)
    txt.pack()

    quit01 = Button(root, text="확인", command=close, bg='white', fg='blue')
    quit01.pack()
    root.mainloop()

starttxt=myfont.render(u'Game Start! 5',True,(255,255,255))
txt=myfont.render(u'time : '+timegender(time),True,(255,255,255))
cometruTxt=myfont.render(u'Remaining meteorite : ',True,(255,255,255))
#stark1=pygame.transform.rotate(star[0][0],t)


while not done:
    clock.tick(FPS)
    #배경, 행성, 게임시작,나가기 초기화
    screen.blit(bg, (0,0))
    if(start_state==0):
        if HP==0:
            if moving>=0:
                screen.blit(logo,(pos(logo)[0]+moving,pos(logo)[1]-185))
                screen.blit(play[play_state],(pos(play[play_state])[0]-150-moving,pos(play[play_state])[1]+160))
                screen.blit(quitt[quit_state],(pos(quitt[quit_state])[0]+150+moving,pos(quitt[quit_state])[1]+160))
                moving=moving-25
            if moving==-25:
                HP=4
                pygame.time.wait(100)
                rankname()
                rank(score,score_name)
                screen = pygame.display.set_mode(size)
        else:
            screen.blit(logo,(pos(logo)[0],pos(logo)[1]-185))
            screen.blit(play[play_state],(pos(play[play_state])[0]-150,pos(play[play_state])[1]+160))
            screen.blit(quitt[quit_state],(pos(quitt[quit_state])[0]+150,pos(quitt[quit_state])[1]+160))
    elif(moving<600):
        screen.blit(logo,(pos(logo)[0]+moving,pos(logo)[1]-185))
        screen.blit(play[play_state],(pos(play[play_state])[0]-150-moving,pos(play[play_state])[1]+160))
        screen.blit(quitt[quit_state],(pos(quitt[quit_state])[0]+150+moving,pos(quitt[quit_state])[1]+160))
        moving=moving+25
        
    
    planet_speed=(planet_speed+0.3)%360
    planet2=pygame.transform.rotozoom(planet[planet_char],planet_speed,1)
    screen.blit(planet2,pos(planet2))

    screen.blit(shadow,(pos(shadow)[0],pos(shadow)[1]+30))
    # 우주선
    angle=math.atan2(position[1]-centerY,position[0]-centerX)
    angle2 = angle * (180/math.pi) #호도법을 육십분법으로 바꿔줌
    angle2 = (angle2 + 90) % 360

    ship2=pygame.transform.rotate(ship[ship_state],-angle2)
    ship_state=0
        
    #-(ship2.get_size()[0]/2) 하는 이유는 rotate를 할때 이미지 좌표가 달라진다 그러므로 바뀔때마다 이미지 크기를 불러와서 다시 빼줘야한다
    x2,y2=vision(ship2,angle,85) #85는 반지름 길이이다.
    screen.blit(ship2,(x2,y2))
    #우주선 끝

    #눈 표시
    screen.blit(eyes[eyes_state],vision(eyes[eyes_state],angle,20))

    #star_angle=math.atan2(,)

    #시간초 표시 게임시작
    if moving>=600:
        #HP가 0이 되었다.
        if HP!=0:
            screen.blit(healthbar,(10,10))
            screen.blit(healthbarin[HP],(10,10))
            ti=ti+1
            if ti==FPS :
                ti=ti%FPS
                time=time+1
                if time<=5 and checktime==0:
                    starttxt=myfont.render(u'Game Start! '+str(5-time),True,(255,255,255))
                elif checktime==0 :
                    time=0
                    checktime=1
                if checktime==1:
                    txt=myfont.render(u'time : '+timegender(time),True,(255,255,255))
            if time==30 :
                level=0.5
            if time==60:
                level=1
            if time==90:
                level=1.5
            if time==120:
                level=2
            #운석 화면 출력
            if checktime==1 :
                if len(cometru)==0 :
                    HP=0
                    score.append(time)
                    checktime=0
                    ti=0
                    time=0
                    start_state=0
                for i in range(0,len(cometru)):
                    cometru[i].hap=(cometru[i].hap+cometru[i].t)%360
                    cometru[i].distance=cometru[i].distance-(cometru[i].speed+level)
                    cometru[i].ratate=pygame.transform.rotate(cometru[i].image[cometru[i].crush],cometru[i].hap)
                    #행성에 운석이 박히면 운석을 지운다.
                    if crush((centerX-(planet2.get_size()[0]/2),centerY-(planet2.get_size()[1]/2)),vision(cometru[i].ratate,cometru[i].angle,cometru[i].distance),planet[planet_char].get_size()):
                        pygame.mixer.Sound.play(crush_sound)
                        cometru.remove(cometru[i])
                        eyes_state=3
                        HP=HP-1
                        screen.blit(healthbar,(10,10))
                        pygame.mixer.Sound.play(gameover)
                        if HP==0:
                            del cometru[:]
                            score.append(time)
                            checktime=0
                            ti=0
                            time=0
                            start_state=0
                        break
                    screen.blit(cometru[i].ratate,vision(cometru[i].ratate,cometru[i].angle,cometru[i].distance))
            #텍스트 출력
            if checktime==0: screen.blit(starttxt,(296,95))
            if checktime==1:
                screen.blit(txt,(296,95))
                cometruTxt=myfont.render(u'Remaining meteorite : '+str(len(cometru)),True,(255,255,255))
                screen.blit(cometruTxt,(30,550))
        
    

    #마우스 클릭
    if click == 0 and start_state==0:
        screen.blit(cursor[0],(position[0],position[1]))
    elif click == 1 and start_state==0:
        screen.blit(cursor[1],(position[0],position[1]))

    if start_state==1:
        screen.blit(cursor[2],(position[0]-cursor[2].get_size()[0]/2,position[1]-cursor[2].get_size()[1]/2))
    
    #마우스 클릭 끝

    
    #슈팅 게임때 쓸꺼.
    for i in range(0,len(shot_state)) :
        x,y=vision(shot_state[i][0],shot_state[i][1],shot_state[i][2])
        shot_state[i][2]=shot_state[i][2]+10
        screen.blit(shot_state[i][0],(x,y))
        if checktime==1 : 
            for j in range(0,len(cometru)):
                if moving>=600 and crush(vision(cometru[j].ratate,cometru[j].angle,cometru[j].distance),(x,y),cometru[j].ratate.get_rect().size):
                    cometru[j].crush=cometru[j].crush+1
                    pygame.mixer.Sound.play(crush_sound)
                    if cometru[j].crush==3:
                        cometru.remove(cometru[j])
                    #print("충돌!"+str(st))
                    shot_sw=1
                    break
        if shot_sw==1:
            shot_state.remove(shot_state[i])
            shot_sw=0
            break
        if (x<0 or x>820) or (y<0 or y>620) :
            shot_state.remove(shot_state[i])
            break

    
    #마우스 이벤트 발생
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.MOUSEMOTION:
            position=pygame.mouse.get_pos()
            #eyes_state=0
            #게임시작 나가기 얼굴 표정 변환
            if(start_state==0):
                if (131<position[0] and position[0]<353) and (426<position[1] and position[1]<483):
                    play_state=1
                    eyes_state=1
                else:
                    play_state=0
                if (457<position[0] and position[0]<631) and (432<position[1] and position[1]<477):
                    quit_state=1
                    eyes_state=2
                else:
                    quit_state=0
            #print(position[0],position[1],angle)   
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button==1:
                eyes_state=0
                pygame.mixer.Sound.play(hits)
                if(start_state==0):
                    if (132<position[0] and position[0]<412) and (83<position[1] and position[1]<135):
                        planet_char=(planet_char+1)%4
                    #게임시작
                    if (131<position[0] and position[0]<353) and (426<position[1] and position[1]<483):
                        start_state=1
                        moving=25
                        for i in range(0,100):
                            cometru.append(starClass(random.randrange(0,4)))
                        starttxt=myfont.render(u'Game Start! 5',True,(255,255,255))
                        level=0
                    #나가기 클릭
                    if (457<position[0] and position[0]<631) and (432<position[1] and position[1]<477):
                        done = True
                #print(pygame.mouse.get_pos(),eyes_state)
                click=1
                ship_state=1
                shot_state.append([pygame.transform.rotate(shot,-angle2),angle,shot_speed])
        elif event.type == pygame.MOUSEBUTTONUP:
            click=0
    
    pygame.display.flip()

pygame.quit()
