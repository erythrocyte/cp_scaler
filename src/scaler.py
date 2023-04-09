import logging
from typing import List


def scale_coord(fig: List, nx: int, ny: int, sx: float, sy: float, updater) -> List:
    pts_count = (nx + 1) * (ny + 1) * 6
    if pts_count != len(fig):
        logging.error(f'Coord size is not corresponds to nx = {nx}, ny = {ny}')
        return None

    res = [None] * len(fig)

    x0, y0, z0 = fig[0], fig[1], fig[2]
    res[0] = x0
    res[1] = y0
    res[2] = z0

    for k in range(3, pts_count, 3):
        x1, y1, z1 = fig[k], fig[k+1], fig[k+2]
        dx = x1 - x0
        dy = y1 - y0

        res[k] = x0 + dx * sx
        res[k+1] = y0 + dy * sy
        res[k + 2] = z1

        updater(int((k+1) / pts_count * 100))

    return res
