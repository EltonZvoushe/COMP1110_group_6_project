
import pytest

from project import (
    Match,
    calculate_outcome_percentages,
    count_outcomes,
    count_total_matches,
    filter_team_matches,
    get_match_result,
)


def make_matches():
    """Build a small, fixed list of matches for the tests."""
    return [
        Match('Arsenal', 'Chelsea', 2, 1),   # Arsenal home win
        Match('Arsenal', 'Spurs', 1, 1),     # Arsenal home draw
        Match('Arsenal', 'Everton', 0, 2),   # Arsenal home loss
        Match('Arsenal', 'Wolves', 3, 0),    # Arsenal home win
        Match('Chelsea', 'Arsenal', 0, 0),   # Arsenal away draw
        Match('Everton', 'Arsenal', 2, 0),   # Arsenal away loss
        Match('Spurs', 'Chelsea', 1, 0),     # Arsenal not involved
    ]


def test_filter_team_matches():
    matches = make_matches()
    home = filter_team_matches(matches, 'Arsenal', 'Home')
    away = filter_team_matches(matches, 'Arsenal', 'Away')
    assert len(home) == 4
    assert len(away) == 2
    assert all(match.home_team == 'Arsenal' for match in home)
    assert all(match.away_team == 'Arsenal' for match in away)
    assert filter_team_matches(matches, 'Fulham', 'Home') == []
    with pytest.raises(ValueError):
        filter_team_matches(matches, 'Arsenal', 'Neutral')


def test_get_match_result():
    win = Match('Arsenal', 'Chelsea', 2, 1)
    draw = Match('Arsenal', 'Chelsea', 1, 1)
    assert get_match_result(win, 'Home') == 'W'
    assert get_match_result(win, 'Away') == 'L'
    assert get_match_result(draw, 'Home') == 'D'
    assert get_match_result(draw, 'Away') == 'D'
    with pytest.raises(ValueError):
        get_match_result(win, 'Neutral')


def test_count_outcomes():
    matches = make_matches()
    home = filter_team_matches(matches, 'Arsenal', 'Home')
    away = filter_team_matches(matches, 'Arsenal', 'Away')
    assert count_outcomes(home, 'Home') == {
        'wins': 2, 'draws': 1, 'losses': 1}
    assert count_outcomes(away, 'Away') == {
        'wins': 0, 'draws': 1, 'losses': 1}
    assert count_outcomes([], 'Home') == {
        'wins': 0, 'draws': 0, 'losses': 0}


def test_calculate_outcome_percentages():
    outcomes = {'wins': 2, 'draws': 1, 'losses': 1}
    assert calculate_outcome_percentages(outcomes) == {
        'win_pct': 50.0, 'draw_pct': 25.0, 'loss_pct': 25.0}
    thirds = {'wins': 1, 'draws': 1, 'losses': 1}
    assert calculate_outcome_percentages(thirds)['win_pct'] == 33.3
    empty = {'wins': 0, 'draws': 0, 'losses': 0}
    assert calculate_outcome_percentages(empty) == {
        'win_pct': 0.0, 'draw_pct': 0.0, 'loss_pct': 0.0}


def test_count_total_matches():
    assert count_total_matches({'wins': 2, 'draws': 1, 'losses': 1}) == 4
    assert count_total_matches({'wins': 0, 'draws': 0, 'losses': 0}) == 0


def test_away_percentages_end_to_end():
    matches = make_matches()
    away = filter_team_matches(matches, 'Arsenal', 'Away')
    outcomes = count_outcomes(away, 'Away')
    assert calculate_outcome_percentages(outcomes) == {
        'win_pct': 0.0, 'draw_pct': 50.0, 'loss_pct': 50.0}
