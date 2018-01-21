import mysql.connector
import config

class dota2_sql():
    def __init__(self):
        user = config.getConfig("database", "dbuser")
        password = config.getConfig("database", "dbpassword")
        database = config.getConfig("database", "dbname")
        host = config.getConfig("database", "dbhost")
        self.conn = mysql.connector.connect(host=host,user=user, password=password, database=database, use_unicode=True)
        self.cursor = self.conn.cursor()

    def get_all_match_id(self, skill):
        skill_lst = ["", "normal_match", "high_match", "veryhigh_match"]
        table_name = skill_lst[skill]
        self.cursor.execute('select match_id from %s' % table_name)
        values = self.cursor.fetchall()
        id_set=set()
        for i, in values:
            id_set.add(i)
        return id_set

    def insert_many(self, lst, skill):
        skill_lst = ["", "normal_match", "high_match", "veryhigh_match"]
        table_name = skill_lst[skill]
        cmd = "INSERT INTO "+table_name+" (match_id, match_seq_num, start_time, duration, radiant_win, lobby_type," \
                                        " game_mode, radiant_hero0, radiant_hero1, radiant_hero2, radiant_hero3, " \
                                        "radiant_hero4, dire_hero0, dire_hero1, dire_hero2, dire_hero3, dire_hero4," \
                                        " radiant_gold, dire_gold) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, " \
                                        "%s, %s, %s, %s, %s, %s, %s, %s, %s )"
        self.cursor.executemany(cmd, lst)
        self.conn.commit()

