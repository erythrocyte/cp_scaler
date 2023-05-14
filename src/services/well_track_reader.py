import logging
from src.models import well_track, track_point


def read_well_track(fn: str) -> well_track.WellTrack:
    if not fn:
        logging.error(f'well track file {fn} is invalid')
        return None

    result = well_track.WellTrack()

    f = open(fn)

    while True:
        line = f.readline()

        # if line is empty
        # end of file is reached
        if not line:
            break

        if line.startswith('--'):
            continue

        vals = list(map(float, line.split()))
        p = track_point.TrackPoint()
        p.x = vals[0]
        p.y = vals[1]
        p.z = vals[2]

        result.points.append(p)
    
    return result 

