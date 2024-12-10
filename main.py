from Simulation import simulation
from Draw import Vision
import numpy as np


def brake(car):
    car.v_x = max(np.floor(car.v_x - car.v_x / 2),0)
    car.v_y = max(np.floor(car.v_y - car.v_y / 2),0)

if __name__ == "__main__":

    # 时间参数
    total_step = 1000
    second_per_step = 0.25
    total_second = total_step*second_per_step
    # 车辆参数
    V_max = 30 # 最大速度22.5m/s
    safe_distance = 80 # 两车安全距离80m
    # safe_time_headway = 
    brakeTime = 5
    isExecution = True
    carLength = 5  #设置车长为5米
    # IDM参数设置 
    aMax = 8.5
    bMax = 8.5
    S_0 = 10
    T = 1.6
    V_0 = 30
    

    simulator = simulation()
    road = simulator.createRoad()
    visible = Vision()

    # mttc = []
    # drac = []
    # 主循环
    for step in range(total_step):
        # 来车
        if step % 20 == 0:
            car = simulator.createVehicle(vy=15) 
            road.append(car)
        # 自由加速
        for i,this_car in enumerate(road):
            # acceleration = ((np.random.rand() - 0.5)*2 /5)
            acceleration = 0.2


            
            if i==0 and this_car.loc_y >= 2000 and isExecution:
                if brakeTime >= 0:
                    brake(this_car)
                    brakeTime = brakeTime - second_per_step

                    # print(brakeTime)
                else:
                    isExecution = False
            if len(road)>1 and i > 0:
                # print(road[i].loc_y)
                if road[i-1].loc_y - road[i].loc_y >= carLength+2:
                    delta_distance = road[i-1].loc_y - road[i].loc_y - carLength+2
                delta_velocity = road[i-1].v_y - road[i].v_y
                expect_distance = S_0 + max(0,road[i].v_y*T + road[i].v_y * delta_velocity/(2*np.sqrt(aMax*bMax)))
                acceleration = aMax*(1-(road[i].v_y/V_0)**4-(expect_distance/delta_distance)**2)
                

                if np.isnan(acceleration):
                    acceleration = 0
                # print((acceleration,expect_distance,delta_distance,delta_velocity))
                # print(delta_distance)
                # road[i+1].v_y = max(road[i].v_y,road[i+1].v_y-(np.abs(road[i+1].v_y-road[i].v_y))*10/11)
                # print (acceleration)
            if -bMax <= acceleration <= aMax:
                this_car.update_v(time_step=second_per_step,a_y=acceleration)
                this_car.update_loc(time_step=second_per_step)
                this_car.update_trajectory(time=step*second_per_step)
            

    #         single_car_mttc = []
    #         if delta_velocity:
    #             single_car_mttc.append(calculate_mttc(delta_a=acceleration,delta_v=delta_velocity,Sn_distance=expect_distance))
    #         else:
    #             single_car_mttc.append(calculate_mttc(delta_a=acceleration,delta_v=0,Sn_distance=expect_distance))
    #         single_car_drac = []
    #         single_car_drac.append(calculate_drac(delta_v=delta_velocity,Sn_distance=expect_distance))
    #     mttc.append(min(single_car_mttc))
    #     drac.append(min(single_car_drac))
    # min_mttc = min(mttc)
    # min_drac = min(drac)
    # print(min_mttc)
    # print(min_drac)

    visible.visible_speed(main_road_vehicles=road,total_time=total_second)
    visible.visible_1(main_road_vehicles=road,V_max=V_max,total_time=total_second)
            

        
        
