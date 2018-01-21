import json, time
from dota2py import api
import sql
from match import Match

dota2_db = sql.dota2_sql()


class Crawler():
    def __init__(self, skill):
        self.skill = skill
        self.old_ids = dota2_db.get_all_match_id(self.skill)
        self.buffer = []
        with open("status.json") as f:
            self.json_data = json.load(f)
            self.succeed_in_last_run = self.json_data[str(skill)]
        self.total_download = 0
        self.total_valid = 0

    def download(self, from_=None):
        if not from_:
            result = api.get_match_history(skill=self.skill)["result"]
            matches = result["matches"] if len(result) > 1 else []
        else:
            result = api.get_match_history(skill=self.skill, start_at_match_id=from_)["result"]
            matches = result["matches"][1:] if len(result) > 2 else []
        if not matches: return

        oldest_id = min([i["match_id"] for i in matches])
        for match in matches:
            if int(match["match_id"]) in self.old_ids and self.succeed_in_last_run: return  # end if have the same
            m = Match.get_match_by_id(match["match_id"])
            print '.',
            self.total_download += 1
            if m.is_valid():
                print '|',
                self.total_valid += 1
                self.buffer.append(m.sql_data)
                self.old_ids.add(int(match["match_id"]))
        if int(result["results_remaining"]) > 0:
            self.download(from_=oldest_id)

    def commit(self):
        dota2_db.insert_many(self.buffer, self.skill)
        self.buffer = []

    def run(self):
        try:
            self.download()
            self.download_succeed = True
        except:
            self.download_succeed = False
        finally:
            self.commit()
            with open("status.json", "w") as f:
                self.json_data[str(self.skill)] = self.download_succeed
                json.dump(self.json_data, f, indent=4)

            with open("log.txt", "a+") as f:
                localtime = time.asctime(time.localtime(time.time()))
                f.write("Date: %s, Skill:%d, Total Download: %d, Total Valid: %d Succeed %s\n" % (
                    localtime, self.skill, self.total_download, self.total_valid, str(self.download_succeed)))
            self.total_valid = 0
            self.total_download = 0

