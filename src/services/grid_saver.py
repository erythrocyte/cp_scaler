import vtk
import logging
from src.models.grid import Grid
from src.services import grid_converter


def save_as_vtk(fn: str, grd: Grid):
    ug = grid_converter.convert_to_vtk(grd)
    save_ug_vtk(fn, ug)


def save_ug_vtk(fn: str, grd: vtk.vtkUnstructuredGrid):
    xmlWriter = vtk.vtkXMLUnstructuredGridWriter()
    xmlWriter.SetFileName(fn)
    xmlWriter.SetInputData(grd)
    xmlWriter.Write()
    logging.debug('vtu saved!')
