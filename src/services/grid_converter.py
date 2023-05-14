import vtk
import logging
from src.models.grid import Grid
import vtk.util.numpy_support as ns
import numpy as np


def convert_to_vtk(grd: Grid) -> vtk.vtkUnstructuredGrid:
    # * Convert corner point grid/cartesian grid into VTK unstructure grid
    logging.info('Converting GRDECL to Paraview Hexahedron mesh data....')
    NX, NY, NZ = grd.nx, grd.ny, grd.nz
    ug = vtk.vtkUnstructuredGrid()

    # 1.Collect Points from the raw CornerPoint data [ZCORN]&[COORD]
    # X,Y has to be interpolated from [ZCORN]
    Points = vtk.vtkPoints()
    Points.SetNumberOfPoints(len(grd.zcorn))  # =2*NX*2*NY*2*NZ

    ptsid = 0
    for k in range(NZ):
        for j in range(NY):
            for i in range(NX):
                CellCoords = __getCellCoords(i, j, k, grd)
                # Loop 8 point for each cell, see getCellCoords(i,j,k) for node ordering
                for pi in range(8):
                    Points.SetPoint(ptsid, CellCoords[pi])
                    ptsid += 1
    ug.SetPoints(Points)

    # 2. Recover Cells which follows the convention of [ZCORN]
    cellArray = vtk.vtkCellArray()
    Cell = vtk.vtkHexahedron()

    cellid = 0
    for k in range(NZ):
        for j in range(NY):
            for i in range(NX):
                for pi in range(8):
                    # Convert GRDECL node index convention to VTK convention
                    # https://www.vtk.org/wp-content/uploads/2015/04/file-formats.pdf
                    # 0,1,2,3(GRDECL)->0,1,3,2(VTK,anti-clockwise)
                    if(pi == 2 or pi == 6):
                        VTKid = pi+1
                    elif(pi == 3 or pi == 7):
                        VTKid = pi-1
                    else:
                        VTKid = pi
                    Cell.GetPointIds().SetId(pi, cellid*8+VTKid)
                cellArray.InsertNextCell(Cell)
                cellid += 1
    ug.SetCells(Cell.GetCellType(), cellArray)

    logging.debug(f"     NumOfPoints: {ug.GetNumberOfPoints()}")
    logging.debug(f"     NumOfCells: {ug.GetNumberOfCells()}")

    # Load all available keywords/cellarrays into VTK container
    for cube in grd.cubes:
        # VTK will automatically overwrite the data with the same keyword
        ug = __appendScalarData2VTK(ug, cube.name, np.array(cube.values))

    logging.info('Unstructured grid done!')

    return ug


def __appendScalarData2VTK(ug, name, numpy_array):
    # * Append scalar cell data (numpy array) into vtk object, should not directly called by user
    data = ns.numpy_to_vtk(numpy_array.ravel(order='F'),
                           deep=True, array_type=vtk.VTK_FLOAT)
    data.SetName(str(name))
    data.SetNumberOfComponents(1)
    ug.GetCellData().AddArray(data)

    return ug


def __getCellCoords(i, j, k, grd: Grid):
    """Get XYZ coords for eight node of a cell
    6----7
     -   -   <-Bottom Face
    4----5
      2----3
     -    -  <-Top Face
    0----1   
    Author:Bin Wang(binwang.0213@gmail.com)
    Date: Sep. 2018
    """
    XYZ = []
    Pillars = __getCellPillars(i, j, grd)
    Zs = __getCellZ(i, j, k, grd)
    for pi in range(8):  # Loop 8 point for each cell
        Pillar_i = pi % 4
        XYZ.append(__interpPtsOnPillar(Zs[pi], Pillars[Pillar_i]))
    return XYZ


def __interpPtsOnPillar(z, Pillar):
    """Obtain the eight coords for a cell
       X,Y coords has to be interpolated from Z
    xy1=xy0+k*z
    Pillar=[(x0 y0 z0),(x1 y1 z1)]
    (x,y,z) is somewhere between (x0 y0 z0) and (x1 y1 z1)
    Author:Bin Wang(binwang.0213@gmail.com)
    Date: Sep. 2018
    """
    if(abs(Pillar[1][2]-Pillar[0][2]) > 1e-8):
        k = (z-Pillar[0][2])/(Pillar[1][2]-Pillar[0][2])
    else:  # Degenrated cell
        k = 0.0

    x = Pillar[0][0]+k*(Pillar[1][0]-Pillar[0][0])
    y = Pillar[0][1]+k*(Pillar[1][1]-Pillar[0][1])

    return np.array([x, y, z])


def __getCellZ(i, j, k, grd: Grid):
    """Get the Z coords for a cell

    Follow getCornerPointCellIdx convention:
    Z, [0,1,2,3,4,5,6,7]
    Author:Bin Wang(binwang.0213@gmail.com)
    Date: Sep. 2018
    """
    CellIds = __getCornerPointCellIdx(i, j, k, grd)
    return [grd.zcorn[i] for i in CellIds]


def __getCornerPointCellIdx(i, j, k, grd: Grid):
    """Obtain the eight coords index for a cell
    3x3x1 system (2D X-Y plane)
    30---31,32---33,34---35
    |      |       |      |  <- Cell 6,7,8
    24---25,26---27,28---29
    18---19,20---21,22---23
    |      |       |      |  <- Cell 3,4,5
    12---13,14---15,16---17
    6 --- 7,8 --- 9,10---11
    |      |       |      |  <- Cell 0,1,2
    0 --- 1,2 --- 3,4 --- 5
    Node order convention for a 3D cell
     6----7
     -   -   <-Bottom Face
    4----5
      2----3
     -    -  <-Top Face
    0----1
    Author:Bin Wang(binwang.0213@gmail.com)
    Date: Sep. 2018
    """
    nx, ny, nz = 2*grd.nx, 2*grd.ny, 2*grd.nz

    p1_id, p2_id = __getIJK(2*i, 2*j, 2*k, nx, ny,
                            nz), __getIJK(2*i+1, 2*j, 2*k, nx, ny, nz)
    p3_id, p4_id = __getIJK(2*i, 2*j+1, 2*k, nx, ny,
                            nz), __getIJK(2*i+1, 2*j+1, 2*k, nx, ny, nz)

    p5_id, p6_id = __getIJK(2*i, 2*j, 2*k+1, nx, ny,
                            nz), __getIJK(2*i+1, 2*j, 2*k+1, nx, ny, nz)
    p7_id, p8_id = __getIJK(2*i, 2*j+1, 2*k+1, nx, ny,
                            nz), __getIJK(2*i+1, 2*j+1, 2*k+1, nx, ny, nz)

    # print(p1_id,p2_id,p3_id,p4_id)#Top Layer
    # print(p5_id,p6_id,p7_id,p8_id)#Bottom Layer

    return p1_id, p2_id, p3_id, p4_id, p5_id, p6_id, p7_id, p8_id


def __getCellPillars(i, j, grd: Grid):
    """Obtain the four pillars (p0,p1,p2,p3) of a corner point cell
    The index of pillar

    3x3x1 system (2D X-Y plane)
    12--- 13  --- 14  ---15
    |      |       |      |  <- Cell 6,7,8
    8 ---  9  --- 10  ---11
    |      |       |      |  <- Cell 3,4,5
    4 ---  5  ---  6  --- 7
    |      |       |      |  <- Cell 0,1,2
    0 ---  1 ---   2 ---  3


    The pillars index for a grid follows below ordering (XY Plane)
    pil2   pil3
    *------*
    |      |
    |      |
    *------*
    pil0   pil1
    0   12  3
    1. neighboring cell share one common edge index
    2. ZCORN follows the same order for a cell
    3. Try a 3x3x1 grid system using mrst
    Author:Bin Wang(binwang.0213@gmail.com)
    Date: Sep. 2018
    """
    nx, ny = grd.nx+1, grd.ny+1
    pil0_id, pil1_id = __getIJK(
        i, j, 0, nx, ny, 0), __getIJK(i+1, j, 0, nx, ny, 0)
    pil2_id, pil3_id = __getIJK(
        i, j+1, 0, nx, ny, 0), __getIJK(i+1, j+1, 0, nx, ny, 0)

    return [__getPillar(pil0_id, grd), __getPillar(pil1_id, grd), __getPillar(pil2_id, grd), __getPillar(pil3_id, grd)]


def __getIJK(i, j, k, NX, NY, NZ):
    # Convert index [i,j,k] to a flat 3D matrix index [ijk]
    return i + (NX)*(j + k*(NY))


def __getPillar(Pid, grd: Grid):
    """Get a pillar line from COORD
    Pillar is the vertical cell edge line (top point-bottm point)

    IndexMap of COORD
    [Row1] xtop ytop ztop xbottom ybottom zbottom
    [Row2] xtop ytop ztop xbottom ybottom zbottom
    ....
    Row follows an order of X->Y->Z
    Arguments
    ---------
    Pid -- Pillar index in [COORD]
    Author:Bin Wang(binwang.0213@gmail.com)
    Date: Sep. 2018
    """
    id_top = [6*Pid+0, 6*Pid+1, 6*Pid+2]
    id_bottom = [6*Pid+3, 6*Pid+4, 6*Pid+5]
    TopPoint = np.array([grd.coord[i] for i in id_top])
    BottomPoint = np.array([grd.coord[i] for i in id_bottom])
    return [TopPoint, BottomPoint]
