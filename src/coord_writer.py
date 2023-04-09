from typing import List


def write(fn: str, coord: List):
    separ = 6 * ' '
    with open(fn, 'w') as f:
        f.write('COORD\n')
        f.write(2 * '\n')
        index = 0
        for i in range(len(coord) // 6):
            f.write(f'{coord[index]:.6f}{separ}')
            f.write(f'{coord[index+1]:.6f}{separ}')
            f.write(f'{coord[index+2]:.6f}{separ}')
            f.write(f'{coord[index+3]:.6f}{separ}')
            f.write(f'{coord[index+4]:.6f}{separ}')
            f.write(f'{coord[index+5]:.6f}\n')
            index += 6
        f.write('/\n')
