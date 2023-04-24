import math
from tabulate import tabulate
import matplotlib.pyplot as plt
import numpy as np

G = 9.80665

CLUBHEADTOBALL = {
    "driver": 1.477876,
    "3wood": 1.476636,
    "5wood": 1.475728,
    "hybrid": 1.460112,
    "2iron": 1.454545,
    "3iron": 1.448980,
    "4iron": 1.427083,
    "5iron": 1.404255,
    "6iron": 1.3840435,
    "7iron": 1.333333,
    "8iron": 1.321839,
    "9iron": 1.2822353,
    "pw": 1.228916,
    "gw": 1.222222,
    "sw": 1.157895,
}

CLUBLOFT = {
    "driver": 10.5,
    "3wood": 15,
    "5wood": 18,
    "hybrid": 21,
    "2iron": 16,
    "3iron": 21,
    "4iron": 24,
    "5iron": 27,
    "6iron": 30,
    "7iron": 34,
    "8iron": 38,
    "9iron": 42,
    "pw": 46,
    "gw": 51,
    "sw": 54,
}

DISTMULTIPLIER_CH = 3.16
DISTMULTIPLIER_BS = 2.04

CLUB_MASS = 0

TIME_PER_DATA_POLL = 0.038


"""
? DATA FORMAT:
[     0]   -993 -> angular x
[     1]   -580 -> angular y
[     2]  -1153 -> angular z
[     3]  -2734 -> linear x
[     4]    503 -> linear y
[     5]   1561 -> linear z

[     0]   -381
[     1]   -790
[     2]    437
[     3]   -224
[     4]   1391
[     5]   1181

[     0]    183
[     1]   -187
[     2]    610
[     3]   -216
[     4]   1327
[     5]   1402

Data comes in as a list of 6 values, the first three being the angular (x, y, z) acceleration (dps -> degrees per second) of the club, and the last three being the linear (x, y, z) acceleration (g) of the club.


* linear_accel = [data[i::3] for i in range(3)]

data = [
 -794,
 -222,
   57,
 -107,
 1301,
 1486,
 -759,
 -343,
  -23,
  -73,
 1245,
 1706,
 -667,
 -397,
  -92,
  -63,
 1197,
 1861,
 -553,
 -376,
 -108,
  -67,
 1171,
 1916,
 -471,
 -310,
  -92,
  -65,
 1135,
 1866,
 -461,
 -211,
  -60,
  -63,
 1090,
 1861
]

data2 = [
 -381,
 -790,
  437,
 -224,
 1391,
 1181,
 -765,
  -86,
  286,
 -187,
 1384,
 1259,
 -755,
  -64,
  136,
 -158,
 1351,
 1342
]
"""


def process_data(data):
    temp = [
        -794,
        -222,
        57,
        -107,
        1301,
        1486,
        -759,
        -343,
        -23,
        -73,
        1245,
        1706,
        -667,
        -397,
        -92,
        -63,
        1197,
        1861,
        -553,
        -376,
        -108,
        -67,
        1171,
        1916,
        -471,
        -310,
        -92,
        -65,
        1135,
        1866,
        -461,
        -211,
        -60,
        -63,
        1090,
        1861
    ]

    data_length = len(data)
    len_sensor_data = data_length // 3
    sensor_one = data[0:len_sensor_data]
    sensor_two = data[len_sensor_data - 1:len_sensor_data * 2]
    sensor_three = data[len_sensor_data * 2 - 1:len_sensor_data * 3]

    linear_accel = [sensor_one[i:i+3]
                    for i in range(0, len(sensor_one), 3)][1::2]
    angular_accel = [sensor_one[i:i+3]
                     for i in range(0, len(sensor_one), 3)][::2]
    # print(f'linear_accel: {linear_accel}\n angular_accel: {angular_accel}')
    linear_accel_x = _get_gs([x[0] for x in linear_accel])
    angular_accel_x = _get_dps([x[0] for x in angular_accel])
    linear_accel_y = _get_gs([x[1] for x in linear_accel])
    angular_accel_y = _get_dps([x[1] for x in angular_accel])
    linear_accel_z = _get_gs([x[2] for x in linear_accel])
    angular_accel_z = _get_dps([x[2] for x in angular_accel])

    direction = ['' for i in range(len(linear_accel_x))]
    for j, accel in enumerate(angular_accel):
        highestAccel = 0
        for i in range(len(accel)):
            if abs(accel[i]) > highestAccel and i == 0:
                if accel[i] > 0:
                    direction[j] = '+x'
                else:
                    direction[j] = '-x'
                highestAccel = abs(accel[i])
            elif abs(accel[i]) > highestAccel and i == 1:
                if accel[i] > 0:
                    direction[j] = '+y'
                else:
                    direction[j] = '-y'
                highestAccel = abs(accel[i])
            elif abs(accel[i]) > highestAccel and i == 2:
                if accel[i] > 0:
                    direction[j] = '+z'
                else:
                    direction[j] = '-z'
                highestAccel = abs(accel[i])

    total_accel = [math.sqrt(i**2 + j**2 + k**2) for i, j,
                   k in zip(linear_accel_x, linear_accel_y, linear_accel_z)]

    total_angular_accel = [math.sqrt(i**2 + j**2 + k**2) for i, j,
                           k in zip(angular_accel_x, angular_accel_y, angular_accel_z)]
    total_linear_accel = [math.sqrt(i**2 + j**2 + k**2) for i, j,
                          k in zip(linear_accel_x, linear_accel_y, linear_accel_z)]

    total_accel = (_convert_from_g(total_accel))
    total_linear_accel = (_convert_from_g(total_linear_accel))
    #linear_accel_z = high_pass_filter(linear_accel_z, 0.1)
    #linear_accel_z = (_convert_from_g(linear_accel_z))
    #linear_accel_z = (_convert_from_g(linear_accel_z))

    return linear_accel, angular_accel, linear_accel_x, linear_accel_y, linear_accel_z, angular_accel_x, angular_accel_y, angular_accel_z, direction, total_accel, total_angular_accel, total_linear_accel

def high_pass_filter(data, alpha_coefficient):
        #yn = [data[0]]
        filtered_data = [0] * len(data)
        filtered_data[0] = data[0]
        filtered_data[1] = data[1]
        
        for i in range(2, len(data)):
            filtered_data[i] = (alpha_coefficient * (filtered_data[i-1] + data[i] - data[i-1]))

        return filtered_data 

def get_club_head_speed(linear_z, total_accel):
    velo_f = 0

    time_list = [i * TIME_PER_DATA_POLL for i in range(len(total_accel))]

    linear_z_dir = list(filter(lambda x: x < 0, linear_z[2:]))
    #linear_z_dir = list(filter(lambda x: x > 0, linear_z[2:]))

    len_linear_z_dir = len(linear_z_dir) if len(linear_z_dir) > 0 else 1
    time = TIME_PER_DATA_POLL * len_linear_z_dir
    len_linear_z_velo = (sum(linear_z_dir) / len_linear_z_dir) / time
    print(f'len_linear_z_velo: {len_linear_z_velo}')

    velo_i = [0 for i in range(len(linear_z))]
    velo_f = []
    print(linear_z)
    for i in range(len(linear_z)):
        if i == 0:
            velo_f.append(linear_z[i] * TIME_PER_DATA_POLL)
        else:
            velo_i[i] = velo_f[i-1]
            # velo_f.append(velo_i[i] + ((linear_z[i] - 10) * TIME_PER_DATA_POLL))
            velo_f.append(velo_i[i] + (linear_z[i] * TIME_PER_DATA_POLL))
    # velo_f = _convert_from_g(linear_z)

    # velo_f = [(total_accel[i])
    #           * TIME_PER_DATA_POLL for i in range(len(total_accel))]

    position = [i / 2 + TIME_PER_DATA_POLL for i in velo_f]
    position_sum = [sum(position[2:i]) for i in range(len(position) - 2)]

    velo_f_mph = [x * 2.23694 for x in velo_f]

    v_len = len(velo_f_mph) if len(velo_f_mph) > 0 else 1

    final_velo = sum(velo_f_mph) / v_len

    # ! NEED TO ENSURE CORRECT UNITS
    return velo_f, velo_f_mph, final_velo, position_sum


def get_ball_speed(club, club_head_speed):
    return club_head_speed * CLUBHEADTOBALL[club]


def get_ball_distance(club_head_speed, ball_speed):
    dist_from_head_speed = club_head_speed * DISTMULTIPLIER_CH - 85.2
    dist_from_ball_speed = ball_speed * DISTMULTIPLIER_BS - 65.2

    # dist_from_head_speed = 0 if dist_from_head_speed < 0 else dist_from_head_speed
    # dist_from_ball_speed = 0 if dist_from_ball_speed < 0 else dist_from_ball_speed

    error = (dist_from_head_speed - dist_from_ball_speed)

    # TODO: Fix this
    return (dist_from_head_speed + dist_from_ball_speed) / 2


def get_smash_factor(club_head_speed, ball_speed):
    return ball_speed / club_head_speed


def get_launch_angle(club, angle):
    pass


def get_club_face_angle(anglur_accel):
    pass


def _convert_from_g(data):
    return [round(i * G, 2) for i in data]


def _get_gs(data):
    #return [(i / 32678) * 8 for i in data]
    return [(i / 32678) * 2 for i in data]
    #return [(i * 0.244) / 1000 for i in data]


def _get_dps(data):
    return [(i * 8.75) / 1000 for i in data]


def plot_acceleration(linear_accel, angular_accel, position, linear_velo):
    data_len = len(linear_accel)
    time = [i * TIME_PER_DATA_POLL for i in range(data_len - 2)]
    fig, axs = plt.subplots(2, 2)
    # plot the linear acceleration
    axs[0, 0].plot(time, linear_accel[2:])
    axs[0, 0].scatter(time, linear_accel[2:])

    # plot the angular acceleration
    axs[0, 1].plot(time, angular_accel[2:])
    axs[0, 1].scatter(time, angular_accel[2:])

    # plot the position
    position_time = [i * TIME_PER_DATA_POLL for i in range(len(position))]
    axs[1, 0].plot(position_time, position)
    axs[1, 0].scatter(position_time, position)

    # plot the linear velocity
    axs[1, 1].plot(time[1:], linear_velo[2:])
    axs[1, 1].scatter(time[1:], linear_velo[2:])

    # set the titles
    axs[0, 0].set_title('Linear Acceleration vs Time')
    axs[0, 1].set_title('Angular Acceleration vs Time')
    axs[1, 0].set_title('Position vs Time')
    axs[1, 1].set_title('Linear Velocity vs Time')

    # set the x and y labels
    axs[0, 0].set(xlabel='Time (s)', ylabel='Linear Acceleration (m/s^2)')
    axs[0, 1].set(xlabel='Time (s)',
                  ylabel='Angular Acceleration (degrees/s^2)')
    axs[1, 0].set(xlabel='Time (s)', ylabel='Position (m)')
    axs[1, 1].set(xlabel='Time (s)', ylabel='Linear Velocity (m/s)')

    # set the tight layout
    plt.tight_layout()

    # show the plot
    plt.show()

def get_inst_velocity(filtered_z):
    vel_data = np.zeros_like(filtered_z)
    
    for i in range (3, len(vel_data)):
        vel_data[i] = vel_data[i-1] + 0.5 * TIME_PER_DATA_POLL * (filtered_z[i-1] + filtered_z[i])
    #for i in range(1, len(filtered_z)):
    #    trapezoid_area = (filtered_z[i] + filtered_z[i-1]) / 2 * TIME_PER_DATA_POLL
    #    vel_data[i] = vel_data[i-1] + trapezoid_area
        
    return vel_data

def getRotationMatrix(yaw, roll, pitch):

    #rotation matrix for yaw angle
    R_Yaw = np.array([[np.cos(yaw), -np.sin(yaw), 0],
                  [np.sin(yaw), np.cos(yaw), 0],
                  [0, 0, 1]])
    
    #rotation matrix for roll angle
    R_Roll = np.array([[1, 0, 0],
                  [0, np.cos(roll), -np.sin(roll)],
                  [0, np.sin(roll), np.cos(roll)]])

    #rotation matrix for pitch angle
    R_Pitch = np.array([[np.cos(pitch), 0, np.sin(pitch)],
                  [0, 1, 0],
                  [-np.sin(pitch), 0, np.cos(pitch)]])
    
    return np.matmul(np.matmul(R_Yaw, R_Pitch), R_Roll)

def velocity_calc(acc, av):

    gravity_vector = [acc[0][0], acc[1][0], acc[2][0]]
    
    normalizedArr = []

    for i in range(1, len(acc[0])):
        #retreive data at ith index
        linearPoint = [acc[0][i], acc[1][i], acc[2][i]]
        
        #retreive difference in angular velocity between current point and i-1
        angularPoint = [av[0][i] + av[0][i-1], av[1][i] + av[1][i-1], av[2][i] + av[2][i-1]]
        
        #calculate yaw, roll, pitch from angularPoint 
        yaw_delta_theta = (0.5) * (angularPoint[2]) * TIME_PER_DATA_POLL     
        pitch_delta_theta = (0.5) * (angularPoint[1]) * TIME_PER_DATA_POLL     
        roll_delta_theta = (0.5) * (angularPoint[0]) * TIME_PER_DATA_POLL     
        
        rotationMatrix = getRotationMatrix(yaw_delta_theta, roll_delta_theta, pitch_delta_theta)

        gravity_vector = np.matmul(rotationMatrix, np.array(gravity_vector).T).T
        
        normalizedArr.append(linearPoint - gravity_vector)

    normalizedArr = [data.tolist() for data in normalizedArr]
    #return normalizedArr
    return [x[0] for x in normalizedArr], [x[1] for x in normalizedArr], [x[2] for x in normalizedArr]


    '''acceleration_earth = np.matmul(R, np.array(acc).reshape(-1, 3).T).T
    angular_velocity_earth = np.matmul(R, np.array(av).reshape(-1, 3).T).T
    
    dt = TIME_PER_DATA_POLL
    velocity = np.zeros_like(acceleration_earth)
    for i in range(1, acceleration_earth.shape[0]):
        # Integrate acceleration
        velocity[i] = velocity[i-1] + acceleration_earth[i] * dt
        
        # Integrate angular velocity
        angle_change = angular_velocity_earth[i] * dt
        R = np.array([[np.cos(angle_change[2]), -np.sin(angle_change[2]), 0],
                      [np.sin(angle_change[2]), np.cos(angle_change[2]), 0],
                      [0, 0, 1]])
        #velocity[i] = np.matmul(R, velocity[i])
        #velocity[i] = np.matmul(R, velocity[i].reshape(3,1)).flatten()
        velocity[i] = np.matmul(R, velocity[i].reshape(3, 1)).flatten()'''

        
    # return velocity

if __name__ == "__main__":
    #content = []
    #with open("data.txt", "rb") as f:
    #    bytes = f.read(2)
    #    while bytes:
    #        content.append(int.from_bytes(bytes, "little", signed = False))
    #        bytes = f.read(2)

    #print(content)
    #f.close()
    #data array below is club not moving
    #data below is club "top of backswing" to bottom then stop
    data = [100, -6123, 1428, 975, 1763, -138, -17881, -22686, -20469, 3275, -32193, -679, -132, 397, 87, 2000, 3488, -330, 141, -4703, 866, 1991, 3503, -283, 224, -1374, 196, 1925, 3586, -239, -51, -388, 154, 1903, 3535, -339, 92, 889, -272, 1931, 3593, -80, 209, -28, -96, 1965, 3616, -144, -150, 1391, -228, 1936, 3371, 121, -82, 1510, -262, 1919, 3417, 17, -517, 1534, -541, 1921, 3519, 435, -317, 1132, -381, 1942, 3484, 253, -1141, 818, -829, 2025, 3607, 934, -651, 1031, -724, 1965, 3568, 669, -2444, -732, -513, 2093, 3695, 1624, -1793, 461, -785, 2073, 3647, 1248, -5054, -523, -187, 2332, 4007, 2488, -3596, -1026, -185, 2236, 3810, 2062, -8374, -1458, 370, 2505, 4458, 3137, -6611, -794, -9, 2345, 4231, 2855, -13069, 990, 633, 2662, 5111, 3785, -10745, -733, 590, 2557, 4715, 3497, -16796, 1266, 228, 2818, 5786, 3776, -14871, 881, 423, 2850, 5566, 3872, -19605, -2316, 2029, 2927, 6168, 3709, -18362, -1722, 866, 2882, 5904, 3688, -21059, -5708, 4688, 2827, 5940, 3045, -20283, -4197, 3426, 2887, 6256, 3396, -20677, -2238, 5653, 2395, 4888, 2507, -21216, -5133, 5679, 2661, 5420, 2860, -17581, -1124, 4546, 1991, 3633, 1736, -19471, -622, 5107, 2135, 4278, 2092, -14885, -1367, 3999, 1607, 2317, 960, -15988, -1585, 4176, 1770, 3006, 1377, -11872, -1971, 3296, 1490, 1140, 604, -13574, -3047, 3884, 1600, 1653, 734, -8057, -2130, 1297, 1383, 236, -84, -10223, -180, 2358, 1361, 696, 169, -4357, -47, -486, 1360, -408, -404, -6071, -988, 266, 1342, -127, -181, -515, -1086, -1927, 1553, -651, -386, -2301, -2488, -1174, 1472, -574, -400, 3246, -2198, -3204, 1839, -494, -358, 1275, -1224, -2601, 1689, -650, -475, 6765, -2522, -4186, 1990, 204, -502, 5004, -747, -3785, 1944, -238, -372, 9697, -3841, -4816, 2050, 1446, -423, 8259, -4074, -4438, 1993, 775, -416, 13033, -2238, -6623, 2150, 3062, -332, 11359, -4437, -5665, 2139, 2213, -274, 16434, -2493, -9696, 2441, 5120, 45, 15277, -7105, -7855, 2267, 4104, -303, 20747, -1307, -10928, 2636, 7228, 278, 18567, -362, -10396, 2335, 6070, 139, 24773, 407, -11780, 2745, 9004, 1131, 22182, 712, -12132, 2819, 8256, 778, 26784, 3928, -11852, 2506, 10380, 1260, 25526, 4946, -12004, 2649, 9702, 1240, 25666, 12146, -10384, 2493, 10306, 1802, 26786, 2347, -11927, 2511, 10631, 1720, 24469, 4694, -5904, 2267, 9873, 766, 24840, 12837, -7572, 2417, 10033, 828, 23749, 6546, -5144, 2350, 8657, 696, 23910, 5727, -5688, 2393, 9404, 970, 23235, 515, -3272, 2895, 7135, 816, 23668, 3001, -3694, 2566, 8031, 555, 19252, 3390, -1033, 2794, 4995, 431, 21799, 3276, -2397, 2848, 6061, 566, 15174, 2986, 1408, 2398, 2881, -29, 17067, 6546, 385, 2753, 3786, 411, 10516, 497, 1825, 2058, 1523, -489, 13031, 921, 2033, 2158, 2186, -215, 6487, -326, 1194, 1733, 569, -857, 8460, -967, 1535, 1787, 935, -662, 3482, 113, 345, 1614, 294, -1243, 4863, -412, 720, 1678, 406, -1028, 951, -948, 107, 1525, 181, -1585, 2116, -636, 89, 1592, 214, -1434, -1315, -1263, -180, 1381, 204, -1906, -291, -812, 39, 1434, 210, -1809, -3106, -1281, -1139, 1323, 299, -2171, -2136, -1308, -585, 1373, 210, -1985, -4758, 1761, -1916, 1289, 738, -2100, -4029, -957, -1560, 1267, 480, -2129, -6138, 3185, -3207, 1388, 1441, -2026, -5447, 2472, -2503, 1378, 985, -2136, -7225, 3893, -4983, 1714, 2220, -2197, -7036, 5403, -3951, 1527, 1909, -1965, -8027, 11363, -4798, 2304, 2773, -1500, -7571, 2750, -4946, 1846, 2479, -1721, -8888, 9424, -5782, 3104, 2954, -1669, -8848, 13578, -5668, 2705, 2986, -1899, -9874, 1684, -4785, 3269, 3055, -1242, -9356, 6455, -5747, 3358, 2936, -1565, -12439, 4150, -3430, 3173, 3567, -798, -10764, 834, -3538, 3302, 3215, -880, -13444, 1395, -3845, 2946, 4346, -1171, -13468, 5524, -3562, 2970, 4108, -941, -12253, -2298, -3360, 2728, 4389, -1320, -12972, -1858, -4006, 2775, 4352, -1254, -10147, -1346, -2321, 2582, 4520, -1874, -11370, -1796, -2813, 2714, 4510, -1519, -5892, -8791, -2195, 2492, 4074, -1934, -8162, -5611, -1981, 2809, 4222, -2031, -3219, -3496, -1164, 2221, 3746, -1701, -4613, -4948, -1643, 2010, 4024, -1874, 3571, -5756, -704, 276, 594, -1910, 24447, 18138, 26173, 26269, -14357, -27991, 85, 430, -80, 491, 1088, -3859, 2433, -4538, -1026, 507, 1113, -3872, 160, -1480, 1688, 434, 1181, -3915, 317, 555, -353, 337, 1169, -3812, 7, 1770, -1979, 839, 1286, -3796, -211, -1237, 1375, 932, 1268, -3873, -459, 389, 122, 770, 1160, -3618, -309, 1218, -1137, 520, 1150, -3686, -918, 627, 166, 1044, 1339, -3655, -397, 1248, -929, 924, 1267, -3716, -1319, 962, 494, 1294, 1462, -3642, -1000, 815, 10, 1264, 1414, -3628, -1715, -62, 3554, 1747, 1667, -3499, -1601, 312, 1962, 1471, 1545, -3576, -2284, 1263, 5886, 2561, 1821, -3709, -1838, 294, 4874, 2132, 1685, -3616, -2775, 4249, 7879, 3032, 2047, -3892, -2526, 2940, 6480, 2835, 2046, -3690, -3951, 7172, 11258, 3632, 2324, -4282, -3164, 5703, 9237, 3178, 2138, -4067, -4591, 13240, 9847, 3798, 2567, -4585, -4221, 9380, 11231, 4162, 2425, -4596, -4326, 8741, 19106, 3626, 2537, -4517, -4636, 12773, 12559, 3150, 2488, -4573, -1580, 14176, 15786, 3212, 2151, -4400, -2597, 11861, 17565, 4065, 2603, -4393, -1149, 11499, 18652, 4055, 1663, -3541, -1903, 9424, 21774, 3243, 1696, -4112, -1265, 14450, 10994, 2548, 1106, -3007, -730, 15904, 11886, 3602, 1536, -3194, -1339, 11431, 10209, 1971, 510, -1921, -1748, 10570, 12926, 2174, 833, -2440, -1765, 5070, 12235, 1725, -317, -1469, -1243, 9778, 9356, 1421, -87, -1825, -1537, 8043, 2485, 913, -936, -1222, -1237, 8442, 5713, 1905, -459, -1148, -1947, 2984, 1816, 1127, -1223, -637, -2703, 1613, 6475, 846, -1100, -896, -2404, -3421, 2947, 959, -1532, -749, -1630, 1361, 332, 576, -1485, -852, -1486, -4355, -2129, 869, -1559, -1054, -1403, -1318, -2717, 1139, -1544, -737, -248, -4658, -7187, 786, -1145, -1484, -1504, -5879, -3086, 1236, -1381, -1143, -428, -12429, -3444, 1110, -301, -2403, -237, -9610, -4077, 458, -818, -2024, -293, -11434, -10239, 1372, 602, -3490, -254, -11987, -6860, 1585, 196, -2884, -2988, -20959, -6016, 2185, 1827, -4844, 479, -15125, -10085, 987, 1003, -4575, -524, -12903, -20214, 1905, 2526, -6196, -
        1687, -14502, -16925, 2841, 2391, -4874, -3077, -24251, -13280, 3739, 3946, -6656, -1316, -21659, -15974, 1913, 3499, -6586, 597, -13496, -26923, 1650, 4162, -7250, -1116, -12065, -29050, 3589, 3973, -6859, -1908, -15430, -20296, 3649, 4713, -6362, 388, -22178, -19883, 1905, 4667, -7392, 8462, -8524, -23138, -1090, 3197, -7999, 5960, 4673, -32356, 1967, 3474, -6691, 3678, -16802, -17523, 3288, 3837, -5593, 3467, -26279, -5660, 1006, 3940, -7200, 6968, -16643, -12831, 119, 1682, -5940, 8317, -3642, -28655, 1173, 2463, -5866, 7364, -6442, -18419, 888, 781, -4012, 5883, -14900, -12765, 1269, 1515, -4791, 8172, -4101, -13924, -536, -441, -3242, 7084, -5310, -14891, 321, 15, -3560, 5946, -4557, -7246, -419, -1025, -2542, 6399, -7759, -5279, -613, -726, -2937, 3517, -3515, -3205, -691, -1336, -1994, 4374, -4789, -3769, -796, -1263, -2189, 1622, -252, -3121, -906, -1512, -1891, 2382, -2272, -2621, -672, -1426, -1970, 23, -1010, 1059, -1341, -1552, -1900, 982, 58, -2091, -1402, -1523, -1863, -1198, 392, 1768, -1556, -1575, -1956, -189, 1011, -251, -1358, -1577, -1953, -2490, 2730, 626, -1652, -1544, -2138, -1966, 632, 2340, -1355, -1609, -2013, -4421, 4329, 897, -1085, -1147, -2323, -3831, 1141, 3628, -1527, -1318, -2242, -6338, 5373, 667, -1415, -703, -3103, -4898, 6293, -1042, -1423, -980, -2679, -6874, 8466, -3516, -1469, -330, -3583, -7269, 5815, 623, -773, -596, -3453, -8734, 11596, -2925, 1006, -292, -3990, -8666, 2464, 4847, -905, -142, -3622, -9923, 9483, -1702, -1891, -1171, -5073, -7118, 22391, -16769, -675, -633, -4628, -8779, 3885, 6724, 366, -295, -4092, -10113, 1671, 6591, -575, -825, -4450, -8995, 11252, 2683, 306, 199, -4752, -8377, 8699, 3580, 552, -271, -4523, -9599, 6013, 7127, -322, 339, -5147, -9303, 11409, 2541, -37, 401, -5048, -7832, 5875, 6967, 616, 918, -4602, -9493, 2245, 11205, 217, 669, -4721, -6436, 2873, 7274, -467, 567, -5096, -6501, 7323, 3478, -80, 887, -5065, -4836, -5264, 11175, 265, 892, -4581, -4671, -2471, 9247, -337, 502, -4891, -2377, -490, 3312, -210, 746, -4309, -2663, 1291, 2327, 241, 911, -4224, 1815, -4643, 674, 496, 1990, -405, -20026, -2597, -1424, 18770, -11225, -26853, 2395, -5705, 449, 1059, 3969, -781, 1815, -4643, 674, 496, 1990, -405, -138, 19, 141, 1031, 3939, -760, 2395, -5705, 449, 1059, 3969, -781, 19, -177, 207, 920, 3962, -755, -138, 19, 141, 1031, 3939, -760, 454, -1878, 174, 1026, 4055, -661, 19, -177, 207, 920, 3962, -755, -257, 168, 97, 1127, 4133, -540, 454, -1878, 174, 1026, 4055, -661, -882, 2139, -114, 1030, 4083, -555, -257, 168, 97, 1127, 4133, -540, -785, 1601, -290, 974, 3885, -538, -882, 2139, -114, 1030, 4083, -555, -930, 1411, -340, 1042, 3869, -440, -785, 1601, -290, 974, 3885, -538, -967, 1034, -391, 1078, 4006, -310, -930, 1411, -340, 1042, 3869, -440, -1393, 1246, -557, 1063, 4050, -177, -967, 1034, -391, 1078, 4006, -310, -1635, 620, -563, 1051, 4098, -78, -1393, 1246, -557, 1063, 4050, -177, -2057, 329, -570, 1019, 4124, 68, -1635, 620, -563, 1051, 4098, -78, -2624, -215, -423, 953, 4139, 245, -2057, 329, -570, 1019, 4124, 68, -3198, -1588, -169, 915, 4169, 422, -2624, -215, -423, 953, 4139, 245, -4223, -2155, 79, 1062, 4291, 680, -3198, -1588, -169, 915, 4169, 422, -5715, -2113, 383, 1178, 4478, 946, -4223, -2155, 79, 1062, 4291, 680, -7214, -2813, 597, 1106, 4596, 1131, -5715, -2113, 383, 1178, 4478, 946, -8809, -3876, 918, 1203, 4685, 1281, -7214, -2813, 597, 1106, 4596, 1131, -10984, -3233, 1215, 1400, 4834, 1541, -8809, -3876, 918, 1203, 4685, 1281, -13568, -1921, 1106, 1469, 5062, 1880, -10984, -3233, 1215, 1400, 4834, 1541, -15488, -2410, 1161, 1574, 5270, 2123, -13568, -1921, 1106, 1469, 5062, 1880, -17080, -2385, 1244, 1382, 5138, 2083, -15488, -2410, 1161, 1574, 5270, 2123, -17444, -5874, 1852, 1120, 4903, 2193, -17080, -2385, 1244, 1382, 5138, 2083, -18457, -6909, 2816, 1146, 4948, 2521, -17444, -5874, 1852, 1120, 4903, 2193, -18470, -9167, 3772, 1244, 4844, 2451, -18457, -6909, 2816, 1146, 4948, 2521, -18218, -10257, 4875, 1481, 4416, 2411, -18470, -9167, 3772, 1244, 4844, 2451, -18708, -8604, 5506, 1869, 3999, 2856, -18218, -10257, 4875, 1481, 4416, 2411, -20015, -2911, 5326, 1964, 3726, 3121, -18708, -8604, 5506, 1869, 3999, 2856, -18965, -2626, 4357, 1698, 3360, 2966, -20015, -2911, 5326, 1964, 3726, 3121, -17071, -4385, 3893, 1563, 2901, 2757, -18965, -2626, 4357, 1698, 3360, 2966, -15353, -4760, 3585, 1481, 2419, 2326, -17071, -4385, 3893, 1563, 2901, 2757, -13922, -4057, 3296, 1418, 1831, 1859, -15353, -4760, 3585, 1481, 2419, 2326, -11932, -5232, 3084, 1674, 1449, 1855, -13922, -4057, 3296, 1418, 1831, 1859, -10916, -3771, 2462, 1923, 1297, 1971, -11932, -5232, 3084, 1674, 1449, 1855, -9426, -2182, 1568, 1993, 1047, 1711, -10916, -3771, 2462, 1923, 1297, 1971, -6770, -3736, 819, 2068, 740, 1529, -9426, -2182, 1568, 1993, 1047, 1711, -5675, -1673, 7, 1997, 477, 1374, -6770, -3736, 819, 2068, 740, 1529, -3774, -1167, -674, 1991, 263, 1162, -5675, -1673, 7, 1997, 477, 1374, -1153, -2809, -1097, 2114, 192, 1249, -3774, -1167, -674, 1991, 263, 1162, -82, -518, -1685, 2225, 172, 1230, -1153, -2809, -1097, 2114, 192, 1249, 2276, -1112, -2207, 2262, 181, 1186, -82, -518, -1685, 2225, 172, 1230, 4152, -990, -2638, 2315, 318, 1293, 2276, -1112, -2207, 2262, 181, 1186, 5535, 378, -3076, 2286, 497, 1106, 4152, -990, -2638, 2315, 318, 1293, 8015, -1476, -3195, 2068, 789, 861, 5535, 378, -3076, 2286, 497, 1106, 9810, -1732, -3456, 2016, 1270, 866, 8015, -1476, -3195, 2068, 789, 861, 11498, -1931, -3965, 2040, 1857, 960, 9810, -1732, -3456, 2016, 1270, 866, 12995, -1099, -4635, 2118, 2505, 1173, 11498, -1931, -3965, 2040, 1857, 960, 14635, -192, -5620, 2108, 3171, 1079, 12995, -1099, -4635, 2118, 2505, 1173, 17870, -3984, -6724, 2175, 3951, 1255, 14635, -192, -5620, 2108, 3171, 1079, 17619, 2538, -8191, 1980, 4539, 1551, 17870, -3984, -6724, 2175, 3951, 1255, 19334, 2856, -9086, 1637, 5001, 1469, 17619, 2538, -8191, 1980, 4539, 1551, 21199, 3754, -9610, 1970, 5863, 1666, 19334, 2856, -9086, 1637, 5001, 146]
    print(len(data))
    print(f'{"="*20} Testing {"="*20}\n')
    t, aa, x, y, z, ax, ay, az, d, accel, taa, tla = process_data(data)
    print(f"z val right after return: {z}")
    
    #laz_ms2 = (_convert_from_g(z))
    #vel_data = get_inst_velocity(laz_ms2)
    nx, ny, nz = velocity_calc([x, y, z], [ax, ay, az])
    print(f"len nx: {len(nx)}, len ny: {len(ny)}, len nz: {len(nz)}")
    laz_ms2 = (_convert_from_g(nz))
    #v, vf_m, fv, pos = get_club_head_speed(z, accel)
    v, vf_m, fv, pos = get_club_head_speed(nz, accel)
    print(f"INTIAL DATA: {t}\n")
    print(
        #f'CLUB HEAD SPEED: \n\n{tabulate(zip(x,y,z,laz_ms2,vel_data,vf_m), headers=["x (g)", "y (g)", "z (g)", "total (m/s^2)", "v (m/s i think)", "v (mph)"], tablefmt="pretty")}\n')
        f'CLUB HEAD SPEED: \n\n{tabulate(zip(nx,ny,nz,laz_ms2,vf_m), headers=["x (g)", "y (g)", "z (g)", "total (m/s^2)", "v (mph)"], tablefmt="pretty")}\n')
    #print(f'FINAL VELOCITY: {fv:.2} mph\n')
    print(f'FINAL VELOCITY: {max(vf_m):.2} mph\n')
    print(f'{"="*10} ACCEL {"="*10}\n')
    print('INITIAL ANGULAR ACCELERATION: ', aa, '\n')
    print(
        f'ANGULAR ACCELERATION: \n\n{tabulate(zip(ax,ay,az,d), headers=["x (??)", "y (??)", "z (??)", "dir"], tablefmt="pretty")}\n')

    print(f'{"="*10} BALL SPEED {"="*10}\n')
    print(f'BALL SPEED: {get_ball_speed("driver", fv):.2} mph\n')

    print(f'{"="*10} BALL DISTANCE {"="*10}\n')
    print(
        f'BALL DISTANCE: {get_ball_distance(fv, get_ball_speed("driver", fv)):.2} yards\n')

    print(f'{"="*10} SMASH FACTOR {"="*10}\n')
    print(
        f'SMASH FACTOR: {get_smash_factor(fv, get_ball_speed("driver", fv)):.2}\n')

    print(f'{"="*10} POSITION {"="*10}\n')
    print(pos[2:])

    print(f'{"="*10} PLOT {"="*10}\n')
    print(len(tla), len(taa), len(pos), len(vf_m))
    plot_acceleration(tla, taa, pos, vf_m)
