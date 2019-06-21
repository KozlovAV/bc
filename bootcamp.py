# -- coding: utf-8 --
import sys, os
from pprint import pprint
from shutil import copyfile

import cmd
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

PROMPT = '> '


class Watcher(FileSystemEventHandler):
    DIRECTORY_TO_WATCH = 'C:/Users/avk/AppData/Local/Temp/'
    FILE_PATTERN = 'vdh-'
    DST_PATH = 'D:/00.Inbox'

    def __init__(self):
        self.observer = Observer()
        self.trg_files = {}
        self.temp_files = {}
        self.filename = ''
        self.global_log = open('d:/global.log', 'a')

    def run(self):

        if not self.observer.is_alive():
            self.observer = Observer()
            self.trg_files = {}
            self.observer.schedule(self, self.DIRECTORY_TO_WATCH, recursive=False)
            self.observer.start()
            self.trg_files = {}
            self.temp_files = {}
            print(f'Start watching directory {self.DIRECTORY_TO_WATCH}')
        else:
            print('Already watching')

    def stop(self):
        self.observer.stop()
        if self.observer.is_alive():
            self.observer.join()
        print(f'Stop watching directory {self.DIRECTORY_TO_WATCH}')
        self.global_log.close()

    def print_status(self):
        print(f'Watcher alive status is {self.observer.is_alive()}')
        print('Files are: ')
        pprint(self.trg_files)

    def _should_trace(self, name):
        res = self.FILE_PATTERN in name \
              and self.FILE_PATTERN + 'wm-' not in name \
              and '.tmp.part' in name
        return res


    def on_any_event(self, event):
        if self._should_trace (event.src_path):
            print('Received event is ', event.event_type, event.src_path)
            print(PROMPT)


    def on_created(self, event):
        if self.filename:
            # start trace files
            if self._should_trace (event.src_path):
                self.trg_files[self.filename].append(event.src_path)
                self.temp_files[event.src_path] = self.filename
                print(f'For trg file {self.filename} temps files are ', self.trg_files[self.filename])
                self.global_log.write(f'\nFor trg file {self.filename} temps files are ' + str(self.trg_files[self.filename]))
                self.global_log.flush()
                print(PROMPT)


    def on_moved(self, event):
        tmp_src_file = event.src_path
        tmp_dest_file = event.dest_path

        trg_name = self.temp_files[tmp_src_file]
        all_tmp_files = self.trg_files[trg_name]

        new_tmp_list = [x.replace(tmp_src_file, tmp_dest_file) for x in all_tmp_files]
        self.trg_files[trg_name] = new_tmp_list

        has_parts = [x for x in new_tmp_list if '.tmp.part' in x]
        if len(has_parts) == 0:
            print(f'All temp files for {trg_name} are complited')
            self.global_log.write(f'\nAll temp files for {trg_name} are complited')
            self.global_log.flush()

            ll = []
            trg_dir = self.DST_PATH + '/' + trg_name + '/'
            for file in new_tmp_list:
                base = os.path.basename(file)
                dst = trg_dir + base
                ll.append(dst)

                os.makedirs(os.path.dirname(dst), exist_ok=True)
                copyfile(file, dst)
                print(f' file copied in {dst}')

            self.trg_files[trg_name] = []
            self.temp_files = {k: v for k, v in self.temp_files.items() if v!=trg_name}

            cmd = 'ffmpeg -loglevel panic -i ' + ' -i '.join(ll) + ' -c:a copy -c:v copy ' + trg_dir + trg_name + '.mp4 > ' + trg_dir + trg_name + '.log '
            self.global_log.write(f'\n cmd is '+cmd)
            self.global_log.flush()
            os.system(cmd)


    def pre_download_start(self, name):
        print('Start collecting file names for ', name)
        self.filename = name
        self.trg_files[name] = []

    def post_download_start(self):
        if self.filename:
            print(f'For trg file {self.filename} temps files are ', self.trg_files[self.filename])
            print(PROMPT)
            self.filename = ''


# class Handler(FileSystemEventHandler):
#
#     # @staticmethod


class Shell(cmd.Cmd):

    def __init__(self):
        cmd.Cmd.__init__(self)
        self.prompt = PROMPT
        self.intro = "Добро пожаловать\nДля справки наберите 'help'"
        self.doc_header = "Доступные команды (для справки по конкретной команде наберите 'help _команда_')"
        self.watcher = Watcher()

    def do_start_watcher(self, line):
        self.watcher.run()

    def do_stop_watcher(self, line):
        self.watcher.stop()

    def do_watcher_status(self, line):
        self.watcher.print_status()

    def do_predownload(self, line):
        self.watcher.pre_download_start(line)

    def do_download_started(self, line):
        self.watcher.post_download_start()

    def do_exit(self, line):
        return True

    def default(self, line):
        print(f"Несуществующая команда {line}")

    def postloop(self):
        self.watcher.stop()
        print('Выхожу...')

    def emptyline(self):
        pass

    def do_EOF(self, line):
        return True

    def cmdloop(self, intro=None):
        print(self.intro)
        while True:
            try:
                super(Shell, self).cmdloop(intro="")
                break  # Нафиг не надо???
            except KeyboardInterrupt:
                print('interr |')
                self.postloop()
                return True

        # print(self.intro)
        #
        # doQuit = False
        # while doQuit != True:
        #     try:
        #         self.cmdloop(intro='')
        #         doQuit = True
        #     except KeyboardInterrupt:
        #         sys.stdout.write('\n')
        #         sys.stdout.write('Presses Ctrl C')


if __name__ == "__main__":
    shell = Shell()
    try:
        shell.cmdloop()
    except KeyboardInterrupt:
        print("завершение сеанса...")
