import time
import random

class MLX90614():
    def get_human_temp(self):
        time.sleep(1)
        temp = random.uniform(350,375)/10
        return float('%.1f' % temp)

if __name__ == "__main__":
    mlx = MLX90614()
    print(mlx.get_human_temp())