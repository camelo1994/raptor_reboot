import math

def interpolate(value,fromLow,fromHigh,toLow,toHigh):
    return ((toHigh-toLow)/(fromHigh-fromLow))*(value-fromLow)+toLow


def chk_sign(v):
    if v>0:
        return 1
    elif v<0:
        return -1

def get_speed(start,end,v_mod):
    x=end[0]-start[0]
    y=end[1]-start[1]
    if x!=0 and y!=0:
        delta_x=math.fabs(end[0]-start[0])
        delta_y=math.fabs(end[1]-start[1])
        theta=math.atan(delta_y/delta_x)
        vx=math.sqrt((v_mod**2)/(1+(math.tan(theta)**2)))
        vy=math.tan(theta)*vx
        a=(vx,vy)
    elif y==0 and x!=0:
        a=((x/v_mod),0)
    elif x==0 and y!=0:
        a=(0,(y/v_mod))
    else:
        a=(0,0)
    return (chk_sign(x)*a[0],chk_sign(y)*a[1])


def get_speed_list(list,v):
    n=len(list)-1
    speed_list=[]
    for i in range(n):
        start=(list[i][0],list[i][1])
        end=(list[i+1][0],list[i+1][1])
        speed_list.append(get_speed(start,end,v))
    return speed_list

def get_hyp(list):
    n=len(list)
    lista=[]
    for i in range(n):
        lista.append(math.hypot(list[i][0],list[i][1]))
    return lista






listpos=[(0,0),(460,200),(500,900),(750,300),(-100,-900)]

listvel=get_speed_list(listpos,10)
print(listvel)
print(get_hyp(listvel))

