import math
from typing import List
from src.models import grid


def get_grid_cell_indexes_from_vtk(grd: grid.Grid, cell_indexes: List[int]):
    result = []
    nx = grd.nx
    ny = grd.ny
    nz = grd.nz
    for cell_index in cell_indexes:
        k = int(math.trunc(float(cell_index) / (nx * ny)))
        k1 = cell_index - k * nx * ny
        j = int(math.trunc(float(k1) / nx))
        i = int(k1 - j * nx)

        result.append([i, j, k])

    return result
