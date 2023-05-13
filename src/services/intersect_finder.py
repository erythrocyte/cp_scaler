import vtk
import logging
from src.models.well_track import WellTrack


def find_intersected_cells(grd: vtk.vtkUnstructuredGrid, well: WellTrack):
    locator = vtk.vtkCellLocator()
    locator.SetDataSet(grd)
    locator.BuildLocator()

    cellsIds = vtk.vtkIdList()
    locator.FindCellsAlongLine([well.points[0].x, well.points[0].y, well.points[0].z],
                               [well.points[1].x, well.points[1].y, well.points[1].z], 0.001, cellsIds)

    logging.info(f'intersection with well completed({cellsIds.GetNumberOfIds()} cells)')
