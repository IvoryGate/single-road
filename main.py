from Simulation import simulation
from Draw import Vision
import numpy as np


def brake(car):
    car.v_x = max(np.floor(car.v_x - car.v_x / 2),0)
    car.v_y = max(car.v_y - 22.5 / 20,0)
    
if __name__ == "__main__":

    # 时间参数
    total_step = 1000
    second_per_step = 0.2
    total_second = total_step*second_per_step

    # 车辆参数
    brakeTime = 50
    isExecution = True
    carLength = 5  #设置车长为5米

    # IDM参数设置 
    aMax = 8.5 #最大加速度
    bMax = 8.5 #最大舒适减速度
    S_0 = 10   #静止距离
    T = 2.5    #车头时距
    V_0 = 22.5 #期望速度(最大速度)
    V_max = 22.5
    
    simulator = simulation()
    road = simulator.createRoad()
    visible = Vision()

    # 主循环
    for step in range(total_step):
        # 来车
        if step % 4 == 0:
            car = simulator.createVehicle(vy=10) 
            road.append(car)
        # 自由加速
        for i,this_car in enumerate(road):
            # acceleration = ((np.random.rand() - 0.5)*2 /5)
            acceleration = 1
            
            if i==0 and this_car.loc_y >= 2000 and isExecution:
                if brakeTime >= 0:
                    brake(this_car)
                    brakeTime = brakeTime - second_per_step
                    # print(brakeTime)
                else:
                    isExecution = False
            if len(road)>1 and i > 0:
                if road[i-1].loc_y - road[i].loc_y >= carLength:
                    delta_distance = road[i-1].loc_y - road[i].loc_y - carLength
                else:
                    delta_distance = 5
                delta_velocity = road[i-1].v_y - road[i].v_y
                expect_distance = S_0 + max(0,road[i].v_y*T + road[i].v_y * delta_velocity/(2*np.sqrt(aMax*bMax)))
                acceleration = aMax*(1-(road[i].v_y/V_0)**4-(expect_distance/delta_distance)**2)
                # print(car.speeds)
                if np.isnan(acceleration):
                    acceleration = 0

            if -bMax <= acceleration <= aMax:
                this_car.update_v(time_step=second_per_step,a_y=acceleration)
                this_car.update_loc(time_step=second_per_step)
                this_car.update_trajectory(time=step*second_per_step)
            

    visible.visible_speed(main_road_vehicles=road[0:30],total_time=total_second)
    visible.visible_1(main_road_vehicles=road[0:30],V_max=V_max,total_time=total_second)
            

        
        
