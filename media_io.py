import os, sys, re
from sorting import custom_sort

class media_io:
    all_key_abs_paths = {}
    all_media_files = {}
    reversed = None
    sort_func = 'num_smart'
    ignore_regex = None
    skip_interactive = False
    file_ext = None
    file_ext_len = 0
    def __init__(self, skip_interactive=False):
        if skip_interactive:
            self.skip_interactive = True
        print("Init media_io")
    def sort_lists(self):
        keys = self.all_media_files.keys()
        for key in keys:
            arr = self.all_media_files[key]
            if isinstance(self.sort_func, type(lambda x:x)):
                arr = sorted(arr, key=self.sort_func, reverse=self.reversed)
            elif self.sort_func == 'num_smart':
                print("Num smart sorting activated.")
                arr = custom_sort(arr).sort_prioritizing_proper_number_order(is_ascending=not self.reversed)
            print("Sorted array looks like {}".format(arr))
            self.all_media_files[key] = arr

    def get_args_for_read_folder(self):
        args = sys.argv
        print(args)
        args_iter = iter(args)
        while True:
            try:
                nx = next(args_iter)
                if nx == '-e' or nx == '--file-ext':
                    try:
                        self.file_ext = next(args_iter)
                        self.file_ext_len = len(self.file_ext)
                    except:
                        print("Possibly no argument following -e, --file-ext")
                        exit(1)
                if nx == '-i' or nx == '--input-folder':
                    try:
                        folder = next(args_iter)
                        os.chdir(path=folder)
                    except:
                        print("Possibly no argument following -i, --input-folder")
                        exit(1)
                elif nx == '-s' or nx == '--sort-alg':
                    try:
                        func_name = next(args_iter)
                        if func_name == 'len':
                            self.sort_func = len
                        elif func_name == 'created':
                            self.sort_func = 'created'
                        elif func_name == 'num_smart':
                            self.sort_func = 'num_smart'
                    except:
                        print("Possibly no argument following -s, --sort-alg.  Possible args are len.")
                        exit(1)
                elif nx == '-r' or nx == '--ignore-regex':
                    print("-r flag found!")
                    self.ignore_regex = re.compile(next(args_iter))
                elif nx == '-d' or nx == '--descend-order':
                    self.reversed = True
            except:
                print("No more args")
                if self.file_ext is None:
                    print("Expected argument for file extension. (-e) or --file-ext = <aka. mp3>")
                    exit(1)
                print("File extension is {}, file ext. length is {}.".format(self.file_ext, self.file_ext_len))
                self.recurse_dir_struct()
                break
    def recurse_dir_struct(self, other_dir_path=None, key_name=None):
        #print("Called recurse directory structure.")
        cwd = os.getcwd()
        if other_dir_path is not None:
            print("Other_dir_path is not None! It is {}".format(other_dir_path))
            cwd = other_dir_path
        contents = os.listdir(cwd)
        temp = []
        for fn in contents:
            temp.append(os.path.join(os.path.abspath(fn)))
        contents = temp
        print("Contents of {} are {}".format(cwd, contents))
        abs_file_name = str(cwd)
        fname_only = str(os.path.split(cwd)[-1]).replace(" ", "_")
        use_cwd = 'n' if self.skip_interactive else None
        if not self.skip_interactive:
            use_cwd = input("Use {}.{} as name of {} (Y,n):".format(str(fname_only),self.file_ext, self.file_ext))
        if use_cwd.lower() != 'y' and use_cwd.lower() != 'n':
            print("Expected y or n. Defaulting to yes.")
            use_cwd = 'y'
        if use_cwd.lower() == 'n':
            key_list = list(self.all_media_files.keys())
            abs_file_name = input(
                "What is the name you wish to use? You can use an existing entry (select it via index-# or name). Current entries are {}:".format(
                    str(key_list))) if not self.skip_interactive else key_name
            try:
                key_index = int(abs_file_name)
                abs_file_name = key_list[key_index]
            except(ValueError):
                print("User did not enter a number")
            except(IndexError):
                print("User entered an out of bounds value")
                exit(1)
            finally:
                #print("Gets here")
                if not abs_file_name in self.all_media_files:
                    self.all_media_files[abs_file_name] = []
        else:
            if not fname_only in self.all_media_files:
                self.all_media_files[fname_only] = []
        print(contents)
        for c in contents:
            #print("Found {}.".format(c))
            if os.path.isdir(c):
                #print("Calling recurse_dir_struct because {} is a directory".format(c))
                cwd_old = cwd
                os.chdir(c)
                self.recurse_dir_struct(other_dir_path=c)
                os.chdir(cwd_old)
            elif os.path.isfile(c) and c[-(self.file_ext_len + 1):] == '.{}'.format(self.file_ext):
                if self.ignore_regex is not None:
                    print("Ignore regex is not none. Excluding last {}, path is {}. Str ignore_regex is {}".format(c[:-(self.file_ext_len + 1)],
                                                                                                                  (self.file_ext_len + 1), self.ignore_regex.pattern))
                    if self.ignore_regex.match(c, 0, -(self.file_ext_len + 1)) is not None:
                        print("Skipping {} because regex is {}".format(c, self.ignore_regex.pattern))
                        continue
                    if c[:-(1 + self.file_ext_len)].find(self.ignore_regex.pattern) != -1:
                        print("Skipping {} because string contains {}".format(c, self.ignore_regex.pattern))
                        continue
                else:
                    print("No ignore-regex flag present.")
                print("Adding file {}: {}".format(self.file_ext, c))
                dir = self.all_media_files[abs_file_name]
                if abs_file_name in self.all_media_files:
                    abs_path = os.path.abspath(c)
                    dir.append(abs_path)
                else:
                    dir = []
                    abs_path = os.path.abspath(c)
                    dir.append(abs_path)
                    self.all_media_files[abs_file_name] = dir
            #else:
            #    print("{} is not a directory, nor is it a(n) {} file".format(c, self.file_ext))