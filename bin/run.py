import os
from bin import s
from src.services import grdecl_reader, grid_converter, well_track_reader, intersect_finder, grid_saver


def do():
    data_fn = os.path.join(s.d,  'Test_local_coord_2.grdecl')
    well_track_fn = os.path.join(s.d, 'well_track.dat')

    grd = grdecl_reader.read_grid(data_fn)
    well = well_track_reader.read_well_track(well_track_fn)

    vtk_grid = grid_converter.convert_to_vtk(grd)
    grid_saver.save_ug_vtk(os.path.join(s.d, '1.vtk'), vtk_grid)

    intersect_finder.find_intersected_cells(vtk_grid, well)

    print('intersect finding completed')
