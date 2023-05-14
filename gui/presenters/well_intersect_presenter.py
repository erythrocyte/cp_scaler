from gui.models.well_inter_calc_prms import WellIntersectCalcParams

from src.services import grdecl_reader, well_track_reader, grid_converter, intersect_finder, grid_worker


def calc(prms: WellIntersectCalcParams, updater):
    updater(0)
    grd = grdecl_reader.read_grid(prms.data_fn)
    updater(20)
    well = well_track_reader.read_well_track(prms.well_track_fn)
    updater(30)

    vtk_grid = grid_converter.convert_to_vtk(grd)
    updater(50)
    # grid_saver.save_ug_vtk(os.path.join(s.d, '1.vtk'), vtk_grid)

    cell_indexes = intersect_finder.find_intersected_cells(vtk_grid, well)
    updater(85)

    ijk_indexes = grid_worker.get_grid_cell_indexes_from_vtk(grd, cell_indexes)
    updater(95)

    __save_indexes(prms.result_fn, ijk_indexes)
    updater(100)
    print('intersect finding completed')


def __save_indexes(fn: str, ijk_indexes):
    f = open(fn, 'w')
    for ijk in ijk_indexes:
        f.write('\t'.join([str(v + 1) for v in ijk]) + '\n')
    f.close()
