"""CS 61A Presents The Game of Hog."""

from dice import four_sided, six_sided, make_test_dice
from ucb import main, trace, log_current_line, interact

GOAL_SCORE = 100  # The goal of Hog is to score 100 points.


######################
# Phase 1: Simulator #
######################

def roll_dice(num_rolls, dice=six_sided):
    """Simulate rolling the DICE exactly NUM_ROLLS>0 times. Return the sum of
    the outcomes unless any of the outcomes is 1. In that case, return the
    number of 1's rolled.
    """
    # These assert statements ensure that num_rolls is a positive integer.
    assert type(num_rolls) == int, 'num_rolls must be an integer.'
    assert num_rolls > 0, 'Must roll at least once.'
    # BEGIN PROBLEM 1
    sum_outcomes = 0
    num_ones = 0

    # Roll dice 'num_rolls' times
    while (num_rolls > 0):
        outcome = dice()  # Roll once
        if (outcome == 1):
            num_ones += 1
        else:
            sum_outcomes += outcome
        num_rolls -= 1

    # Return score based on whether any of the outcomes was a 1
    if (num_ones > 0):  # One or more of the outcomes was a 1
        return num_ones  # Return number of ones rolled (Pig Out)
    else:  # None of the outcomes was a 1
        return sum_outcomes  # Return sum of outcomes

    # END PROBLEM 1


def free_bacon(opponent_score):
    """Return the points scored from rolling 0 dice (Free Bacon)."""
    # BEGIN PROBLEM 2
    # Handle scores less than 100
    assert(opponent_score < 100)

    # Isolate units digit from tens digit (assumes that 'opponent_score' is less than 100)
    units_dig = opponent_score - ((opponent_score // 10) * 10)
    tens_dig = (opponent_score - units_dig) // 10

    # Return largest digit in opponent's score, plus 1
    return (max(units_dig, tens_dig) + 1)

    # END PROBLEM 2


# Write your prime functions here!

# Returns whether a number is prime
def is_prime(n):
    if (n == 1):
        return False  # By definition, 1 is not prime

    divisor = 2;  # Divisor to test, starting at 2
    while (divisor <= (n // 2)):  # There are divisors remaining to test
        if ((n % divisor) == 0):  # Remainder is zero; 'n' has a divisor
            return False  # Not prime
        else:  # Remainder is non-zero
            divisor += 1  # Test next divisor
    return True  # No divisors remaining; 'n' is prime

# Given a number, prime or not, returns the next larger number that is prime
def next_prime(n):
    n += 1
    while (not is_prime(n)):
        n += 1
    return n

def take_turn(num_rolls, opponent_score, dice=six_sided):
    """Simulate a turn rolling NUM_ROLLS dice, which may be 0 (Free Bacon).
    Return the points scored for the turn by the current player. Also
    implements the Hogtimus Prime and When Pigs Fly rules.

    num_rolls:       The number of dice rolls that will be made.
    opponent_score:  The total score of the opponent.
    dice:            A function of no args that returns an integer outcome.
    """
    # Leave these assert statements here; they help check for errors.
    assert type(num_rolls) == int, 'num_rolls must be an integer.'
    assert num_rolls >= 0, 'Cannot roll a negative number of dice in take_turn.'
    assert num_rolls <= 10, 'Cannot roll more than 10 dice.'
    assert opponent_score < 100, 'The game should be over.'
    # BEGIN PROBLEM 2
    score = 0

    # Free Bacon
    if (num_rolls == 0):
        score = free_bacon(opponent_score)
    else:
        score = roll_dice(num_rolls, dice)

    # Hogtimus Prime
    if (is_prime(score)):
        score = next_prime(score)

    # When Pigs Fly
    return min(25 - num_rolls, score)

    # END PROBLEM 2


def reroll(dice):
    """Return dice that return even outcomes and re-roll odd outcomes of DICE."""
    def rerolled():
        # BEGIN PROBLEM 3
        outcome = dice();  # Initial roll
        if ((outcome % 2) == 0):  # Even outcome
            return outcome;
        else:  # Odd outcome
            outcome = dice();  # Roll again, discarding previous outcome
            return outcome;  # Return next outcome
        # END PROBLEM 3
    return rerolled


def select_dice(score, opponent_score, dice_swapped):
    """Return the dice used for a turn, which may be re-rolled (Hog Wild) and/or
    swapped for four-sided dice (Pork Chop).

    DICE_SWAPPED is True if and only if four-sided dice are being used.
    """
    # BEGIN PROBLEM 4
    dice = six_sided
    if (dice_swapped):  # Pork Chop (player chose to roll -1 dice)
        dice = four_sided  # Replace six-sided dice with four-sided dice
    # END PROBLEM 4
    if (score + opponent_score) % 7 == 0:
        dice = reroll(dice)
    return dice


def other(player):
    """Return the other player, for a player PLAYER numbered 0 or 1.

    >>> other(0)
    1
    >>> other(1)
    0
    """
    return 1 - player


def play(strategy0, strategy1, score0=0, score1=0, goal=GOAL_SCORE):
    """Simulate a game and return the final scores of both players, with
    Player 0's score first, and Player 1's score second.

    A strategy is a function that takes two total scores as arguments
    (the current player's score, and the opponent's score), and returns a
    number of dice that the current player will roll this turn.

    strategy0:  The strategy function for Player 0, who plays first
    strategy1:  The strategy function for Player 1, who plays second
    score0   :  The starting score for Player 0
    score1   :  The starting score for Player 1
    """
    player = 0  # Which player is about to take a turn, 0 (first) or 1 (second)
    dice_swapped = False  # Whether 4-sided dice have been swapped for 6-sided
    # BEGIN PROBLEM 5
    debug = False  # Whether to print verbose debugging messages and limit number of turns
    debug_turn_cap = 5  # Limit on number of turns when debugging

    dice = select_dice(score0, score1, dice_swapped)  # Initial dice

    if (debug):
        print("Initial scores: Player 0 ", score0, ", player 1 ", score1)
        print("Goal: ", goal)
        print("")

    turn_count = 0
    while (score0 < goal) and (score1 < goal):  # Game ends when one player's score reaches 'goal'
        if (debug):
            if (turn_count >= debug_turn_cap): break
            print("Turn ", turn_count, ", player ", player, "'s turn.  Player 0 ", score0, ", player 1 ", score1)
        assert(score0 >= 0)
        assert(score1 >= 0)

        # Determine who is "current player" and who is "opponent", and whose strategy to use in this turn
        if (player == 0):  # Player 0's turn
            cur_player_score = score0
            opponent_score = score1
            strategy = strategy0
        else:  # Player 1's turn
            cur_player_score = score1
            opponent_score = score0
            strategy = strategy1
        if (debug):
            print("Current player's score ", cur_player_score, ", opponent's score ", opponent_score)

        # Execute current player's strategy to determine number of rolls
        num_rolls = strategy(cur_player_score, opponent_score)
        if (debug): print("Number of rolls: ", num_rolls)

        # 'Pork Chop' rule
        if (num_rolls == -1):  # Player chose to roll -1 dice
            # Apply 'Pork Chop' rule
            if (debug): print("Player ", player, " chose to roll -1 dice; 'Pork Chop' rule will apply.")
            dice_swapped = not dice_swapped
            turn_score = 1  # Score 1 point for turn
        else:  # 'Pork Chop' rule does not apply
            # Select dice, applying 'Hog Wild' rule
            dice = select_dice(cur_player_score, opponent_score, dice_swapped)

            # Take turn using selected dice
            turn_score = take_turn(num_rolls, opponent_score, dice)

        # Add turn score to player's score
        if (debug): print("Turn score: ", turn_score)
        cur_player_score += turn_score
        if (debug): print("Current player's score is now: ", cur_player_score)

        # Apply 'Swine Swap' rule
        if (cur_player_score == (opponent_score * 2)) or (opponent_score == (cur_player_score * 2)):
            if (debug): print("Applying 'Swine Swap' rule...")

            # Swap scores of the two players
            cur_player_score_temp = cur_player_score  # Temporary holder for current player's score
            cur_player_score = opponent_score
            opponent_score = cur_player_score_temp

        # Update player scores
        if (player == 0):  # Player 0's turn
            score0 = cur_player_score
            score1 = opponent_score
        else:  # Player 1's turn
            score1 = cur_player_score
            score0 = opponent_score

        # Turn complete
        turn_count += 1  # Increment turn count for debugging purposes
        player = other(player)  # Switch players
    # END PROBLEM 5
    return score0, score1


#######################
# Phase 2: Strategies #
#######################

def always_roll(n):
    """Return a strategy that always rolls N dice.

    A strategy is a function that takes two total scores as arguments
    (the current player's score, and the opponent's score), and returns a
    number of dice that the current player will roll this turn.

    >>> strategy = always_roll(5)
    >>> strategy(0, 0)
    5
    >>> strategy(99, 99)
    5
    """
    def strategy(score, opponent_score):
        return n
    return strategy


def check_strategy_roll(score, opponent_score, num_rolls):
    """Raises an error with a helpful message if NUM_ROLLS is an invalid
    strategy output. All strategy outputs must be integers from -1 to 10.

    >>> check_strategy_roll(10, 20, num_rolls=100)
    Traceback (most recent call last):
     ...
    AssertionError: strategy(10, 20) returned 100 (invalid number of rolls)

    >>> check_strategy_roll(20, 10, num_rolls=0.1)
    Traceback (most recent call last):
     ...
    AssertionError: strategy(20, 10) returned 0.1 (not an integer)

    >>> check_strategy_roll(0, 0, num_rolls=None)
    Traceback (most recent call last):
     ...
    AssertionError: strategy(0, 0) returned None (not an integer)
    """
    msg = 'strategy({}, {}) returned {}'.format(
        score, opponent_score, num_rolls)
    assert type(num_rolls) == int, msg + ' (not an integer)'
    assert -1 <= num_rolls <= 10, msg + ' (invalid number of rolls)'


def check_strategy(strategy, goal=GOAL_SCORE):
    """Checks the strategy with all valid inputs and verifies that the
    strategy returns a valid input. Use `check_strategy_roll` to raise
    an error with a helpful message if the strategy returns an invalid
    output.

    >>> def fail_15_20(score, opponent_score):
    ...     if score != 15 or opponent_score != 20:
    ...         return 5
    ...
    >>> check_strategy(fail_15_20)
    Traceback (most recent call last):
     ...
    AssertionError: strategy(15, 20) returned None (not an integer)
    >>> def fail_102_115(score, opponent_score):
    ...     if score == 102 and opponent_score == 115:
    ...         return 100
    ...     return 5
    ...
    >>> check_strategy(fail_102_115)
    >>> fail_102_115 == check_strategy(fail_102_115, 120)
    Traceback (most recent call last):
     ...
    AssertionError: strategy(102, 115) returned 100 (invalid number of rolls)
    """
    # BEGIN PROBLEM 6
    for score0 in range(0, goal):
        for score1 in range(0, goal):
            num_rolls = strategy(score0, score1)
            check_strategy_roll(score0, score1, num_rolls)
    return None  # All possible valid inputs tested, with no invalid output detected
    # END PROBLEM 6


# Experiments

def make_averaged(fn, num_samples=1000):
    """Return a function that returns the average_value of FN when called.

    To implement this function, you will have to use *args syntax, a new Python
    feature introduced in this project.  See the project description.

    >>> dice = make_test_dice(3, 1, 5, 6)
    >>> averaged_dice = make_averaged(dice, 1000)
    >>> averaged_dice()
    3.75
    """
    # BEGIN PROBLEM 7
    "*** REPLACE THIS LINE ***"
    # END PROBLEM 7


def max_scoring_num_rolls(dice=six_sided, num_samples=1000):
    """Return the number of dice (1 to 10) that gives the highest average turn
    score by calling roll_dice with the provided DICE over NUM_SAMPLES times.
    Assume that the dice always return positive outcomes.

    >>> dice = make_test_dice(3)
    >>> max_scoring_num_rolls(dice)
    10
    """
    # BEGIN PROBLEM 8
    "*** REPLACE THIS LINE ***"
    # END PROBLEM 8


def winner(strategy0, strategy1):
    """Return 0 if strategy0 wins against strategy1, and 1 otherwise."""
    score0, score1 = play(strategy0, strategy1)
    if score0 > score1:
        return 0
    else:
        return 1


def average_win_rate(strategy, baseline=always_roll(4)):
    """Return the average win rate of STRATEGY against BASELINE. Averages the
    winrate when starting the game as player 0 and as player 1.
    """
    win_rate_as_player_0 = 1 - make_averaged(winner)(strategy, baseline)
    win_rate_as_player_1 = make_averaged(winner)(baseline, strategy)

    return (win_rate_as_player_0 + win_rate_as_player_1) / 2


def run_experiments():
    """Run a series of strategy experiments and report results."""
    if True:  # Change to False when done finding max_scoring_num_rolls
        six_sided_max = max_scoring_num_rolls(six_sided)
        print('Max scoring num rolls for six-sided dice:', six_sided_max)
        rerolled_max = max_scoring_num_rolls(reroll(six_sided))
        print('Max scoring num rolls for re-rolled dice:', rerolled_max)

    if False:  # Change to True to test always_roll(8)
        print('always_roll(8) win rate:', average_win_rate(always_roll(8)))

    if False:  # Change to True to test bacon_strategy
        print('bacon_strategy win rate:', average_win_rate(bacon_strategy))

    if False:  # Change to True to test swap_strategy
        print('swap_strategy win rate:', average_win_rate(swap_strategy))

    "*** You may add additional experiments as you wish ***"


# Strategies

def bacon_strategy(score, opponent_score, margin=8, num_rolls=4):
    """This strategy rolls 0 dice if that gives at least MARGIN points,
    and rolls NUM_ROLLS otherwise.
    """
    # BEGIN PROBLEM 9
    "*** REPLACE THIS LINE ***"
    return 4  # Replace this statement
    # END PROBLEM 9
check_strategy(bacon_strategy)


def swap_strategy(score, opponent_score, margin=8, num_rolls=4):
    """This strategy rolls 0 dice when it triggers a beneficial swap. It also
    rolls 0 dice if it gives at least MARGIN points. Otherwise, it rolls
    NUM_ROLLS.
    """
    # BEGIN PROBLEM 10
    "*** REPLACE THIS LINE ***"
    return 4  # Replace this statement
    # END PROBLEM 10
check_strategy(swap_strategy)


def final_strategy(score, opponent_score):
    """Write a brief description of your final strategy.

    *** YOUR DESCRIPTION HERE ***
    """
    # BEGIN PROBLEM 11
    "*** REPLACE THIS LINE ***"
    return 4  # Replace this statement
    # END PROBLEM 11
check_strategy(final_strategy)


##########################
# Command Line Interface #
##########################

# NOTE: Functions in this section do not need to be changed. They use features
# of Python not yet covered in the course.

@main
def run(*args):
    """Read in the command-line argument and calls corresponding functions.

    This function uses Python syntax/techniques not yet covered in this course.
    """
    import argparse
    parser = argparse.ArgumentParser(description="Play Hog")
    parser.add_argument('--run_experiments', '-r', action='store_true',
                        help='Runs strategy experiments')

    args = parser.parse_args()

    if args.run_experiments:
        run_experiments()
