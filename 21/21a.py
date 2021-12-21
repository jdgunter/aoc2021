from dataclasses import dataclass
from typing import Dict, Union


@dataclass
class DeterministicDie:
    current: int
    max_value: int

    def roll(self):
        """Roll the die and increment its state."""
        roll = self.current
        if self.current == self.max_value:
            self.current = 0
        self.current += 1
        return roll


INVERSE = {1:2, 2:1}


@dataclass
class DiracDice:
    current_player: int
    player_scores: Dict[int, int]
    player_positions: Dict[int, int]
    loser: Union[int, None]
    die: DeterministicDie
    die_rolls: int

    def has_ended(self):
        """
        If the game has ended, first mark the game's loser then return True. Return False otherwise.
        """
        for player, score in self.player_scores.items():
            if score >= 1000:
                self.loser = INVERSE[player]
                return True
        return False

    def take_turn(self, player):
        """Take a turn for the given player."""
        distance = self.die.roll() + self.die.roll() + self.die.roll()
        self.die_rolls += 3
        self.player_positions[player] = (self.player_positions[player] + distance) % 10
        self.player_scores[player] += self.player_positions[player] + 1

    def play(self):
        """
        Play a game of Dirac Dice.
        
        Returns the score of the losing player multiplied by the number of die rolls.
        """
        while not self.has_ended():
            self.take_turn(self.current_player)
            self.current_player = INVERSE[self.current_player]
        return self.die_rolls * self.player_scores[self.loser]


def main():
    """Advent of Code Day 21."""
    die = DeterministicDie(1, 100)
    game = DiracDice(
        current_player=1,
        player_scores={1: 0, 2: 0},
        player_positions={1: 9, 2: 6},
        loser=None,
        die=die,
        die_rolls=0)
    print(game.play())


main()
        