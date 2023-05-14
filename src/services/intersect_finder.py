from typing import List
import vtk
import logging
from src.models.well_track import WellTrack


def find_intersected_cells(grd: vtk.vtkUnstructuredGrid, well: WellTrack) -> List[int]:
    locator = vtk.vtkCellLocator()
    locator.SetDataSet(grd)
    locator.BuildLocator()    

    result = []
    tolerance = 0.001

    for i in range (len(well.points)-1):
        p1 = well.get_point_list(i)
        p2 = well.get_point_list(i+1)
        cellsIds = vtk.vtkIdList()
        locator.FindCellsAlongLine(p1, p2, tolerance, cellsIds)
        for i in range(cellsIds.GetNumberOfIds()):
            result.append(cellsIds.GetId(i))

    result = list(dict.fromkeys(result))
    logging.info(f'intersection with well completed({cellsIds.GetNumberOfIds()} cells)')

    return result
