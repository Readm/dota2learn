from dota2py import api
import config


class Match():
    def __init__(self, dic):
        self.match_id = dic["match_id"]
        self.start_time = dic["start_time"]
        self.match_seq_num = dic["match_seq_num"]
        self.duration = dic["duration"]
        self.radiant_win = dic["radiant_win"]
        self.lobby_type = dic["lobby_type"]
        self.game_mode = dic["game_mode"]
        self.leaver = False

        radiant_hero = []
        dire_hero = []
        radiant_gold = 0
        dire_gold = 0
        for player in dic["players"]:
            if player["leaver_status"] >1: self.leaver = True
            if player["player_slot"] > 127:  # dire
                radiant_gold += player["gold"]
                radiant_hero.append(player["hero_id"])
            else:
                dire_gold += player["gold"]
                dire_hero.append(player["hero_id"])

        self.radiant_gold = radiant_gold
        self.radiant_hero = radiant_hero
        self.dire_gold = dire_gold
        self.dire_hero = dire_hero

    @classmethod
    def get_match_by_id(cls, match_id):
        key = config.getConfig("key", "key")
        api.set_api_key(key)
        match = api.get_match_details(match_id)
        return Match(match["result"])

    def is_valid(self):
        if self.game_mode not in [1, 2, 3, 5, 8, 22]:
            return False
        if self.leaver:
            return False
        if self.duration < 900:
            return False
        if self.lobby_type not in [0, 2, 5, 7]:
            return False
        return True

    @property
    def sql_data(self):
        return (self.match_id,
                self.match_seq_num,
                self.start_time,
                self.duration,
                self.radiant_win,
                self.lobby_type,
                self.game_mode,
                self.radiant_hero[0],
                self.radiant_hero[1],
                self.radiant_hero[2],
                self.radiant_hero[3],
                self.radiant_hero[4],
                self.dire_hero[0],
                self.dire_hero[1],
                self.dire_hero[2],
                self.dire_hero[3],
                self.dire_hero[4],
                self.radiant_gold,
                self.dire_gold,
                )


import sql

s = sql.dota2_sql()
m = Match.get_match_by_id("3690951045")
s.insert_many([m.sql_data], 1)
