from typing import List
from src.grid import Grid
from src.cube import Cube
import os.path


def read_grid(fn: str) -> Grid:
    grd = Grid()
    return __read_file(fn, grd)

def read_coord(fn: str):
    file = open(fn)
    coord = __readSection(file)
    file.close()

    return coord

def __read_file(fn: str, grd: Grid):
    gridfile = open(fn)

    for line in gridfile:
        if line.startswith('--') or not line.strip():
            # skip comments and blank lines
            continue
        elif line.startswith('PINCH'):
            __skipSection(gridfile)
        elif line.startswith('MAPUNITS'):
            __skipSection(gridfile)
        elif line.startswith('MAPAXES'):
            __skipSection(gridfile)
        elif line.startswith('GRIDUNIT'):
            __skipSection(gridfile)
        elif line.startswith('COORDSYS'):
            __skipSection(gridfile)
        elif line.startswith('INCLUDE'):
            include_fn = next(gridfile)
            include_fn = include_fn.replace('\'', '')
            include_fn = include_fn.strip()
            d = os.path.dirname(fn)
            include_fn = os.path.join(d, include_fn)
            grd = __read_file(include_fn, grd)
        elif line.startswith('SPECGRID'):
            nx, ny, nz = next(gridfile).split()[0:3]
            grd.nx = int(nx)
            grd.ny = int(ny)
            grd.nz = int(nz)
        elif line.startswith('COORD'):
            grd.coord = __readSection(gridfile)
        elif line.startswith('ZCORN'):
            grd.zcorn = __readSection(gridfile)

        elif line.startswith('ACTNUM'):
            grd.cubes.append(__readScalarSection('ACTNUM', gridfile))
        elif line.startswith('EQLNUM'):
            grd.cubes.append(__readScalarSection('EQLNUM', gridfile))
        elif line.startswith('SATNUM'):
            grd.cubes.append(__readScalarSection('SATNUM', gridfile))
        elif line.startswith('FIPNUM'):
            grd.cubes.append(__readScalarSection('FIPNUM', gridfile))
        elif line.startswith('PERMX'):
            grd.cubes.append(__readScalarSection('PERMX', gridfile))
        elif line.startswith('PERMY'):
            grd.cubes.append(__readScalarSection('PERMY', gridfile))
        elif line.startswith('PERMZ'):
            grd.cubes.append(__readScalarSection('PERMZ', gridfile))
        elif line.startswith('PORO'):
            grd.cubes.append(__readScalarSection('PORO', gridfile))
        else:
            print("else section: {}".format(line[:8]))

    gridfile.close()

    return grd


def __readScalarSection(name, f):
    '''Reads a section of scalars, adds them to the unstructured
    grid array.'''

    scalars = __readSection(f)
    cube = Cube()
    cube.values = scalars
    cube.name = name

    return cube


def __skipSection(f):
    '''Skips over an unprocessed section.'''
    while True:
        line = next(f).rstrip()
        if line.endswith('/'):
            return


def __readSection(f):
    '''Reads a data section and returns an expanded array.'''
    section = []
    while True:
        line = next(f)
        if line.startswith('--'):
            continue
        if any(c.isalpha() for c in line):
            continue
        vals = __convertTokens(line)
        if len(vals) == 0:
            continue
        section.extend(vals)
        if section[-1] == '/':
            section.pop()
            section = list(map(float, section))
            break
    return section


def __convertTokens(line):
    '''Expands tokens of the type N*data to N copies of data.'''
    values = []
    for t in line.split():
        if t.find('*') == -1:
            values.append(t)
        else:
            run = t.split('*')
            inflation = [run[1]] * int(run[0])
            values.extend(inflation)

    return values
