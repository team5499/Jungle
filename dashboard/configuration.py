import time
import threading
import os
import json

from page import Page

def panic(message, err=1):
    print(message)
    exit(err)

class Configuration():
    '''This class represents a configuration for the dashboard'''
    def __init__(self, file):
        try:
            self.json_file = open(file, 'r+')
        except FileNotFoundError:
            panic('the specified JSON config file wasn\'t found')
            exit(1)
        try:
            self.raw_json_obj = json.load(self.json_file)
        except ValueError:
            panic('config json formatting issue')
            exit(1)
        self._check_json(self.raw_json_obj) # if this passes, then we can move onto loading the page configurations

        # load our widgets
        self.widgets = []
        for p in self.raw_json_obj['']

        # load our pages
        self.pages = []
        for p in self.raw_json_obj['pages']:
            self.pages.append(Page(p))

    def get_page_names(self):
        return self.get_raw_json_obj()['pages'].keys()

    def get_nav_bar(self):
        nav_bar = []
        for k, v in self.get_raw_json_obj()['pages'].items():
            nav_bar.append(('/{}'.format(k), k, v['title']))
        return nav_bar

    def get_page_title(self, page):
        return self.get_raw_json_obj()['pages'][page]['title']

    def get_page_widgets(self, page):
        return self.get_raw_json_obj()['pages'][page]['widgets']

    def contains_page(self, key):
        return key in self.get_raw_json_obj()['pages']

    def edit_widget_attr(self, page, id, key, value):
        path = key.split('.')
        widgets = self.raw_json_obj['pages'][page]['widgets']
        widget = None
        for w in widgets:
            if w['id'] == id:
                widget = w
                break
        current_item = widget[path[0]]
        for k in path[1:-1]:
            current_item = current_item[k]
        current_item[path[-1]] = value
        self.write_file()

    # starts a thread for writing and flushing, since this operation does take time
    def write_file(self):
        thread = threading.Thread(target=self._write_file, args=[
        ], name='write_thread{}'.format(time.perf_counter()), daemon=True)
        thread.start()

    def _write_file(self):
        while time.perf_counter() - self._last_flush_time < ConfigurationHandler.MIN_FLUSH_PERIOD_S:
            pass  # wait until minimum period has elapsed
        with self._flush_lock:
            self.data_file.seek(0)
            json.dump(self.raw_json_obj, self.data_file,
                      indent=4, sort_keys=True)  # pretty dump
            self.data_file.truncate()
            self.data_file.flush()  # takes time
            os.fsync(self.data_file.fileno())  # takes time
        self.last_flush_time = time.perf_counter()


    # Utils
    def _check_json(self, raw_json_obj):
        '''This function checks the configuration json for `pages` and `widget_templates`'''
        assert 'pages' in raw_json_obj, 'FATAL: the config file must have \'pages\''
        assert 'widget_templates' in raw_json_obj, 'FATAL: the config file must have \'widget_templates\''
        problems = []
        for k, v in raw_json_obj.items():
            if not issubclass(v.__class__, list):
                problems.append(k)
                continue
            for d in v:
                if not issubclass(d.__class__, dict):
                    problems.append(k)
                    continue
        if len(problems) > 0:
            print('FATAL: there were problem(s) with these variable(s):')
            print(problems)
            exit(1)
