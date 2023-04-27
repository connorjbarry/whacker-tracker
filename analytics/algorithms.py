import math
from tabulate import tabulate
import matplotlib.pyplot as plt
import numpy as np

G = 9.80665
SENS1_DIST = 10
SENS2_DIST = 20
SENS3_DIST = 30

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
    "driver": 13,
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

    linear_accel = [data[i:i+3]
                    for i in range(0, len(data), 3)][1::2]
    # print(linear_accel)
    angular_accel = [data[i:i+3]
                     for i in range(0, len(data), 3)][::2]
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
    linear_accel_z = (linear_accel_z)

    return linear_accel, angular_accel, linear_accel_x, linear_accel_y, linear_accel_z, angular_accel_x, angular_accel_y, angular_accel_z, direction, total_accel, total_angular_accel, total_linear_accel


def get_club_head_speed(linear_z, total_accel):
    velo_f = 0

    time_list = [i * TIME_PER_DATA_POLL for i in range(len(total_accel))]

    linear_z_dir = list(filter(lambda x: x < 0, linear_z[2:]))

    len_linear_z_dir = len(linear_z_dir)
    time = TIME_PER_DATA_POLL * len_linear_z_dir
    len_linear_z_velo = (sum(linear_z_dir) / len_linear_z_dir) / time

    velo_f = _convert_from_g(linear_z)

    # velo_f = [(total_accel[i])
    #           * TIME_PER_DATA_POLL for i in range(len(total_accel))]

    position = [i / 2 + TIME_PER_DATA_POLL for i in velo_f]
    position_sum = [sum(position[2:i]) for i in range(len(position) - 2)]

    velo_f_mph = [abs(x) * 2.23694 for x in velo_f]

    v_len = len(velo_f_mph) if len(velo_f_mph) > 0 else 1

    final_velo = max(velo_f_mph[2:v_len])

    index = velo_f_mph.index(final_velo)

    velo_f_mph = sum(velo_f_mph[index:index+5]) / 5

    # ! NEED TO ENSURE CORRECT UNITS
    return velo_f, velo_f_mph, final_velo, index


def get_ball_speed(club, club_head_speed):
    return club_head_speed * CLUBHEADTOBALL[club]


def get_ball_distance(club_head_speed, ball_speed):
    dist_from_head_speed = club_head_speed * DISTMULTIPLIER_CH - 85.2
    dist_from_ball_speed = ball_speed * DISTMULTIPLIER_BS - 65.2

    if dist_from_head_speed < 0:
        dist_from_head_speed = club_head_speed * DISTMULTIPLIER_CH
    if dist_from_ball_speed < 0:
        dist_from_ball_speed = ball_speed * DISTMULTIPLIER_BS
    # dist_from_head_speed = 0 if dist_from_head_speed < 0 else dist_from_head_speed
    # dist_from_ball_speed = 0 if dist_from_ball_speed < 0 else dist_from_ball_speed

    # TODO: Fix this
    return dist_from_head_speed if dist_from_head_speed >= dist_from_ball_speed else dist_from_ball_speed


def get_smash_factor(club_head_speed, ball_speed):
    if club_head_speed == 0:
        return 0
    return ball_speed / club_head_speed


def get_launch_angle(club, angle):
    loft = CLUBLOFT[club]
    return (loft + angle)


def get_club_face_angle(anglur_accel_y, idx):
    ang = anglur_accel_y[2:]
    ang = [theta * TIME_PER_DATA_POLL for theta in ang]
    first_ang_point = ang[0]
    return ang[idx]


def _convert_from_g(data):
    return [round(i * G, 2) for i in data]


def _get_gs(data):
    return [(i / 32678) * 8 for i in data]


def _get_dps(data):
    return [(i * 8.75) / 1000 for i in data]


def process_individal_sensor_data(data):
    data_length = len(data)
    len_sensor_data = data_length // 2
    # sensor_one = data[0:len_sensor_data]
    sensor_two = data[0:len_sensor_data]
    sensor_three = data[len_sensor_data:len_sensor_data * 2]
    # t_1, aa_1, x_1, y_1, z_1, ax_1, ay_1, az_1, d_1, accel_1, taa_1, tla_1 = process_data(
    #     sensor_one)
    # nx1, ny1, nz1 = velocity_calc([x_1, y_1, z_1], [ax_1, ay_1, az_1])
    t_2, aa_2, x_2, y_2, z_2, ax_2, ay_2, az_2, d_2, accel_2, taa_2, tla_2 = process_data(
        sensor_two)
    nx2, ny2, nz2 = velocity_calc([x_2, y_2, z_2], [ax_2, ay_2, az_2])
    t_3, aa_3, x_3, y_3, z_3, ax_3, ay_3, az_3, d_3, accel_3, taa_3, tla_3 = process_data(
        sensor_three)
    nx3, ny3, nz3 = velocity_calc([x_3, y_3, z_3], [ax_3, ay_3, az_3])

    # _, _, s1_club_head_speed = get_club_head_speed(nz1, accel_1)
    s2_v, s2_vf, s2_club_head_speed, idx_2 = get_club_head_speed(nz2, accel_2)
    _, s3_vf, s3_club_head_speed, idx_3 = get_club_head_speed(nz3, accel_3)

    s2_ball_speed = get_ball_speed('driver', s2_club_head_speed)
    s3_ball_speed = get_ball_speed('driver', s3_club_head_speed)

    s2_ball_distance = get_ball_distance(s2_club_head_speed, s2_ball_speed)
    s3_ball_distance = get_ball_distance(s3_club_head_speed, s3_ball_speed)

    s2_smash_factor = get_smash_factor(s2_club_head_speed, s2_ball_speed)
    s3_smash_factor = get_smash_factor(s3_club_head_speed, s3_ball_speed)

    xs_2, ys_2, zs_2 = get_club_position_data(t_2)

    s2_club_face_angle = get_club_face_angle(
        ay_2, idx_2)
    s3_club_face_angle = get_club_face_angle(
        ay_3, idx_3)

    s2_launch_angle = get_launch_angle('driver', s2_club_face_angle)
    s3_launch_angle = get_launch_angle('driver', s3_club_face_angle)

    s1_predicted_chs = abs(((s2_club_head_speed - s3_club_head_speed) /
                            10) * SENS1_DIST)
    if s1_predicted_chs < s2_club_head_speed and s1_predicted_chs < s3_club_head_speed:
        s1_predicted_chs = s2_club_head_speed + s1_predicted_chs
    s1_predicted_bs = get_ball_speed('driver', s1_predicted_chs)
    s1_predicted_dist = get_ball_distance(s1_predicted_chs, s1_predicted_bs)
    s1_predicted_sf = get_smash_factor(s1_predicted_chs, s1_predicted_bs)
    s1_predicted_cfa = ((s2_club_face_angle - s3_club_face_angle) /
                        10) * 30
    s1_predicted_la = ((s2_launch_angle - s3_launch_angle) /
                       10) * 30

    print('Sensor 1')
    print(tabulate([['Ball Speed', s1_predicted_bs], ['Club Head Speed', s1_predicted_chs], ['Ball Distance', s1_predicted_dist], ['Smash Factor', s1_predicted_sf], ['Club Face Angle', s1_predicted_cfa], ['Launch Angle', s1_predicted_la]], headers=[
          'Data', 'Value'], tablefmt='orgtbl'))

    print('Sensor 2')
    print(tabulate([['Ball Speed', s2_ball_speed], ['Club Head Speed', s2_club_head_speed], ['Ball Distance', s2_ball_distance], [
          'Smash Factor', s2_smash_factor], ['Club Face Angle', s2_club_face_angle], ['Launch Angle', s2_launch_angle]], headers=['Data', 'Value'], tablefmt='orgtbl'))

    print('Sensor 3')
    print(tabulate([['Ball Speed', s3_ball_speed], ['Club Head Speed', s3_club_head_speed], ['Ball Distance', s3_ball_distance], [
          'Smash Factor', s3_smash_factor], ['Club Face Angle', s3_club_face_angle], ['Launch Angle', s3_launch_angle]], headers=['Data', 'Value'], tablefmt='orgtbl'))

    # print(f'Sensor position data')
    # print(
    #     f'\n{tabulate(zip(xs_2, ys_2, zs_2), headers=["x", "y", "z"], tablefmt="pretty")}\n')

    # plot_position(xs_2, ys_2, zs_2)

    # print(f'Sensor 2 velocity data')
    # print(
    #     f'\n{tabulate(zip(nx2, ny2, nz2, s2_v), headers=["x", "y", "z", "m/s2"], tablefmt="pretty")}\n')

    return s1_predicted_chs, s1_predicted_bs, s1_predicted_dist, s1_predicted_sf, s1_predicted_cfa, s1_predicted_la


def get_club_position_data(linear_accel):
    accel = []
    for data in linear_accel:
        accel.append(_convert_from_g(_get_gs(data)))

    point_pos = []
    pos = []
    for data in accel:
        for i in data:
            point_pos.append(i/2 + TIME_PER_DATA_POLL)
        pos.append(point_pos)
        point_pos = []

    x_pos = [i[0] for i in pos]
    y_pos = [i[1] for i in pos]
    z_pos = [i[2] for i in pos]

    x_pos_sum = [sum(x_pos[2:i]) for i in range(len(x_pos) - 2)]
    y_pos_sum = [sum(y_pos[2:i]) for i in range(len(y_pos) - 2)]
    z_pos_sum = [sum(z_pos[2:i]) for i in range(len(z_pos) - 2)]

    return x_pos_sum, y_pos_sum, z_pos_sum

    # print([i for i in linear_accel if i == 1])
    # accel = _get_gs([i for i in linear_accel])
    # print(linear_accel)


def getRotationMatrix(yaw, roll, pitch):

    # rotation matrix for yaw angle
    R_Yaw = np.array([[np.cos(yaw), -np.sin(yaw), 0],
                      [np.sin(yaw), np.cos(yaw), 0],
                      [0, 0, 1]])

    # rotation matrix for roll angle
    R_Roll = np.array([[1, 0, 0],
                       [0, np.cos(roll), -np.sin(roll)],
                       [0, np.sin(roll), np.cos(roll)]])

    # rotation matrix for pitch angle
    R_Pitch = np.array([[np.cos(pitch), 0, np.sin(pitch)],
                        [0, 1, 0],
                        [-np.sin(pitch), 0, np.cos(pitch)]])

    return np.matmul(np.matmul(R_Yaw, R_Pitch), R_Roll)


def velocity_calc(acc, av):

    gravity_vector = [acc[0][0], acc[1][0], acc[2][0]]

    normalizedArr = []

    for i in range(1, len(acc[0])):
        # retreive data at ith index
        linearPoint = [acc[0][i], acc[1][i], acc[2][i]]

        # retreive difference in angular velocity between current point and i-1
        angularPoint = [av[0][i] + av[0][i-1], av[1]
                        [i] + av[1][i-1], av[2][i] + av[2][i-1]]

        # calculate yaw, roll, pitch from angularPoint
        yaw_delta_theta = (0.5) * (angularPoint[2]) * TIME_PER_DATA_POLL
        pitch_delta_theta = (0.5) * (angularPoint[1]) * TIME_PER_DATA_POLL
        roll_delta_theta = (0.5) * (angularPoint[0]) * TIME_PER_DATA_POLL

        rotationMatrix = getRotationMatrix(
            yaw_delta_theta, roll_delta_theta, pitch_delta_theta)

        gravity_vector = np.matmul(
            rotationMatrix, np.array(gravity_vector).T).T

        normalizedArr.append(linearPoint - gravity_vector)

    normalizedArr = [data.tolist() for data in normalizedArr]
    # return normalizedArr
    return [x[0] for x in normalizedArr], [x[1] for x in normalizedArr], [x[2] for x in normalizedArr]


def plot_position(x, y, z):
    # 3d plot x y z
    # label the plots and axes
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(x, y, z)
    ax.set_xlabel('X Label')
    ax.set_ylabel('Y Label')
    ax.set_zlabel('Z Label')

    # set title
    plt.title('3D Plot of Position')

    plt.show()


def plot_acceleration(linear_accel, angular_accel, linear_velo, position=[0 for i in range(104)]):
    data_len = len(linear_accel)
    print(
        f'types: {type(linear_accel)} {type(angular_accel)} {type(linear_velo)} )')
    time = [i * TIME_PER_DATA_POLL for i in range(data_len - 1)]
    fig, axs = plt.subplots(2, 2)
    # plot the linear acceleration
    axs[0, 0].plot(time, linear_accel[2:])
    axs[0, 0].scatter(time, linear_accel[2:])

    # plot the angular acceleration
    axs[0, 1].plot(time, angular_accel[2:])
    axs[0, 1].scatter(time, angular_accel[2:])

    # plot the position
    position_time = [i * TIME_PER_DATA_POLL for i in range(len(position))]
    axs[1, 0].plot(time, position)
    axs[1, 0].scatter(time, position)

    # plot the linear velocity
    axs[1, 1].plot(time, linear_velo[2:])
    axs[1, 1].scatter(time, linear_velo[2:])

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


if __name__ == "__main__":
    data = [715, -1544, -812, 350, 3502, -2138, 576, 18, -126, 43, 2362, 3314, -571, 23, -229, 45, 2425, 3296, -463, 21, -119, 62, 2310, 3261, -471, 24, -174, 82, 2368, 3279, -542, 7, -213, 96, 2375, -33, 3288, -481, -4, -147, 104, 2398, 3347, -409, -21, 349, 82, 2480, 3336, -438, -5, -37, 71, 2281, 3282, -459, -8, -44, 50, 2333, 3273, -413, -25, 57, 14, 2381, 3244, -486, -62, 182, -26, 2296, 3256, -572, -71, 89, -56, 2303, 3237, -479, -84, 153, -74, 2234, 3230, -501, -75, -66, -82, 2316, 3290, -438, -81, -397, -92, 2544, 3352, -252, -84, -1187, -74, 2521, 3417, -198, -152, -1500, 35, 2665, 3430, 85, -303, -425, 189, 2748, 3386, 354, -470, -308, 367, 2874, 3384, 285, -630, -323, 551, 3014, 3395, 414, -818, -75, 683, 3046, 3420, 551, -970, -322, 819, 3082, 3439, 465, -1136, -323, 913, 3106, 3441, 548, -1275, -287, 980, 3206, 3445, 619, -1386, -478, 1040, 3264, 3465, 630, -1467, -304, 1093, 3358, 3514, 750, -1546, -260, 1149, 3355, 3532, 742, -1580, -696, 1241, 3512, 3549, 669, -1599, -474, 1326, 3665, 3586, 825, -1586, -505, 1411, 3652, 3553, 716, -1503, -754, 1516, 3710, 3468, 677, -1400, -636, 1577, 3891, 3336, 629, -1275, -759, 1604, 3897, 3131, 406, -1102, -853, 1604, 3948, 2924, 445, -952, -433, 1575, 4098, 2710, 354, -795, -320, 1542, 3973, 2472, 117, -614, -605, 1531, 4038, 2215, 108, -433, -645, 1552, 4139, 1945, -65, 6, -249, -613, 1555, 4276, 1595, -230, 176, -76, 200, -556, 1541, 4508, 1195, -248, 60, -246, 1503, 4572, 865, -518, 196, -259, 1496, 4566, 611, -625, 323, -68, 1521, 4497, 317, -711, 430, -98, 1559, 4388, -11, -998, 556, -193, 1583, 4238, -215, -986, 648, 336, 1569, 4027, -390, -1017, 718, 523, 1511, 3458, -618, -1107, 726, 690, 1357, 3397, -870, -1263, 723, 385, 1116, 2818, -1102, -1231, 724, 205, 800, 2161, -1276, -1102, 677, 218, 476, 1918, -1427, -1365, 653, 76, 128, 1077, -1521, -1084, 596, 511, -228, 545, -1532, -1083, 544, 214, -671, 411, -1526, -1490, 518, -197, -1182, -10, -1417, -875, 368, 577, -1724, -590, -1316, -1774, 204, 749, -2300, -694, -1306, -1930, 94, 217, -2878, -846, -1187, -1272, 96, 803, -3587, -431, -1108, -2240, 168, 328, -4273, -146, -893, -1995, 314, 440, -4833, -79, -355, -1890, 558, 869, -5283, 729, 67, -2170, 801, 1113, -5641, 1115, 775, -1885, 1116, 1932, -5870, 1575, 1837, -2025, 1478, 1786, -6013, 2383, 2783, -2271, 1745, 1489, -6093, 2501, 3829, -1926, 2066, 2207, -6094, 2969, 4862, -1643, 2554, 2624, -6025, 3794, 5860, -1686, 3118, 2785, -5964, 4344, 7010, -1374, 3831, 3283, -5858, 5005, 7904, -849, 4726, 3276, -5455, 4961, 8573, 224, -540, 5573, 3832, -4687, 4609, 9133, -767, -240, 6307, 3523, -3571, 4314, 9622, -12, 6690, 3957, -2435, 4426, 9841, 14, 6792, 3504, -1318, 4222, 9723, -334, 6546, 1553, -465, 3640, 9621, -224, 5901, 1396, 215, 3047, 9181, -260, 5072, 5073, 1470, 988, 2811, 8617, -513, 4206, 678, 1655, 2398, 7820, -450, 3329, 29, 2073, 2354, 6678, -464, 2478, 4, 2323, 2611, 5668, -274, 1722, 43, 2496, 2187, 4878, -493, 1096, -860, 2535, 2565, 4120, -455, 447, -75, 2458, 2575, 3201, -746, -146, -232, 2438, 2343, 2431, -1282, -666, -633, 2421, 2195, 1812, -1154, -1069, -921, 2106, 2182, 1264, -1360, -1276, -1905, 2215, 2320, 815, -1333, -1418, -2103, 1949, 2396, 458, -1256, -1542, -1703, 1636, 2635, 48, -1384, -1694, -1388, 1367, 2485, -346, -1566, -1824, -1360, 1162, 2454, -584, -1717, 100, -1946, -1265, 988, 2758, -825, -1667, -2007, -1358, 839, 2706, -904, -1747, -2039, -1159, 741, 2759, -933, -1689, -2046, -924, 701, 2904, -1027, -1821, -2025, -842, 685, 2900, -1107, -1892, -2034, -912, 682, 3045, -1136, -1901, -2027, -427, 675, 3086, -1145, -2001, -2012, -567, 649, 3236, -1220, -2015, -1986, -657, 646, 3134, -1255, -2002, -1951, -602, 649, 3173, -1220, -2021, -1896, -739, 674, 3350, -
            1224, -2086, -1817, -656, 667, -1506, -642, 168, 3351, -2282, 473, 8, -126, 29, 2644, 3249, -219, 18, -209, 40, 2661, 3248, -150, -1, -171, 65, 2571, 3214, -138, 11, -146, 62, 2601, 3212, -189, -5, -203, 86, 2637, 3227, -219, -32, -266, 72, 2663, 3286, -122, -2, 291, 87, 2728, 3279, -56, -7, 94, 76, 2611, 3228, -103, -12, -101, 30, 2641, 3217, -110, -15, 35, 27, 2702, 3192, -171, -37, 169, -20, 2647, 3204, -265, -35, 115, -39, 2618, 3199, -209, -85, 151, -56, 2536, 3182, -189, -80, 39, -71, 2575, 3216, -185, -140, -266, -66, 2708, 3260, -44, -227, -870, -63, 2742, 3311, 49, -307, -1627, -34, 2678, 3325, 196, -337, -759, 118, 2767, 3285, 424, -504, -267, 317, 2843, 3245, 365, -615, -346, 416, 2897, 3222, 376, -800, -161, 563, 3070, 3214, 529, -966, -190, 709, 3043, 3202, 465, -1123, -381, 778, 3141, 3164, 537, -1265, -263, 881, 3270, 3123, 606, -1395, -413, 919, 3309, 3083, 641, -1497, -416, 1014, 3407, 3068, 805, -1584, -176, 1076, 3414, 3071, 827, -1651, -582, 1121, 3519, 3020, 808, -1645, -605, 1216, 3705, 2988, 967, -1627, -403, 1288, 3701, 2946, 989, -1587, -729, 1340, 3752, 2836, 978, -1493, -717, 1421, 3930, 2685, 955, -1371, -682, 1458, 4010, 2492, 836, -1234, -930, 1484, 4132, 2282, 830, -1083, -646, 1506, 4219, 2057, 782, -917, -315, 1518, 4174, 1847, 620, -747, -569, 1487, 4162, 1613, 509, -591, -733, 1499, 4177, 1345, 417, -397, -649, 1513, 4292, 1033, 243, -218, -728, 1536, 4531, 637, 118, -74, -393, 1545, 4658, 269, -59, 74, -327, 1518, 4623, 5, -247, 212, -263, 1502, 4496, -253, -346, 318, -80, 1520, 4364, -578, -586, 449, -353, 1519, 4254, -835, -741, 557, 35, 1525, 4159, -994, -764, 626, 413, 1474, 3784, -1147, -801, 628, 544, 1236, 3601, -1345, -1051, 699, 476, 1115, 3449, -1533, -1155, 633, 103, 807, 2930, -1636, -1057, 644, 213, 492, 2565, -1688, -1295, 711, 20, 218, 2074, -1719, -1219, 642, 293, -185, 1439, -1639, -1087, 625, 476, -638, 1431, -1565, -1452, 608, -193, -1013, 1257, -1435, -1237, 474, 271, -1560, 828, -1248, -1414, 439, 1035, -2059, 681, -1179, -2207, 470, 292, -2646, 466, -1117, -1722, 323, 810, -3266, 1091, -1101, -1739, 513, 743, -3695, 1446, -1080, -2042, 548, 430, -4361, 1258, -803, -1552, 715, 979, -4794, 1883, -529, -1565, 964, 1133, -5138, 2322, -247, -1546, 1253, 1880, -5490, 2630, 469, -1322, 1623, 2230, -5638, 3203, 1215, -1563, 1982, 1699, -5800, 3550, 1895, -1550, 2232, 2106, -5831, 3849, 2678, -1029, 2695, 2753, -5714, 4450, 3357, -758, 3281, 2887, -5612, 5211, 4085, -534, 4002, 3185, -5490, 6106, 4624, 151, 4706, 3406, -5066, 5988, 4960, 665, 5571, 3537, -4558, 5402, 5249, 982, 6229, 3663, -3575, 4826, 5572, 1062, 6733, 3471, -2644, 4724, 5770, 933, 6889, 3774, -1316, 4841, 5802, 429, 6728, 2083, -392, 4261, 5960, -131, 6122, 965, 310, 3688, 5957, -344, 5400, 1303, 976, 3049, 5885, -977, 4557, 884, 1660, 2729, 5716, -990, 3604, 12, 2033, 2608, 5162, -1036, 2820, -323, 2284, 2732, 4383, -997, 1994, 18, 2555, 2608, 3844, -1026, 1315, -803, 2513, 2652, 3384, -1167, 604, -602, 2491, 2984, 2723, -1115, 14, -153, 2506, 2809, 2146, -1747, -443, -626, 2376, 2529, 1631, -1899, -947, -783, 2279, 2439, 1199, -1814, -1270, -1538, 2080, 2516, 785, -1747, -1519, -2198, 1840, 2733, 399, -1524, -1664, -1935, 1579, 3006, 79, -1608, -1783, -1459, 1367, 2975, -292, -1744, -1906, -1365, 1115, 2823, -533, -1962, -1940, -1277, 928, 2930, -755, -1988, -2069, -1232, 794, 3006, -917, -1937, -2104, -1294, 667, 2952, -911, -1936, -2124, -907, 588, 2966, -995, -1876, -2104, -832, 590, 3028, -1093, -2012, -2090, -703, 549, 3020, -1105, -2027, -2110, -404, 531, 3160, -1133, -2071, -2074, -459, 550, 3271, -1177, -2145, -2056, -530, 530, 3242, -1248, -2096, -2034, -601, 531, 3220, -1228, -2069, -1961, -575, 536, 3271, -1199, -2077]

    print(len(data))
    print(f'{"="*20} Testing {"="*20}\n')
    # t, aa, x, y, z, ax, ay, az, d, accel, taa, tla = process_data(data)
    process_individal_sensor_data(data)
    # v, vf_m, fv, _ = get_club_head_speed(z, accel)
    # velo_idx = vf_m.index(fv)
    # print(f"INTIAL DATA: {t}\n")
    # print(
    #     f'CLUB HEAD SPEED: \n\n{tabulate(zip(x,y,z,accel,v,vf_m), headers=["x (g)", "y (g)", "z (g)", "total (m/s^2)", "v (m/s i think)", "v (mph)"], tablefmt="pretty")}\n')
    # print(f'FINAL VELOCITY: {fv} mph\n')
    # print(f'{"="*10} ACCEL {"="*10}\n')
    # # print('INITIAL ANGULAR ACCELERATION: ', aa, '\n')
    # print(
    #     f'ANGULAR ACCELERATION: \n\n{tabulate(zip(ax,ay,az,d), headers=["x (??)", "y (??)", "z (??)", "dir"], tablefmt="pretty")}\n')

    # print(f'{"="*10} BALL SPEED {"="*10}\n')
    # print(f'BALL SPEED: {round(get_ball_speed("driver", fv), 2)} mph\n')

    # print(f'{"="*10} BALL DISTANCE {"="*10}\n')
    # print(
    #     f'BALL DISTANCE: {round(get_ball_distance(fv, get_ball_speed("driver", fv)), 2)} yards\n')

    # print(f'{"="*10} SMASH FACTOR {"="*10}\n')
    # print(
    #     f'SMASH FACTOR: {round(get_smash_factor(fv, get_ball_speed("driver", fv)), 2)}\n')

    # x_pos, y_pos, z_pos = get_club_position_data(t)
    # print(f'{"="*10} POSITION {"="*10}\n')
    # # print(pos[2:])

    # print(f"{'='*10} CLUB FACE ANGLE {'='*10}\n")
    # print(f'{round(get_club_face_angle(ay, velo_idx), 2)} degrees\n')

    # print(f'{"="*10} PLOT {"="*10}\n')
    # plot_position(x_pos, y_pos, z_pos)
    # plot_acceleration(tla, taa, v)
