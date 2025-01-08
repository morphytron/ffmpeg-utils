import os, subprocess as sp
from media_io import media_io
class create_mp3_from_folder_and_subdirectories:
    def __init__(self):
        med_io = media_io()
        med_io.get_args_for_read_folder()
        med_io.sort_lists()
        self.gen_video_list(all_media_files=med_io.all_media_files, all_key_abs_paths=med_io.all_key_abs_paths,file_ext=med_io.file_ext, file_ext_len=med_io.file_ext_len)
        self.execute_transcode(all_media_files=med_io.all_media_files, all_key_abs_paths=med_io.all_key_abs_paths,file_ext=med_io.file_ext, file_ext_len=med_io.file_ext_len)
    def gen_video_list(self, all_media_files = {}, all_key_abs_paths = {}, file_ext = '', file_ext_len=0):
        for key in all_media_files.keys():
            list_of_vids = str(os.path.join(os.getcwd(),key + '.txt'))
            all_key_abs_paths[key] = list_of_vids
            print("Generating video list for {} @ {}".format(key, list_of_vids))
            with open(list_of_vids, 'w') as f:
                for abs_path_fname in all_media_files[key]:
                    write_line = 'file \'{}.{}\'\n'.format(abs_path_fname[:-file_ext_len], file_ext)
                    print("Writing {}".format(write_line))
                    f.write(write_line) # omit the last 4 chars of the absolute path , which includes mp3 and .
                f.flush()
                f.close()

    def execute_transcode(self, all_media_files={}, all_key_abs_paths={}, file_ext='', file_ext_len=0):
        for key in all_media_files.keys():
            in_args = []
            out_args = []
            index = 0
            cpu_count = os.cpu_count()
            ideal_jobs_count = int(cpu_count / 3) # each encode and decode is three threads (two for decode)
            for abs_path_to_mp4 in all_media_files[key]:
                in_args.append("-i")
                in_args.append("\"{}\"".format(abs_path_to_mp4))
                out_args.append("-map")
                out_args.append(str(index % ideal_jobs_count))
                out_args.append("\"{}\"".format(abs_path_to_mp4[:-file_ext_len] + '.'.format(file_ext)))
                index += 1
            while len(in_args) > 0:
                print("Ideal number of jobs is {} if each task is 3 threads".format(ideal_jobs_count))
                temp_in = in_args[:ideal_jobs_count*2]
                temp_out = out_args[:ideal_jobs_count*3]
                args = ['ffmpeg'] + temp_in + ['-vn', '-ac', '2'] + temp_out
                #print(args)
                print("Starting... running...\n{}".format(" ".join(args)))
                sp.run(" ".join(args), shell=True, check=True, text=True,  executable='/bin/zsh')
                in_args = in_args[ideal_jobs_count*2:]
                out_args = out_args[ideal_jobs_count*3:]
            print("Starting combining to single {}...".format(file_ext))
            args_last = " ".join(['ffmpeg', '-f', 'concat', '-safe', '0', '-i', "\"{}\"".format(self.all_key_abs_paths[key]), "\"{}\"".format(self.all_key_abs_paths[key][:-file_ext_len] + '.{}'.format(file_ext))])
            print(args_last)
            sp.run(args_last,
                           # Probably don't forget these, too
                   check=True,
                   text=True, shell=True, executable='/bin/zsh')



