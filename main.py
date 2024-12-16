from Simulation import simulation
from Draw import Vision
import numpy as np
from rich import print as rprint
from Evaluation import evaluation


def brake(car):
    car.v_x = max(np.floor(car.v_x - car.v_x / 2), 0)
    car.v_y = max(car.v_y - 22.5 / 20, 0)


def winer(per_step, tau, winer_pre):
    return np.exp(- per_step / tau)*winer_pre+np.sqrt(2*per_step/tau)*np.random.normal(0, 1)


if __name__ == "__main__":

    # 时间参数
    total_step = 1000
    second_per_step = 0.2
    total_second = total_step*second_per_step

    # 车辆参数
    brakeTime = 30
    isExecution = True
    carLength = 5  # 设置车长为5米

    # IDM参数设置
    aMax = 2.5  # 最大加速度
    bMax = 40.5  # 最大舒适减速度
    S_0 = 10  # 静止距离
    T = 2.5  # 车头时距
    V_0 = 22.5  # 期望速度(最大速度)
    V_max = 22.5

    tau = 20
    V_s = 0.01
    S = 1
    sigma_r = 0.05

    simulator = simulation()
    road = simulator.createRoad()
    eval = evaluation()
    visible = Vision()

    delta_velocity = 0
    expect_distance = 0

    min_mttc = []
    min_drac = []

    # 主循环
    for step in range(total_step):
        # 来车
        if step % 20 == 0:
            car = simulator.createVehicle(vy=V_max)
            road.append(car)
        winer_s = [0]
        winer_l = [0]
        # 自由加速
        for i, this_car in enumerate(road):
            # acceleration = ((np.random.rand() - 0.5)*2 /5)
            acceleration = 1

            if i == 0 and this_car.loc_y >= 2000 and isExecution:
                if brakeTime >= 0:
                    brake(this_car)
                    brakeTime = brakeTime - second_per_step
                    # print(brakeTime)
                else:
                    isExecution = False
            if len(road) > 1 and i > 0:
                if road[i-1].loc_y - road[i].loc_y >= carLength:
                    delta_distance = (
                        road[i-1].loc_y - road[i].loc_y - carLength)*np.exp(V_s*winer_s[-1])
                    winer_s.append(winer(per_step=second_per_step,
                                   tau=tau, winer_pre=winer_s[-1]))
                road[i-1].v_y = road[i-1].v_y - S*sigma_r*winer_l[-1]
                delta_velocity = (
                    road[i-1].v_y - road[i].v_y) + S*sigma_r*winer_l[-1]
                winer_l.append(winer(per_step=second_per_step,
                               tau=tau, winer_pre=winer_l[-1]))
                expect_distance = S_0 + \
                    max(0, road[i].v_y*T + road[i].v_y *
                        delta_velocity/(2*np.sqrt(aMax*bMax)))
                acceleration = aMax * \
                    (1-(road[i].v_y/V_0)**4 -
                     (expect_distance/delta_distance)**2)
                if np.isnan(acceleration):
                    acceleration = 0
                elif acceleration >= 0:
                    acceleration = min(aMax, acceleration)
                elif acceleration < 0:
                    acceleration = max(-bMax, acceleration)

                this_car.min_mttc.append(eval.calculate_mttc(
                    delta_velocity, acceleration, delta_distance))
                print(eval.calculate_mttc(
                    delta_velocity, acceleration, delta_distance))
                this_car.min_drac.append(eval.calculate_drac(
                    delta_velocity, delta_distance))

            # if -bMax <= acceleration <= aMax:
            this_car.update_v(time_step=second_per_step, a_y=acceleration)
            this_car.update_loc(time_step=second_per_step)
            this_car.update_trajectory(time=step*second_per_step)

    for i,car in enumerate(road):
        if len(car.min_mttc)!=0 and len(car.min_drac)!=0:
            min_mttc.append(min(car.min_mttc))
            min_drac.append(min(car.min_drac))

    print(len(min_mttc))
    print(len(min_drac))

    rprint(min_mttc)
    rprint(min_drac)

    visible.visible_speed(main_road_vehicles=road, total_time=total_second)
    visible.visible_1(main_road_vehicles=road,
                      V_max=V_max, total_time=total_second)
    visible.visible_2(min_mttc, min_drac)
