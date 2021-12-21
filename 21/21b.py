from collections import namedtuple


GameState = namedtuple("GameState", ["p1_score", "p2_score", "p1_pos", "p2_pos", "player_on_turn", "rolls_left_in_turn"])


PREVIOUSLY_SEEN_GAME_STATES = {}


def sum_wins(d1, d2, d3):
    """Sum number of wins in the three dictionaries."""
    return {
        1: d1[1] + d2[1] + d3[1], 
        2: d1[2] + d2[2] + d3[2],
    }


def gamestate_after_rolling(gamestate, die_roll):
    """Get the next game state after the given value is rolled."""
    if gamestate.player_on_turn == 1:
        return gamestate._replace(
            p1_pos=(gamestate.p1_pos + die_roll) % 10, 
            rolls_left_in_turn=gamestate.rolls_left_in_turn - 1)
    elif gamestate.player_on_turn == 2:
        return gamestate._replace(
            p2_pos=(gamestate.p2_pos + die_roll) % 10,
            rolls_left_in_turn=gamestate.rolls_left_in_turn - 1)


def next_turn(gamestate):
    """Get the next game state after handling end-of-turn administrative tasks."""
    if gamestate.player_on_turn == 1:
        return gamestate._replace(
            p1_score=gamestate.p1_score + gamestate.p1_pos + 1,
            player_on_turn=2,
            rolls_left_in_turn=3)
    elif gamestate.player_on_turn == 2:
        return gamestate._replace(
            p2_score=gamestate.p2_score + gamestate.p2_pos + 1,
            player_on_turn=1,
            rolls_left_in_turn=3)


def count_winning_universes(gamestate):
    """Count the number of winning universes for player 1 and 2 that can arise from the given gamestate."""
    if gamestate in PREVIOUSLY_SEEN_GAME_STATES:
        return PREVIOUSLY_SEEN_GAME_STATES[gamestate]
    if gamestate.p1_score >= 21:
        PREVIOUSLY_SEEN_GAME_STATES[gamestate] = {1: 1, 2: 0}
        return PREVIOUSLY_SEEN_GAME_STATES[gamestate]
    if gamestate.p2_score >= 21:
        PREVIOUSLY_SEEN_GAME_STATES[gamestate] = {1: 0, 2: 1}
        return PREVIOUSLY_SEEN_GAME_STATES[gamestate] 
    if gamestate.rolls_left_in_turn == 0:
        winning_universe_counts = count_winning_universes(next_turn(gamestate))
    else:
        winning_universe_counts = sum_wins(
            count_winning_universes(gamestate_after_rolling(gamestate, 1)),
            count_winning_universes(gamestate_after_rolling(gamestate, 2)),
            count_winning_universes(gamestate_after_rolling(gamestate, 3)))
    PREVIOUSLY_SEEN_GAME_STATES[gamestate] = winning_universe_counts
    return PREVIOUSLY_SEEN_GAME_STATES[gamestate]


def main():
    """Advent of Code day 21 part 2."""
    starting_gamestate = GameState(
        p1_score=0,
        p2_score=0,
        p1_pos=(10-1),
        p2_pos=(7-1),
        player_on_turn=1,
        rolls_left_in_turn=3)
    print(count_winning_universes(starting_gamestate))


main()
