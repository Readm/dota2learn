import json, time
from dota2py import api
import sql
from match import Match
from config import setConfig, getConfig

dota2_db = sql.dota2_sql()


class Crawler():
    def __init__(self, skill):
        self.skill = skill
        self.old_ids = dota2_db.get_all_match_id(self.skill)
        self.buffer = []
        self.total_download = 0
        self.total_valid = 0
        self.download_succeed = True
        self.reach_last = False
        self.skip_num = 0
        self.same_id = 0

    def get_history(self, from_=None):
        for _ in range(5):
            try:
                if from_:
                    return api.get_match_history(skill=self.skill)["result"]
                else:
                    return api.get_match_history(skill=self.skill,start_at_match_id=from_)["result"]
            except:
                pass
        self.download_succeed = False
        return None

    def download(self, from_=None):
        if not from_:
            result = self.get_history()
            if not result: return
            matches = result["matches"] if len(result) > 1 else []
        else:
            result = self.get_history(from_)
            if not result: return
            matches = result["matches"][1:] if len(result) > 2 else []
        if not matches: return

        oldest_id = min([i["match_id"] for i in matches])
        for match in matches:
            if int(match["match_id"]) in self.old_ids:  # end if have the same
                self.same_id +=1
                self.reach_last = True
                continue
            try:
                m = Match.get_match_by_id(match["match_id"])
            except:
                self.skip_num += 1
                continue
            print '.',
            self.total_download += 1
            if m.is_valid():
                print '|',
                self.total_valid += 1
                self.buffer.append(m.sql_data)
                self.old_ids.add(int(match["match_id"]))
        self.commit()
        if int(result["results_remaining"]) > 0:
            self.download(from_=oldest_id)

    def commit(self):
        self.old_ids = dota2_db.get_all_match_id(self.skill)
        for i in self.buffer:
            if i[0] in self.old_ids: del i
        dota2_db.insert_many(self.buffer, self.skill)
        self.buffer = []

    def run(self):
        try:
            self.old_ids = dota2_db.get_all_match_id(self.skill)
            self.download()
            self.download_succeed = True
        except Exception, e:
            self.download_succeed = False
            self.cause = str(e)
        finally:
            self.commit()

            with open("log.txt", "a+") as f:
                localtime = time.asctime(time.localtime(time.time()))
                f.write(
                    "Date: %s, Skill:%d, Total Download: %d, Total Valid: %d \t Reach Last: %s, "
                    "Skip Num: %d \tSucceed: %s\n" % (
                        localtime, self.skill, self.total_download, self.total_valid,
                        str(self.reach_last), self.skip_num, str(self.download_succeed) + "" if self.download_succeed else self.cause))
            self.total_valid = 0
            self.total_download = 0
            self.reach_last = False
            self.skip_num = 0

            # update config automatically
            key = ["",'n','h','vh'][self.skill]
            current = int(getConfig("crawler", key))
            if not self.reach_last and current > 60:
                setConfig("crawler", key, int(current/1.2))
            if self.same_id>10:
                setConfig("crawler", key, int(current*1.05))
            self.same_id = 0

