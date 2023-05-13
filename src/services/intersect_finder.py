import vtk
from src.models.well_track import WellTrack


def find_intersected_cells(grd: vtk.vtkUnstructuredGrid, well: WellTrack):
    locator = vtk.vtkCellLocator()
    locator.SetDataSet(grd)
    locator.BuildLocator()

    locator.IntersectWithLine()
