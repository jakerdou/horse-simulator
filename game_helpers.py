def game_over(players):
    for player in players:
        if player['misses'] == 5:
            return True
    return False
