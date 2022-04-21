from scene import Scene
import taichi as ti
from taichi.math import *
scene = Scene(voxel_edges=0, exposure=3)
scene.set_directional_light((0.6, 1, 0.6), 0.01, (1, 0.9, 0.8)); scene.set_floor(0, (0, 0.1, 0.2))
BLACK = vec3(0, 0.1, 0.15); RED = vec3(0.4, 0, 0.1); GREEN = vec3(0.05, 0.4, 0.1); WHITE = vec3(0.9, 0.9, 0.8)
@ti.func
def dots_1(x, y):
    res = WHITE
    if (y == 2 or y == 6) and x > 1 and x < 5: res = BLACK
    if y > 2 and y < 6 and (x == 1 or x == 5): res = BLACK
    if y > 2 and y < 6 and x > 1 and x < 5: res = RED
    return res
@ti.func
def dots_2(x, y):
    res = WHITE
    if y < 8 and y % 4 != 0 and x > 1 and x < 5: res = BLACK
    return res
@ti.func
def dots_3(x, y):
    res = WHITE
    if (y == 1 or y == 2) and (x == 4 or x == 5): res = BLACK
    if (y == 4 or y == 5) and x > 1 and x < 5: res = RED
    if (y == 7 or y == 8) and (x == 1 or x == 2): res = BLACK
    return res
@ti.func
def dots_4(x, y):
    res = WHITE
    if (y == 1 or y == 2 or y == 7 or y == 8) and x % 3 != 0: res = BLACK
    return res
@ti.func
def dots_5(x, y):
    res = WHITE
    if (y == 1 or y == 2 or y == 7 or y == 8) and x % 3 != 0: res = BLACK
    if (y == 4 or y == 5) and x > 1 and x < 5: res = RED
    return res
@ti.func
def bamboo_2(x, y):
    res = WHITE
    if y < 8 and y % 4 != 0 and x == 3: res = GREEN
    return res
@ti.func
def bamboo_3(x, y):
    res = WHITE
    if y > 0 and y < 4 and (x == 1 or x == 5): res = GREEN
    if y > 4 and y < 8 and x == 3: res = GREEN
    return res
@ti.func
def bamboo_4(x, y):
    res = WHITE
    if y < 8 and y % 4 != 0 and (x == 1 or x == 5): res = GREEN
    return res
@ti.func
def bamboo_5(x, y):
    res = WHITE
    if y < 8 and y % 4 != 0 and (x == 1 or x == 5): res = GREEN
    if y > 2 and y < 6 and x == 3: res = RED
    return res
@ti.func
def bamboo_6(x, y):
    res = WHITE
    if y < 8 and y % 4 != 0 and x % 2 != 0: res = GREEN
    return res
@ti.func
def bamboo_7(x, y):
    res = WHITE
    if (y == 7 or y == 8) and x == 3: res = RED
    if y < 7 and y % 3 != 0 and x % 2 != 0: res = GREEN
    return res
@ti.func
def bamboo_9(x, y):
    res = WHITE
    if y % 3 != 0 and (x == 1 or x == 5): res = GREEN
    if y % 3 != 0 and x == 3: res = RED
    return res
@ti.func
def dragons_white(x, y):
    return WHITE
N = 63; E = 10; PIECES = [dots_1, dots_2, dots_3, dots_4, dots_5, bamboo_2, bamboo_3,
bamboo_4, bamboo_5, bamboo_6, bamboo_7, bamboo_9, dragons_white]
@ti.func
def gen_1(corner, right, up, front, get_piece_color: ti.template()):
    for x, y, z in ti.ndrange(7, 10, 3):
        pos = corner + x * right + y * up + z * front
        if z == 0: scene.set_voxel(pos, 1, get_piece_color(x, y))
        elif z == 1: scene.set_voxel(pos, 1, WHITE)
        else: scene.set_voxel(pos, 1, vec3(0, 0.6, 0.3))
@ti.func
def gen_13(corner, right, up, front):
    for i in ti.static(range(13)):
        gen_1(corner + i * 8 * right, right, up, front, PIECES[i])
@ti.kernel
def initialize_voxels():
    gen_13(vec3(-N + E, 0, N), vec3(1, 0, 0), vec3(0, 1, 0), vec3(0, 0, -1))
    gen_13(vec3(N, 0, N - E), vec3(0, 0, -1), vec3(0, 1, 0), vec3(-1, 0, 0))
    gen_13(vec3(N - E, 0, -N), vec3(-1, 0, 0), vec3(0, 1, 0), vec3(0, 0, 1))
    gen_13(vec3(-N, 0, -N + E), vec3(0, 0, 1), vec3(0, 1, 0), vec3(1, 0, 0))
initialize_voxels()
scene.finish()
