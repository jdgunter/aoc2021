import sys


class FishPopTable:

    def __init__(self, days_until_mature, reproduction_time, max_days):
        """Initialize a fish population table."""
        self.reproduction_time = reproduction_time
        self.days_until_mature = days_until_mature
        self.pop_counts = [[None for _ in range(max_days + 1)] for _ in range(days_until_mature)]
        # Fill in the base cases: after 0 days, every kind of fish has spawned 0 new fish.
        for t in range(days_until_mature):
            self.pop_counts[t][0] = 1
    
    def get(self, init_internal_timer, day):
        """
        Get the population count for a fish starting with a value of 'init_interal_timer'
        for its internal time after 'day' days.
        """
        if self.pop_counts[init_internal_timer][day]:
            return self.pop_counts[init_internal_timer][day]
        
        if init_internal_timer == 0:
            value = self.get(self.days_until_mature-1, day-1) + self.get(self.reproduction_time-1, day-1)
        else:
            value = self.get(init_internal_timer-1, day-1)
        self.pop_counts[init_internal_timer][day] = value
        return self.pop_counts[init_internal_timer][day]
    
    def population_count(self, initial_internal_timers, num_days):
        """
        Get the population count of a school of fish with the given internal timers
        after the given number of days have passed.
        """
        total_pop = 0
        for internal_timer in initial_internal_timers:
            total_pop += self.get(internal_timer, num_days)
        return total_pop


def main():
    """Day 6 of Advent of Code."""
    input_internal_timers = [int(n) for n in sys.stdin.read().split(",")]
    fish_pop_table = FishPopTable(9, 7, 256)
    # Part 1.
    print(fish_pop_table.population_count(input_internal_timers, 80))
    # Part 2.
    print(fish_pop_table.population_count(input_internal_timers, 256))
        

main()