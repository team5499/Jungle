import time
import threading
import os
import json


class ConfigurationHandler():

    # minimum time between file flushes. If set too low, this can put a lot of unneccesary load on the system
    MIN_FLUSH_PERIOD_S = 0.25

    def __init__(self, file_path='./conf.json', debug=False):
        try:
            self.data_file = open(file_path, 'r+')
        except FileNotFoundError:
            print("the specified file wasn't found")
            exit(1)
        try:
            self.raw_json_obj = json.load(self.data_file)
        except ValueError:
            print('json formatting issue')
            exit(1)
        self.debug = debug
        self._flush_lock = threading.RLock()
        self._last_flush_time = 0
        self._check_json(self.raw_json_obj)

    def _check_json(self, raw_json_obj):
        problems = []
        for k, v in raw_json_obj.items():
            if not issubclass(v.__class__, dict):
                problems.append(k)
                continue
        if len(problems) > 0:
            print('FATAL: there were problem(s) with these variable(s):')
            print(problems)
            exit(1)

    def get_raw_json_obj(self):
        if self.debug:
            self.data_file.seek(0)
            self.raw_json_obj = json.load(self.data_file)
        return self.raw_json_obj

    def get_compact_json_string(self):
        return json.dumps(self.get_raw_json_obj())

    def get_formatted_json_string(self):
        return json.dumps(self.get_raw_json_obj(), indent=4, sort_keys=True)

    def get_page_ids(self):
        return self.get_raw_json_obj()['pages'].keys()

    def get_nav_bar(self):
        nav_bar = []
        for k, v in self.get_raw_json_obj()['pages'].items():
            nav_bar.append((f'/{k}', k, v['title']))
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
        ], name=f'write_thread{time.perf_counter()}', daemon=True)
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
