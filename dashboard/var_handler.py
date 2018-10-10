import time
import threading
import os
from copy import deepcopy
import json


class VariableHandler():

    # minimum time between file flushes. If set too low, this can put a lot of unneccesary load on the system
    MIN_FLUSH_PERIOD_S = 0.25

    def __init__(self, file_path='./vars.json'):
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
        # this object is what gets written to the actual file
        self.orig_json_obj = deepcopy(self.raw_json_obj)
        self._orig_json_lock = threading.RLock()
        self._flush_lock = threading.RLock()
        self._last_flush_time = 0
        self._check_json(self.raw_json_obj)

    def _check_json(self, raw_json_obj):
        problems = []
        for k, v in raw_json_obj.items():
            if 'value' not in v:  # variable must contain "value" property
                problems.append(k)
                continue
            if 'writable' not in v:  # variable must contain "writable" property
                problems.append(k)
                continue
            # "writable" property must be a boolean
            if not issubclass(bool, v['writable'].__class__):
                problems.append(k)
                continue
            if not v['value']:  # "value" property must not be null, or None
                problems.append(k)
                continue
        if len(problems) > 0:
            print('FATAL: there were problem(s) with these variable(s):')
            print(problems)
            exit(1)

    def get_compact_json_string(self):
        return json.dumps(self.raw_json_obj)

    def get_formatted_json_string(self):
        return json.dumps(self.raw_json_obj, indent=4, sort_keys=True)

    def get_vars_list(self):
        return self.raw_json_obj.keys()

    def get_vars_list_alpha(self):
        return sorted(self.get_vars_list(), key=str.lower)

    def contains_var(self, key):
        return key in self.raw_json_obj

    def get_json_var(self, key):
        assert self.contains_key(
            key), f'FATAL: the variable {key} does not exist'
        return self.raw_json_obj[key]['value']

    def set_json_var(self, key, value):
        assert self.contains_key(
            key), f'FATAL: the variable {key} does not exist'
        self.raw_json_obj[key]['value'] = value
        with self._orig_json_lock:
            if self.orig_json_obj[key]['writable']:
                self.orig_json_obj[key]['value'] = value
        if self.raw_json_obj[key]['writable']:
            self.write_file()

    # starts a thread for writing and flushing, since this operation does take time
    def write_file(self):
        thread = threading.Thread(target=self._write_file, args=[
        ], name=f'write_thread{time.perf_counter()}', daemon=True)
        thread.start()

    def _write_file(self):
        while time.perf_counter() - self._last_flush_time < VariableHandler.MIN_FLUSH_PERIOD_S:
            pass  # wait until minimum period has elapsed
        with self._flush_lock:
            self.data_file.seek(0)
            with self._orig_json_lock:
                json.dump(self.orig_json_obj, self.data_file,
                          indent=4, sort_keys=True)  # pretty dump
            self.data_file.truncate()
            self.data_file.flush()  # takes time
            os.fsync(self.data_file.fileno())  # takes time
        self.last_flush_time = time.perf_counter()
