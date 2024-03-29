# This file is modified from https://www.reddit.com/r/learnpython/comments/83rvgv/comment/dvl0gdp/
import os
import sys
import logging
import subprocess
import time
import database
import actions
import datetime
import conditions
import sys
from threading import Thread
from queue import Queue
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from PyQt5.QtCore import QDir, QFileInfo

file_queue = Queue()
pathnames = database.get_folders_list()

class QueueManager(object):
        '''Manager class for taking files off the file_queue and pushing them into wherever'''
        attn_str = "===[ {} ]==="

        def __init__(self, file_queue: Queue, logger: logging.Logger):
            self.thread = Thread(target=self._process_file_queue)
            self.file_queue = file_queue
            self.logger = logger or logging.getLogger(__name__)

        def process_file_queue(self):
            '''Method checks if there is already a thread running or alive processing the queue and if not, creates a new
            one '''
            if not self.thread or not self.thread.is_alive():
                self.thread = Thread(target=self._process_file_queue)
                self.logger.info(self.attn_str.format("START processing"))
                self.thread.start()

        def _process_file_queue(self):
            '''Main method run as a separate thread which pops files off the file_queue and pushes data into whereever'''
            while not file_queue.empty():
                try:
                    # Get file off Queue
                    file = file_queue.get()
                    self.logger.info("Processing file {}".format(file))
                    file_info = QFileInfo(file)
                    dir = file_info.dir().path()
                    print("DIR: ", dir)
                    list_of_active_rules = database.get_rules_list(dir)
                    for rule in list_of_active_rules:
                        rule_conditions = database.retrieve_values(dir, rule)
                        print("Active rule: {}".format(rule))
                        todo, _ = conditions.get_files(rule_conditions)
                        if file in todo:
                            action = todo[file][0]
                            conditions.run_task(rule_conditions, action, file)

                    #### INSERT CODE HERE TO DO WORK ####

                except Exception as e:

                    # If exception, log and do whatever
                    self.logger.error(str(e))

                    #### ANY CODE YOU WANT HERE IN CASE OF EXCEPTION ####

            self.logger.info(self.attn_str.format("END of file queue"))


class QueueEventHandler(FileSystemEventHandler):
        '''Watches a specific folder and raises events on_created and on_deleted'''

        queue_mgr = QueueManager(file_queue, logging.getLogger())

        def on_created(self, event):
            '''
        Handles on_created event. Checks that created thing is a file (not a folder) and adds it to a file_queue
        :param event:
        :return:
        '''
            super(QueueEventHandler, self).on_created(event)
            if not event.is_directory:
                logging.info("New file: {}".format(event.src_path))
                # Windows allocates full size at the start
                # But doesn't let access to file until creation is completed
                # and throws OSError
                # So add a ugly way to confirm creation by
                # repeatedly trying to rename file
                # https://stackoverflow.com/a/53153102
                if sys.platform == 'win32':
                    path = event.src_path
                    while True:
                        try:
                            new_path = path + "_"
                            os.rename(path, new_path)
                            os.rename(new_path, path)
                            time.sleep(0.05)
                            break
                        except OSError:
                            time.sleep(1)
                # Use polling for other OS
                # Wait till the file is fully created
                # https://stackoverflow.com/a/41105283
                else:
                    historicalSize = -1
                    try: 
                        while (historicalSize != os.path.getsize(event.src_path)):
                            historicalSize = os.path.getsize(event.src_path)
                            time.sleep(1)
                    except OSError:
                        pass
                logging.info("File Creation Finished at {}".format(event.src_path))
                file_queue.put_nowait(event.src_path)
                logging.info("Put {} into file queue".format(event.src_path))
                self.queue_mgr.process_file_queue()

        def on_deleted(self, event):
            '''
        Handles on_deleted event. Just notes to logger when a file is deleted.
        :param event:
        :return:
        '''
            super(QueueEventHandler, self).on_deleted(event)
            if not event.is_directory:
                logging.info("Deleted file: %s", event.src_path)


def main():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    path = sys.argv[1] if len(sys.argv) > 1 else '.'
    event_handler = QueueEventHandler()
    observer = Observer()
    for pathname in set(pathnames):
        observer.schedule(event_handler, pathname, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
    