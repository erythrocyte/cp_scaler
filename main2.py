import scaler
import os.path
import coord_writer
import grdecl_reader
import vtk_saver
import vtk_saver2
import sys


def main():
    arg = sys.argv
    coord_fn = arg[1]
    nx = int(arg[2])
    ny = int(arg[3])
    sx = float(arg[4])
    sy = float(arg[5])
    scaled_fn = arg[6]
    # d = '/home/erythrocyte/Documents/move/GRID_SCALE_TEST/Test_local_coord_2/'
    # fn = os.path.join(d, 'Test_local_coord_2.grdecl')
    coord = grdecl_reader.read_coord(coord_fn)
    scaled_fig = scaler.scale_coord(coord, nx, ny, sx, sy)

    d = os.path.dirname(coord_fn)
    fn_fig = os.path.join(d, f'{scaled_fn}.dat')
    coord_writer.write(fn_fig, scaled_fig)
    print('Done!')

    # grd = grdecl_reader.read(fn)
    # # to vtk
    # vtk_name = os.path.join(d, 'orig.vtu')
    # # vtk_saver.save(vtk_name, grd)
    # vtk_saver2.save(vtk_name, grd)

    # sc = scaler.scale_coord(grd.coord, grd.nx, grd.ny, 0.2, 0.2)
    # grd.coord = sc
    # vtk_name = os.path.join(d, 'scaled.vtu')
    # vtk_saver2.save(vtk_name, grd)


if __name__ == '__main__':
    main()
