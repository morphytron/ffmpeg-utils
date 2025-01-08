from convert_mp4_to_mp3 import create_mp3_from_folder_and_subdirectories as cf
from dumb_interweave import mv_interweave
import sys

def run():
    args = sys.argv
    if args[1] == 'ffmpeg-convert':
        cf()
    elif args[1] == 'mv-interweave':
        mv_interweave()
    else:
        print("Expected one of [ffmpeg-convert, mv-interweave] as the first argument.")
        exit(1)

run()

#create_mp3_from_folder_and_subdirectories()
#print("Starting NUM_SMART test.")
#test_arr = ['video_1', 'video_20', 'video_2', 'video_0', 'video_1_1', 'video_3_1', 'video_2_1']
#res = custom_sort(test_arr).sort_prioritizing_proper_number_order(is_ascending=True)
#print("before: {}, after: {}".format(test_arr,res))