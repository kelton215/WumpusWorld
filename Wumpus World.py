#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#world
from random import *
import numpy as np
print("1:wumpus")
print("2:pitch")
print("3:gold")
print("5:wall")
maze=np.array([[5,5,5,5,5,5],[5,0,0,0,0,5],[5,0,0,0,0,5],[5,0,0,0,0,5],[5,0,0,0,0,5],[5,5,5,5,5,5]])#0=unknown,5=wall
g=[9,10,14,15,16,19,20,21,22,25,26,27,28]#gold위치 설정하기 위한 인덱스값
all=[9,10,14,15,16,19,20,21,22,25,26,27,28,37,38,39,40,41,42,43]#확률 0.15로 만들기위한 20개의 수
while True:
    w=np.random.choice(all,size=3,replace=True)#20개중에 wumpus와 pitch각각 세개씩 뽑음(0.15)-독립적이니까 중복 허용
    p=np.random.choice(all,size=3,replace=True)
    gold=np.random.choice(g,size=1)
    if gold==25 and 19 in p:#maze의 모서리에 3(gold)이 위치하고 그 옆 두군데에 pitch가 위치할 경우 agent는 gold에 접근할 수 없으므로 다시 세팅해야함
        if 26 in p:
            continue
    elif gold==10 and 9 in p:
        if 16 in p:
            continue
    elif gold==28 and 27 in p:
        if 22 in p:
            continue
    else:#일반적인 경우
        break

for i in range(0,3):#pitch 위치 설정
    if p[i]<=28:
        a=int(p[i]/6)#인덱스 값을 maze 배열에 넣기 위해 몫과 나머지 구함
        b=int(p[i]%6)
        maze[a][b]=2
for i in range(0,3):#wumpus 위치 설정
    if w[i]<=28:
        a=int(w[i]/6)
        b=int(w[i]%6)
        maze[a][b]=1

a=int(gold/6)
b=int(gold%6)
maze[a][b]=3#gold 위치 설정
print(maze)


# In[ ]:


#agent
x=1#프로그램을 처음 시작할때 agent는 maze[1][1]에 위치
y=1
visited=[7]#지금까지 방문한 모든 인덱스를 저장
state=[7]#maze에 지나온 경로 표시하기 위한 배열(장애물없는 확실한 경로->gold 발견 후 (1,1)로 돌아갈때 사용)
visited_pitch=[]#agent가 마주친 pitch의 인덱스를 저장하기 위한 배열
visited_wumpus=[]#agent가 마주친 wumpus의 인덱스를 저장하기 위한 배열
agent_dir=1#agent가 시작할 때 기본 방향은 동쪽
agent=maze[x][y]
i=0#무한 루프 막기위해 pitch에 도달할때마다 i에 1씩 더해서 특정 수에 도달하면 기본적으로 우회전하던 agent를 좌회전 시킴
s=3#wumpus에 shoot할 수 있는 화살 개수가 3개이니까 사용한 화살 수 세기 위해 설정
h=1#wumpus와 pitch에 의해 agent가 죽는 회수 구하기 위해 설정
maze_print=maze.copy()#maze_print를 통해 agent가 지나간 길을 표시하기 위해 maze를 복제

#agent_dir=1(동쪽 볼때), 2(남쪽 볼때), 3(서쪽 볼때), 4(북쪽 볼때)
def TurnRight():#agent가 오른쪽으로 돌게 함
    global agent_dir
    agent_dir+=1
    if agent_dir==5:
        agent_dir=1
def TurnLeft():#agent가 왼쪽으로 돌게 함
    global agent_dir
    agent_dir-=1
    if agent_dir==0:
        agent_dir=4

#agent가 움직이는 기본 방식: GoForward, TurnRight
def GoForward():#1:동쪽볼때,2:남쪽볼때,3:서쪽볼때,4:북쪽볼때
    global x,y,visited,agent,agent_dir,state
    if agent_dir==1:#agent가 동쪽을 볼때
        if maze[x][y+1]==5:#Bump(wall에 부딪힐 때)
            if i<3:#무한루프를 방지하기 위해 pitch에 2번 부딪힐때까지는 같은 경로가 반복되더라도 우회전함(다른 pitch가 주변에 있을수도있으니까)
                TurnRight()
            elif i<5:#pitch에 3~4번 부딪힐때는 무한루프를 탈출하고 gold를 탐지하기 위해 좌회전
                TurnLeft()
#            elif i<7:
#                TurnBack()
            else:#좌회전으로 인한 무한루프를 탈출하고 gold를 탐지하기 위해 다시 우회전-->이 if i<3부터 else 까지는 무한루프 탈출하기 위해서 구현한건데 완벽하게 탈출하지 못하는 경우가 생겨서 적절한 알고리즘이 아닌것같다고? 아쉽다는 식으로 말하는게 나을거같아요.
                TurnRight()
        else:#동쪽으로 향하니까
            y+=1#x값은 그대로, y값은 1더해서 다시 agent 설정
            visited.append(x*6+y)#agent가 방문한 경로 추가
            state.append(x*6+y)#장애물이 없는 확실한 경로에 추가
        agent=maze[x][y]
    elif agent_dir==2:#agent가 남쪽 볼때
        if maze[x+1][y]==5:
            if i<3:
                TurnRight()
            elif i<5:
                TurnLeft()
#            elif i<7:
#                TurnBack()
            else:
                TurnRight()
        else:
            x+=1
            visited.append(x*6+y)
            state.append(x*6+y)
        agent=maze[x][y]
    elif agent_dir==3:#agent가 서쪽 볼때
        if maze[x][y-1]==5 and (x*6+y)!=19:#여기는 무한루프 막으려고 특수상황에 agent 방향 설정
            if i<3:
                TurnRight()
            elif i<5:
                TurnLeft()
#            elif i<7:
#                TurnBack()
            else:
                TurnRight()
        elif (x*6+y)==19:
            if maze[2][2]==3 or maze[2][3]==3 or maze[2][4]==3:
                x=2
                y=1
                visited.append(13)
                state.append(13)
                agent_dir=1
        else:#일반적인 상황에
            y-=1
            visited.append(x*6+y)
            state.append(x*6+y)
        agent=maze[x][y]
    else:#agent가 북쪽볼때
        if (x*6+y)==19 and maze[4][1]==3:#무한루프 피하기 위해 특수상황에서 방향 설정
            agent_dir=2
        elif (x*6+y)==19:
            if maze[2][2]==3 or maze[2][3]==3 or maze[2][4]==3 or maze[3][2]==2:
                x=2
                y=1
                visited.append(13)
                state.append(13)
                agent_dir=1
            elif maze[3][2]==3 or maze[3][3]==3 or maze[3][4]==3:
                if maze[3][2]==2:
                    agent_dir=4
                else:
                    agent_dir=1
        if (x*6+y)==14:#여기까지 무한루프피하기위한 방향 설정
            agent_dir=1
        elif maze[x-1][y]==5:#Bump
            if i<3:
                TurnRight()
            elif i<5:
                TurnLeft()
#            elif i<7:
#                TurnBack()
            else:
                TurnRight()
        else:
            x-=1
            visited.append(x*6+y)
            state.append(x*6+y)
        agent=maze[x][y]
        
def Shoot():#wumpus만났을 때 shoot하기 위한 함수
    global agent,maze,x,y
    if agent_dir==1:#동쪽볼때
        maze[x][y+1]=0#동쪽으로 한칸 전진
        visited.append(x*6+y)#방문한 경로에 인덱스 값 추가
        y+=1#동쪽으로 한칸 추가
        visited.append(x*6+y)
    elif agent_dir==2:
        maze[x+1][y]=0
        visited.append(x*6+y)
        x+=1
        visited.append(x*6+y)
    elif agent_dir==3:
        maze[x][y-1]=0
        visited.append(x*6+y)
        y-=1
        visited.append(x*6+y)
    else:
        maze[x-1][y]=0
        visited.append(x*6+y)
        x-=1
        visited.append(x*6+y)

def End():#wumpus, pitch에 걸리면 죽고 처음으로 돌아감
    global agent,visited,last,x,y
    last=visited[-2]#agent가 죽기 전 칸(장애물 없이 안전한 마지막칸)
    x=int(last/6)
    y=int(last%6)
    agent=maze[x][y]
    visited.append(x*6+y)

while True:
    if maze[x][y]==0:#장애물 없으면
        GoForward()
        
    elif maze[x][y]==3:#gold발견
        for k in range(0,len(state)):#maze_print로 agent 움직인 경로 표기하기 위해
            a=int(state[k]/6)
            b=int(state[k]%6)
            maze_print[a][b]=9
        print(h,"번째 시도:",state)#알아보기 쉽게 지금까지 지나온 모든 경로 인덱스값 표시,,
        a=int(state[-1]/6)
        b=int(state[-1]%6)
        maze_print[a][b]=8#gold를 찾았다는 의미(gold를 발견 시 3에서 8로 변경)
        print("!GOLD!")
        print(maze_print)
        print("==================")
        break
        
    elif maze[x][y]==1:#wumpus 마주침
        visited_wumpus.append(x*6+y)
        print(h,"번째 시도:",state)
        print("!DIE!(wumpus)")
        h+=1#죽은 회수 추가
        print(h,"번째 시도:",state[0:len(state)-1])
        a=int(state[-1]/6)
        b=int(state[-1]%6)
        print("[",a,"]","[",b,"]""!SCREAM!")
        s-=1#화살 하나 감소
        print("남은 화살 개수:",s)
        print("전진->",state)#wumpus를 shoot한 후 그 칸으로 전진
        h-=1
        for k in range(0,len(state)):
            a=int(state[k]/6)
            b=int(state[k]%6)
            maze_print[a][b]=9
        print(maze_print)
        print("===================")
        End()#agent가 wumpus만나서 죽음
        if s>=0:#화살 개수 3개 제한이니까
            Shoot()
            GoForward()
            h+=1#agent가 몇번째 죽었는지 표시하기 위해 죽으면 변수 h에 1 추가
        continue
        
    elif maze[x][y]==2:#pitch 마주침
        i+=1#무한루프 방지하기 위해 pitch 마주칠 때마다 변수 i 에 1추가
        visited_pitch.append(x*6+y)
        if len(visited_pitch)>1:
            for k in range(0,len(visited_pitch)-1):
                if visited_pitch[-1]==visited_pitch[k]:
                    visited_pitch.pop()
            
        c=int(state[-1]/6)
        d=int(state[-1]%6)
        print(h,"번째 시도:",state)
        for k in range(0,len(state)):
            a=int(state[k]/6)
            b=int(state[k]%6)
            maze_print[a][b]=9
        print(maze_print)
        print("!DIE!(pitch)")
        print("====================")
        state.pop(-1)
        maze_print[c][d]=2
        End()#agent가 pitch에 의해 죽음
        if i<3:#무한루프 방지하기 위해 pitch를 반복해서 만나면 방향을 틀어 진행-->이거만으로는 무한루프발생하는 배열에 대해서 완벽히 대처 못하니까 발표할때 여기는 완벽히 구현못해서 아쉽다고 하던가 무한루프를 해결할 다른 알고리즘을 생각해내지 못했다는 식으로 말해야될것같아요 그리고 이 식 때문에 다음 시도 때에도 경로가 반복되는 경우가 있어서 그것도 아쉬운 점으로  
            TurnRight()
        elif i<5:
            TurnLeft()
        else:
            TurnRight()
        GoForward()
        h+=1
        continue
for k in range(0,len(state)):#gold 발견 후 (1,1)로 돌아가는 climb경로 출력
    a=int(state[k]/6)
    b=int(state[k]%6)
    maze_print[a][b]=8
    
print("!EXIT!",state[::-1])
print(maze_print)#agent가 지나간 경로는 9로 표시, gold 발견하면 8로 표시하고 안전한 경로로 다시 돌아오는 길은 8로 표시
print("agent가 마주친 wumpus:",visited_wumpus)
print("agent가 마주친 pitch:",visited_pitch)

