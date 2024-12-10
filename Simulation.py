from Vehicle import Car

class simulation:
    def __init__(self):
        pass
    
    def createRoad(self):
        road = []
        # road = [Car(ly=0, vy=0)] + [Car(50 * i, 10) for i in range(1, 30)] 
        return road
    
    def createVehicle(self,
            # 车辆相关参数
            lx=0, ly=0, vx=0, vy=0, ax=0, ay=0, lane=0, speed=0,initial_headway = 0,v_max=22.5,v_min=0
            ):
        car = Car(lx, ly, vx, vy, ax, ay, lane, speed,initial_headway,v_max,v_min)
        return car