import math
from tabulate import tabulate

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


def get_club_head_speed(data):
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

    velo_f = 0
    linear_accel = [data[i:i+3] for i in range(0, len(data), 3)][1::2]
    angular_accel = [data[i:i+3] for i in range(0, len(data), 3)][::2]
    linear_accel_x = _get_gs([x[0] for x in linear_accel])
    angular_accel_x = ([x[0] for x in angular_accel])
    linear_accel_y = _get_gs([x[1] for x in linear_accel])
    angular_accel_y = ([x[1] for x in angular_accel])
    linear_accel_z = _get_gs([x[2] for x in linear_accel])
    angular_accel_z = ([x[2] for x in angular_accel])

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

    total_accel = (_convert_from_g(total_accel))

    velo_f = [velo_f + (total_accel[i])
              * TIME_PER_DATA_POLL for i in range(len(total_accel))]

    velo_f_mph = [x * 2.23694 for x in velo_f]

    v_len = len(velo_f_mph) if len(velo_f_mph) > 0 else 1

    final_velo = sum(velo_f_mph) / v_len

    # ! NEED TO ENSURE CORRECT UNITS
    return linear_accel, linear_accel_x, linear_accel_y, linear_accel_z, total_accel, velo_f, velo_f_mph, final_velo, angular_accel, angular_accel_x, angular_accel_y, angular_accel_z, direction


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
    return [(i / 32678) * 8 for i in data]


# def _get_dps(data):
#     return [(i / 32678) * 250 for i in data]


if __name__ == "__main__":
    print(f'{"="*20} Testing {"="*20}\n')
    accel, x, y, z, t, v, vf_m, fv, aa, ax, ay, az, d = get_club_head_speed(0)
    print(f"INTIAL DATA: {accel}\n")
    print(
        f'CLUB HEAD SPEED: \n\n{tabulate(zip(x,y,z,t,v,vf_m), headers=["x (g)", "y (g)", "z (g)", "total (m/s^2)", "v (m/s i think)", "v (mph)"], tablefmt="pretty")}\n')
    print(f'FINAL VELOCITY: {fv:.2} mph\n')
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
