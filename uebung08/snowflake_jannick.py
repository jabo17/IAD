"""
    Implementation of koch-snowflake
"""
import math
import matplotlib.pyplot as plt


SNOWFLAKE_FILENAME = "snowflake"


def koch_snowflake(level: int) -> tuple:
    """
    Determines points of koch_snowflake.
    L = 1
    Triangle: (0,0),(1,0),(1/2,sqrt(3)/2)

    Args:
        level (int): level of subdivisions

    Returns:
        tuple: points_x, points_y

    """
    points_x = []
    points_y = []

    # init jobs stack
    jobs_stack = [[(1 / 2, math.sqrt(3) / 2), (0, 0), level],
                  [(1, 0), (1 / 2, math.sqrt(3) / 2), level],
                  [(0, 0), (1, 0), level]
                  ]

    while len(jobs_stack) > 0:
        job = jobs_stack.pop()
        '''
            p1 ------ p3 ------ p4 ------ p2
                        . a    .
                         .    .
                           p5
                           
            1) calc vec from p1 to p3 --> p1_3 = 1/3 * (p2 - p1)
            2) calc vec from origin to p3 --> p3 = p1 + p1_3
            3) calc vec from origin to p4 --> p4 = p3 + p1_3
            4) calc p5 = p3 + rotate(p1_3, 60 degree)
                a) for the rotation determine CosA = cos(a=60degree), SinA = sin(a=60degree)
                b) rotate p1_3: 
                   p1_3' = (p1_3.x * cosA - p1_3.y * sinA, p1_3.x * sinA + p1_3.y * cosA)
                c) p5 = p3 + p1_3'
        '''
        p1, p2, job_l = job

        # determine p3,p4,p5
        p1_3 = (1 / 3 * (p2[0] - p1[0]), 1 / 3 * (p2[1] - p1[1]))
        p3 = (p1_3[0] + p1[0], p1_3[1] + p1[1])
        p4 = (p1_3[0] + p3[0], p1_3[1] + p3[1])
        cos_a = math.cos(5 / 3 * math.pi)
        sin_a = math.sin(5 / 3 * math.pi)
        p5 = (p1_3[0] * cos_a - p1_3[1] * sin_a + p3[0], p1_3[0] * sin_a + p1_3[1] * cos_a + p3[1])

        # decrement job_level
        job_l -= 1

        # if job level is bigger than 0 create new jobs
        if job_l > 0:
            jobs_stack.extend([
                [p4, p2, job_l],
                [p5, p4, job_l],
                [p3, p5, job_l],
                [p1, p3, job_l],
            ])
        else:
            # put p0,p3,p5,p4 to points
            points_x.extend([p1[0], p3[0], p5[0], p4[0]])
            points_y.extend([p1[1], p3[1], p5[1], p4[1]])

    # close line
    points_x.append(0)
    points_y.append(0)

    return points_x, points_y


def test_koch_snowflake():
    points_x, points_y = koch_snowflake(5)

    with open(SNOWFLAKE_FILENAME + ".txt", "w") as fd:
        for i in range(len(points_x)):
            fd.write(f"{points_x[i]} {points_y[i]}\n")

    plt.plot(points_x, points_y)
    plt.gca().set_aspect('equal')
    plt.savefig(SNOWFLAKE_FILENAME + ".svg")
