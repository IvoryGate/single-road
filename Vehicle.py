import numpy as np
class Car:
    def __init__(self, lx, ly, vx, vy, ax, ay, lane, current_speed,initial_headway,v_max=float('inf'),v_min=0): #这里包含“self”和等式右边的参数
        self.loc_x = lx
        self.loc_y = ly
        self.v_x = vx
        self.v_y = vy
        self.a_x = ax
        self.a_y = ay
        self.lane = lane
        self.just_changed_lane = False
        # self.speed = speed
        self.v_max = v_max
        self.v_min = v_min
        self.speeds = []  #用于储存每个时刻的速度
        self.trajectory = []  #用于储存每个时刻的位置
        self.current_speed = current_speed #用于计算当前车的速度
        self.initial_headway = initial_headway #开始时车的间距
        self.a_y_pre = []
        self.min_mttc = []
        self.min_drac = []    


    def update_loc(self,time_step):  #函数里定义的都是形式参数，后边使用的时候需要传输
        self.loc_x += self.v_x * time_step +0.5*(self.a_x*time_step**2)
        self.loc_y += self.v_y * time_step +0.5*(self.a_y*time_step**2)

    def update_v(self, time_step, a_x=0, a_y=0):  # 矢量  a_x a_y在这里是
        self.a_x = a_x
        self.a_y = a_y
        self.v_x += self.a_x * time_step
        new_v = self.v_y + self.a_y * time_step
        # self.v_y = min(new_v,self.v_max)
        # # self.v_y = max(0, new_v)
        self.v_y = max(0, min(new_v,self.v_max))
        # print(self.v_y)
    
    def get_current_speed(self):  #标量
        return np.sqrt(np.square(self.v_x) + np.square(self.v_y)) #sqrt 开根号；square 平方
    
    def update_trajectory(self, time):
        self.trajectory.append((time, self.loc_x, self.loc_y))
        current_speed = self.get_current_speed()
        self.speeds.append((time, current_speed))
        # self.speed = current_speed  
    
