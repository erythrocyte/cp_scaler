import vtk
from src.models.grid import Grid
from src.services import grid_converter


def save_as_vtk(fn: str, grd: Grid):
    ug = grid_converter.convert_to_vtk(grd)
    xmlWriter = vtk.vtkXMLUnstructuredGridWriter()
    xmlWriter.SetFileName(fn)
    xmlWriter.SetInputData(ug)
    xmlWriter.Write()
    print('vtu saved!')


