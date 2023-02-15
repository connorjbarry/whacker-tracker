import numpy as np

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
    "2iron": 24,
    "3iron": 27,
    "4iron": 30,
    "5iron": 33,
    "6iron": 36,
    "7iron": 39,
    "8iron": 42,
    "9iron": 45,
    "pw": 48,
    "gw": 51,
    "sw": 54,
}

DISTMULTIPLIER_CH = 3.16
DISTMULTIPLIER_BS = 2.04


def get_club_head_speed(coords):
    pass


def get_ball_speed(club, club_head_speed):
    return club_head_speed * CLUBHEADTOBALL[club]


def get_ball_distance(club_head_speed, ball_speed):
    dist_from_head_speed = club_head_speed * DISTMULTIPLIER_CH - 85.2
    dist_from_ball_speed = ball_speed * DISTMULTIPLIER_BS - 65.2

    dist_from_head_speed = 0 if dist_from_head_speed < 0 else dist_from_head_speed
    dist_from_ball_speed = 0 if dist_from_ball_speed < 0 else dist_from_ball_speed

    error = (dist_from_head_speed - dist_from_ball_speed)

    # TODO: Fix this
    return (dist_from_head_speed + dist_from_ball_speed) / 2


def get_smash_factor(club_head_speed, ball_speed):
    return ball_speed / club_head_speed


def get_launch_angle(club, angle):
    pass


def get_club_face_angle(coords, rot):
    pass
