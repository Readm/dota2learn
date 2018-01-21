import time, os
import config, crawler

n_crawler = crawler.Crawler(1)
h_crawer = crawler.Crawler(1)
vh_crawler = crawler.Crawler(1)
crawlers = [n_crawler, h_crawer, vh_crawler]
interval = [config.getConfig("crawler", "n"), config.getConfig("crawler", "h"), config.getConfig("crawler", "vh")]

last_run_time = [time.time() for i in range(3)]
while True:
    time_now = time.time()
    for i in range(3):
        print time_now - last_run_time[i], interval[i]
        if time_now - last_run_time[i] > int(interval[i]) * 60:
            if os.fork()==0:
                crawler[i].run()
                exit()
            last_run_time[i] = time_now
    time.sleep(30)
