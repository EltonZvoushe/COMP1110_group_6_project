##Premier League Matchup Analyzer - Elton's section.
My functions work on Match objects (created by Sean's load_matches)
and produce the win/draw/loss counts and percentages that Samuel's
build_team_summary combines into a team summary.##

VALID_VENUES = ('Home', 'Away')
class Match:
    ##Minimal stand-in for Sean's Match class (same attribute names).

    Sean's real class will also hold shots, corners, fouls and cards.
    ##

    def __init__(self, home_team, away_team, home_goals, away_goals):
        self.home_team = home_team
        self.away_team = away_team
        self.home_goals = home_goals
        self.away_goals = away_goals


def filter_team_matches(matches, team, venue):
   ##Return the matches that `team` played in the given venue.

    venue must be 'Home' or 'Away'. A team is only kept when it was the
    home side (venue 'Home') or the away side (venue 'Away').
    ##
    if venue not in VALID_VENUES:
        raise ValueError('venue must be "Home" or "Away"')

    selected = []
    for match in matches:
        if venue == 'Home' and match.home_team == team:
            selected.append(match)
        elif venue == 'Away' and match.away_team == team:
            selected.append(match)
    return selected


def get_match_result(match, venue):
    ##Return 'W', 'D' or 'L' from the point of view of the venue side.##
    if venue == 'Home':
        goals_for = match.home_goals
        goals_against = match.away_goals
    elif venue == 'Away':
        goals_for = match.away_goals
        goals_against = match.home_goals
    else:
        raise ValueError('venue must be "Home" or "Away"')

    if goals_for > goals_against:
        return 'W'
    if goals_for < goals_against:
        return 'L'
    return 'D'


def count_outcomes(team_matches, venue):
    ##Count wins, draws and losses for a list of one team's matches.
    team_matches should come from filter_team_matches, and venue must be
    the same venue used there so the result is judged from the right side.
    Returns a dictionary: {'wins': int, 'draws': int, 'losses': int}.
   ##
    outcomes = {'wins': 0, 'draws': 0, 'losses': 0}
    for match in team_matches:
        result = get_match_result(match, venue)
        if result == 'W':
            outcomes['wins'] += 1
        elif result == 'D':
            outcomes['draws'] += 1
        else:
            outcomes['losses'] += 1
    return outcomes


def count_total_matches(outcomes):
    ##Return the total number of matches in an outcomes dictionary.##
    return outcomes['wins'] + outcomes['draws'] + outcomes['losses']


def calculate_outcome_percentages(outcomes):
    ##Turn win/draw/loss counts into percentages rounded to 1 decimal.
    Returns {'win_pct': float, 'draw_pct': float, 'loss_pct': float}.
    If there are no matches, every percentage is 0.0 (guardian check, so
    we never divide by zero).
    ##
    total = count_total_matches(outcomes)
    if total == 0:
        return {'win_pct': 0.0, 'draw_pct': 0.0, 'loss_pct': 0.0}

    return {
        'win_pct': round(outcomes['wins'] / total * 100, 1),
        'draw_pct': round(outcomes['draws'] / total * 100, 1),
        'loss_pct': round(outcomes['losses'] / total * 100, 1),
    }





if __name__ == "__main__":
    main()
