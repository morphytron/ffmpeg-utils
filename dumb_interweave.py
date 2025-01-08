import sys, os, subprocess as sp
from sorting import custom_sort
from media_io import media_io

class mv_interweave:
    output_folder = ''
    use_copy = False
    def __init__(self,):
        med_io = media_io()
        #arg reading...
        med_io.get_args_for_read_folder()
        self.get_args_for_interweave()
        #sorting
        med_io.sort_lists()
        #geting variables for local from media_io.
        self.all_media_files = med_io.all_media_files
        self.all_key_abs_paths = med_io.all_key_abs_paths
        self.file_ext = med_io.file_ext
        self.file_ext_len = med_io.file_ext_len

        #print("DATA FROM MED_IO\n{} {} {} {}".format(med_io.all_media_files, med_io.all_key_abs_paths, med_io.file_ext, med_io.file_ext_len))
        #interweaving
        self.interweave_dict()
        self.exec_mv()
    def get_args_for_interweave(self):
        args = sys.argv
        args_iter = iter(args)
        while True:
            try:
                nx = next(args_iter)
                if nx == '-o' or nx == '--output-folder':
                    try:
                        self.output_folder = next(args_iter)
                    except:
                        print("Possibly no argument following -o, --output-folder")
                        exit(1)
                if nx == '-c' or nx == '--use-copy':
                    self.use_copy = True
            except:
                print("Done with args...")
                break


    def interweave_dict(self):
        index = 0
        with open('move_cmd.sh', 'w') as f:
            list_of_sorted_arrays = self.all_media_files.values()
            list_of_iters = []
            for l in list_of_sorted_arrays:
               list_of_iters.append(iter(l))
            print("list of iters: {}".format(list_of_iters))
            iters_that_are_exhausted = 0
            while iters_that_are_exhausted < len(list_of_iters):
                iters_that_are_exhausted = 0
                for l in list_of_iters: # round robin
                    try:
                        next_item = next(l)
                        index_to_6_dec = '{:06d}'.format(index)
                        writ = '{} "{}" "{}/1_{}.{}"\n'.format('cp' if self.use_copy else 'mv', next_item, self.output_folder,
                                                            index_to_6_dec, self.file_ext)
                        print("Writing: {}".format(writ))
                        f.write(writ)
                        index += 1
                    except(StopIteration):
                        #print("List is exhausted")
                        iters_that_are_exhausted += 1
            print("Completed writing script")
            f.flush()
            f.close()
    def exec_mv(self):
        #,
        print("Calling cat movecmd")
        sp.run(" ".join(["cat", "move_cmd.sh;","source", "./move_cmd.sh"]), shell=True,
               text=True, executable='/bin/zsh', check=True)
