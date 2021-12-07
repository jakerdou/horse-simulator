def game_over(players):
    for player in players:
        if player['misses'] == 5:
            return True
    return False

# update shooting statistics
def analysis_update(shotsm, shotsa, tps, tpa):
    string_shotsm = str(shotsm)
    string_shotsa = str(shotsa)
    string_tps = str(tps)
    string_fgp = str(round((shotsm / shotsa) * 100, 1)) + ' %'
    string_threepp = str(round((tps / tpa) * 100, 1)) + ' %'
    string_twopp = str(round(((shotsm - tps) / (shotsa - tpa)) * 100, 1)) + ' %'
    window['shotsm'].update(string_shotsm)
    window['shotsa'].update(string_shotsa)
    window['tps'].update(string_tps)
    window['fgp'].update(string_fgp)
    window['threepp'].update(string_threepp)
    window['twopp'].update(string_twopp)
