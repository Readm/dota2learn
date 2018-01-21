import time, os
import config, crawler

n_crawler = crawler.Crawler(1)
h_crawer = crawler.Crawler(2)
vh_crawler = crawler.Crawler(3)
crawlers = [n_crawler, h_crawer, vh_crawler]
interval = [config.getConfig("crawler", "n"), config.getConfig("crawler", "h"), config.getConfig("crawler", "vh")]

last_run_time = [time.time()-int(interval[i]) for i in range(3)]
while True:
    time_now = time.time()
    for i in range(3):
        if time_now - last_run_time[i] > int(interval[i]) :
            if os.fork()==0:
                crawlers[i].run()
                exit()
            last_run_time[i] = time_now
    time.sleep(10)
    interval = [config.getConfig("crawler", "n"), config.getConfig("crawler", "h"), config.getConfig("crawler", "vh")]
