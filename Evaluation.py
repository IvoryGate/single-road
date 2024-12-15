import numpy as np


class evaluation:
    def __init__(self):
        pass

    def calculate_Eb(t_values, S, A, B, max_a):
        # 定义缩放的墨西哥帽小波函数
        def scaled_mexican_hat_wavelet(t, A, B):
            return (2 / np.sqrt(3) * np.pi**(-1/4)) * (1 - ((t - B) / A)**2) * np.exp(-((t - B) / A)**2 / 2)

        # 定义T函数，用于计算小波变换的近似积分
        def T(A, B, t_values, S):
            wavelet_values = scaled_mexican_hat_wavelet(t_values, A, B)  # 在 t_values 的时间点上评估小波函数
            product = S * wavelet_values  # 计算 S(t) 和小波函数的乘积
            integral_approximation = np.sum(product) * (t_values[1] - t_values[0])  # 乘以时间步长作为积分的近似
            return integral_approximation / np.sqrt(A)

        # 计算 E_b 的值
        product = T(A, B, t_values, S) ** 2  # 计算 T(A, B, t_values, S) 的平方
        integral_approximation = np.sum(product) * (t_values[1] - t_values[0])  # 使用矩形法近似积分
        E_b_value = (1 / max_a) * integral_approximation
        return E_b_value
    
    # 计算mttc指标
    def calculate_mttc(self, delta_v, delta_a, Sn_distance):
            return (delta_v + np.sqrt(delta_v**2 + 2 * delta_a * Sn_distance)) / delta_a

    # 计算drac指标
    def calculate_drac(self, delta_v, Sn_distance):
            return (delta_v**2) / Sn_distance
        

