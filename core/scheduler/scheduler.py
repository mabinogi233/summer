import apscheduler
import time
import threading
import summer.core.configloader.chain_config_loader as chain_config_loader
import summer.web.web_config_loader as web_config_loader


from summer.core.configloader.container import content
from summer.web.webcontainer import web_content

import summer.config as config

debug = True


def parse_xml(_xml_path,config_loader):
    chain_list = config_loader.load(_xml_path)
    content.clear()
    for chain in chain_list:
        content.push(chain)
    if debug:
        print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))," load xml")


def parse_web_xml(_xml_path,config_loader):
    web_list = config_loader.load(_xml_path)
    web_content.clear()
    for web in web_list:
        web_content.push(web)
    if debug:
        print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), " load web xml")


class DefaultConfigScheduler():

    def __init__(self,
                 config_loader,
                 xml_path='',
                 cron_m='*/2',
                 first_run=True,
                 func=parse_xml,
                 web=False):
        self.config_loader = config_loader
        self.xml_path = xml_path
        self.cron = cron_m
        self.chain_list = self.config_loader.load(xml_path)
        self.func = func

        if web:
            self.func = parse_web_xml

        if first_run:
            self.run_first()

    def get_scheduler(self):
        # run every 2 minutes
        # cron = '0 0/2 * * * ? '
        from apscheduler.schedulers.blocking import BlockingScheduler
        scheduler = apscheduler.schedulers.blocking.BlockingScheduler()
        _config_loader = self.config_loader
        _xml_path = self.xml_path

        scheduler.add_job(self.func, 'cron',minute=self.cron,args=(self.xml_path,self.config_loader))

        return scheduler

    def run_scheduler(self):
        self.scheduler = self.get_scheduler()
        self.scheduler.start()

    def subprocess_run_scheduler(self):
        # multi-subprocess
        self.p = threading.Thread(target=self.run_scheduler)
        self.p.start()

    def stop_scheduler(self):
        self.scheduler.shutdown()

    def run_first(self):
        self.func(self.xml_path,self.config_loader)


def start():
    d_core = DefaultConfigScheduler(
        chain_config_loader.ChainConfigLoader(),
        cron_m='*/2',
        xml_path=config.config_xml_path,
    )
    d_web = DefaultConfigScheduler(
        web_config_loader.WebConfigLoader(),
        cron_m='*/3',
        xml_path=config.web_xml_path,
        web=True
    )
    d_core.subprocess_run_scheduler()
    d_web.subprocess_run_scheduler()

