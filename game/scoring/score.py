class Score:
    def __init__(self, points, time, name = None):
        if not isinstance(points, int):
            raise ValueError("Invalid data for Score object.")
        self.points = points
        self.time = time
        self.name = name

    def from_dict(data):
        return Score(points=data["points"], time=data["time"], name=data["name"])
    
    def to_dict(self):
        """Convert the Score object to a dictionary."""
        return {
            "time": self.time,
            "points": self.points,
            "name": self.name
        }