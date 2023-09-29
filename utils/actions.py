# coding=utf8
from utils.joint_preprocess import *
import math


class actionPredictor(object):

    def __init__(self):
        pass

    @staticmethod
    def move_status(joints):

        if joint_filter(joints[0]) and joint_filter(joints[-1]):
            # init_x = (init_neck_x + init_rhip_x + init_lhip_x) / 3
            init_x = float(joints[0][1][0] + joints[0][8][0] + joints[0][11][0]) / 3
            # init_y = (init_neck_y + init_rhip_y + init_lhip_y) / 3
            init_y = float(joints[0][1][1] + joints[0][8][1] + joints[0][11][1]) / 3
            # end_x = (end_neck_x + end_rhip_x + end_lhip_x) / 3
            end_x = float(joints[-1][1][0] + joints[-1][8][0] + joints[-1][11][0]) / 3
            # end_y = (end_neck_y + end_rhip_y + end_lhip_y) / 3
            end_y = float(joints[-1][1][1] + joints[-1][8][1] + joints[-1][11][1]) / 3

            # init_h1 = (init_rhip_y + init_lhip_y) / 2 - init_neck_y
            init_h1 = float(joints[0][8][1] + joints[0][11][1]) / 2 - joints[0][1][1]
            # end_h1 = (end_rhip_y + end_lhip_y) / 2 - end_neck_y
            end_h1 = float(joints[-1][8][1] + joints[-1][11][1]) / 2 - joints[-1][1][1]
            try:
                h1 = end_h1 / init_h1
            except:
                h1 = 0.0
            # init_h2 = (init_rknee_y + init_lknee_y) / 2 - (init_rhip_y + init_lhip_y) / 2
            init_h2 = (float(joints[0][9][1] + joints[0][12][1]) - float(joints[0][8][1] + joints[0][11][1])) / 2
            # end_h2 = (end_rknee_y + end_lknee_y) / 2 - (end_rhip_y + end_lhip_y) / 2
            end_h2 = (float(joints[-1][9][1] + joints[-1][12][1]) - float(joints[-1][8][1] + joints[-1][11][1])) / 2
            try:
                h2 = end_h2 / init_h2
            except:
                h2 = 0.0

            # init_w1 = (init_rhip_x + init_lhip_x) / 2 - init_neck_x
            init_w1 = float(joints[0][8][0] + joints[0][11][0]) / 2 - joints[0][1][0]
            # end_w1 = (end_rhip_x + end_lhip_x) / 2 - end_neck_x
            end_w1 = float(joints[-1][8][0] + joints[-1][11][0]) / 2 - joints[-1][1][0]
            try:
                w1 = end_w1 / init_w1
            except:
                w1 = 0.0
            # init_w2 = (init_rknee_x + init_lknee_x) / 2 - (init_rhip_x + init_lhip_x) / 2
            init_w2 = (float(joints[0][9][0] + joints[0][12][0]) - float(joints[0][8][0] + joints[0][11][0])) / 2
            # end_w2 = (end_rknee_x + end_lknee_x) / 2 - (end_rhip_x + end_lhip_x) / 2
            end_w2 = (float(joints[-1][9][0] + joints[-1][12][0]) - float(joints[-1][8][0] + joints[-1][11][0])) / 2
            try:
                w2 = end_w2 / init_w2
            except:
                w2 = 0.0

            xc = end_x - init_x
            yc = end_y - init_y
            
            if abs(xc) < 30. and abs(yc) < 20.:
                # ty_1 = end_neck_y
                ty_1 = float(joints[-1][1][1])
                # ty_8 = (end_rhip_y + end_lhip_y) / 2
                ty_8 = float(joints[-1][8][1] + joints[-1][11][1]) / 2
                # ty_9 = (end_rknee_y + end_lknee_y) / 2
                ty_9 = float(joints[-1][9][1] + joints[-1][12][1]) / 2
                try:
                    t = float(ty_8 - ty_1) / (ty_9 - ty_8)
                except:
                    t = 0.0
                if h1 < 1.16 and h1 > 0.84 and h2 < 1.16 and h2 > 0.84:

                    if t < 1.73:
                        return 1 # stand
                    else:
                        return 2 # sit
                else:
                    if t < 1.7:
                        if h1 >= 1.08:
                            return 4 # walk close

                        elif h1 < 0.92:
                            return 5 # walk away
                        else:
                            return 0 # nothing
                    else:
                        return 0 # nothing
            elif abs(xc) < 30. and abs(yc) >= 30.:
                # init_y1 = init_neck_y
                init_y1 = float(joints[0][1][1])
                # init_y8 = (init_rhip_y + init_lhip_y) / 2
                init_y8 = float(joints[0][8][1] + joints[0][11][1]) / 2
                # init_y9 = (init_rknee_y + init_lknee_y) / 2
                init_y9 = float(joints[0][9][1] + joints[0][12][1]) / 2

                # end_y1 = end_neck_y
                end_y1 = float(joints[-1][1][1])
                # end_y8 = (end_rhip_y + end_lhip_y) / 2
                end_y8 = float(joints[-1][8][1] + joints[-1][11][1]) / 2
                # end_y9 = (end_rknee_y + end_lknee_y) / 2
                end_y9 = float(joints[-1][9][1] + joints[-1][12][1]) / 2
                try:
                    init_yc = float(init_y8 - init_y1) / (init_y9 - init_y8)
                except:
                    init_yc = 0.0
                try:
                    end_yc = float(end_y8 - end_y1) / (end_y9 - end_y8)
                except:
                    end_yc = 0.0
                th_yc = 0.1
                if yc >= 25 and abs(end_yc - init_yc) >= th_yc:
                    return 6 # sit down
                elif yc < -20 and abs(end_yc - init_yc) >= th_yc:
                    return 7 # stand up
                else:
                    return 0 # nothing
            elif abs(xc) > 30. and abs(yc) < 30.:
                return 3 # walk
            elif abs(xc) < 20. and abs(yc) < 30.:
                # tx_1 = end_neck_x
                tx_1 = float(joints[-1][1][0])
                # tx_8 = (end_rhip_x + end_lhip_x) / 2
                tx_8 = float(joints[-1][8][0] + joints[-1][11][0]) / 2
                # tx_9 = (end_rknee_x + end_lknee_x) / 2
                tx_9 = float(joints[-1][9][0] + joints[-1][12][0]) / 2
                try:
                    t = float(tx_8 - tx_1) / (tx_9 - tx_8)
                except:
                    t = 0.0
                if ((w1 < 1.16 and w1 > 0.84 and w2 < 1.16 and w2 > 0.84) or
                    t < 1.7 and (w1 >= 1.08 or w1 < 0.92)):
                    return 8 # lying
                else:
                    return 0 # nothing
            else:
                return 0 # nothing
            
        head_is_straight = False
        shoulder_is_straight = False
        right_arm_is_straight = False
        left_arm_is_straight = False
        spine_is_straight = False
        right_leg_is_straight = False
        left_leg_is_straight = False
            
        # if (0 in joints[0] and
        #     (16 in joints[0] or
        #      17 in joints[0])):
        #     ear_index = 16 if 16 in joints[0] else 17
        #     head_angle = math.atan2(abs(joints[0][0][1] - joints[0][ear_index][1]),
        #                             abs(joints[0][0][0] - joints[0][ear_index][0])) * 180 / math.pi
        #     print(f'head_angle: {head_angle}')
        #     head_is_straight = abs(head_angle) < 45
        if (2 in joints[0] and
            5 in joints[0]):
            shoulder_angle = math.atan2(abs(joints[0][2][1] - joints[0][5][1]),
                                        abs(joints[0][2][0] - joints[0][5][0])) * 180 / math.pi
            print(f'shoulder_angle: {shoulder_angle}')
            shoulder_is_straight = abs(shoulder_angle) < 30
        elif (1 in joints[0] and
            (2 in joints[0] or
             5 in joints[0])):
            shoulder_index = 2 if 2 in joints[0] else 5
            shoulder_angle = math.atan2(abs(joints[0][1][1] - joints[0][shoulder_index][1]),
                                        abs(joints[0][1][0] - joints[0][shoulder_index][0])) * 180 / math.pi
            print(f'shoulder_angle: {shoulder_angle}')
            shoulder_is_straight = abs(shoulder_angle) < 30
        # if (2 in joints[0] and
        #     3 in joints[0]):
        #     right_arm_angle = math.atan2(abs(joints[0][2][1] - joints[0][3][1]),
        #                                  abs(joints[0][2][0] - joints[0][3][0])) * 180 / math.pi
        #     print(f'right_arm_angle: {right_arm_angle}')
        #     right_arm_is_straight = abs(right_arm_angle) > 45
        # if (5 in joints[0] and
        #     6 in joints[0]):
        #     left_arm_angle = math.atan2(abs(joints[0][5][1] - joints[0][6][1]),
        #                                 abs(joints[0][5][0] - joints[0][6][0])) * 180 / math.pi
        #     print(f'left_arm_angle: {left_arm_angle}')
        #     left_arm_is_straight = abs(left_arm_angle) > 45
        if (1 in joints[0] and
            (8 in joints[0] or
             11 in joints[0])):
            hip_index = 8 if 8 in joints[0] else 11
            spine_angle = math.atan2(abs(joints[0][1][1] - joints[0][hip_index][1]),
                                     abs(joints[0][1][0] - joints[0][hip_index][0])) * 180 / math.pi
            print(f'spine_angle: {spine_angle}')
            spine_is_straight = abs(spine_angle) > 45
        if (8 in joints[0] and
            9 in joints[0]):
            right_leg_angle = math.atan2(abs(joints[0][8][1] - joints[0][9][1]),
                                         abs(joints[0][8][0] - joints[0][9][0])) * 180 / math.pi
            print(f'right_leg_angle: {right_leg_angle}')
            right_leg_is_straight = abs(right_leg_angle) > 45
        if (11 in joints[0] and
            12 in joints[0]):
            left_leg_angle = math.atan2(abs(joints[0][11][1] - joints[0][12][1]),
                                        abs(joints[0][11][0] - joints[0][12][0])) * 180 / math.pi
            print(f'left_leg_angle: {left_leg_angle}')
            left_leg_is_straight = abs(left_leg_angle) > 45

        if not (# head_is_straight or
            shoulder_is_straight or
            # right_arm_is_straight or
            # left_arm_is_straight or
            spine_is_straight or
            right_leg_is_straight or
            left_leg_is_straight):
            return 8 # lying

        return 0 # nothing
