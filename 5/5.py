import sys
from collections import defaultdict, namedtuple


Point = namedtuple("Point", ["x", "y"])


class LineSegment(namedtuple("LineSegment", ["orientation", "start", "end"])):
    __slots__ = ()

    def range(self):
        """Returns a generator over the points contained in the line segment."""
        if self.orientation == "north":
            return self._iterate_points(self.start, self.end, lambda p: Point(p.x, p.y+1))
        elif self.orientation == "east":
            return self._iterate_points(self.start, self.end, lambda p: Point(p.x+1, p.y))
        elif self.orientation == "northeast":
            return self._iterate_points(self.start, self.end, lambda p: Point(p.x+1, p.y+1))
        elif self.orientation == "southeast":
            return self._iterate_points(self.start, self.end, lambda p: Point(p.x+1, p.y-1))
    
    @staticmethod
    def _iterate_points(start, end, next_func):
        """Iterate from start to end using the given next_func to get the next point."""
        current_point = start
        while current_point != end:
            yield current_point
            current_point = next_func(current_point)
        yield current_point


def parse_line_segment(line_seg_string):
    """Parse an input line segment."""
    start, end = line_seg_string.split(" -> ")
    start = [int(n) for n in start.split(",")]
    start = Point(start[0], start[1])
    end = [int(n) for n in end.split(",")]
    end = Point(end[0], end[1])
    if start.x == end.x:
        if start.y < end.y:
            return LineSegment("north", start, end)
        return LineSegment("north", end, start)
    elif start.y == end.y:
        if start.x < end.x:
            return LineSegment("east", start, end)
        return LineSegment("east", end, start)
    # 4 diagonal cases: oriented northwest, northeast, southwest, southeast.
    if start.x < end.x and start.y < end.y:
        return LineSegment("northeast", start, end)
    elif start.x > end.x and start.y > end.y:
        return LineSegment("northeast", end, start)
    elif start.x < end.x and start.y > end.y:
        return LineSegment("southeast", start, end)
    elif start.x > end.x and start.y < end.y:
        return LineSegment("southeast", end, start)
    
    raise ValueError(f"Uncovered case: {start} {end}")


def partn(line_segments, orientations):
    """Part n of day 5."""
    points = defaultdict(int)
    for line_segment in line_segments:
        if line_segment.orientation not in orientations:
            continue    
        for point in line_segment.range():
            points[point] += 1
    num_overlaps = 0
    for point, overlap_count in points.items():
        if overlap_count > 1:
            num_overlaps += 1
    print(num_overlaps)


def part1(line_segments):
    """Part 1 of day 5."""
    partn(line_segments, {"north", "east"})


def part2(line_segments):
    """Part 2 of day 5."""
    partn(line_segments, {"north", "east", "northeast", "southeast"})


def main():
    """Day 5 of Advent of Code."""
    line_segments = [parse_line_segment(line) for line in sys.stdin.readlines()]
    part1(line_segments)
    part2(line_segments)


main()