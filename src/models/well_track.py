from typing import List


class WellTrack:
    def __init__(self) -> None:
        self.points = []

    def get_point_list(self, index: int) -> List[float]:
        if (index >= len(self.points)):
            return None
        
        p = self.points[index]
        return [p.x, p.y, p.z]
