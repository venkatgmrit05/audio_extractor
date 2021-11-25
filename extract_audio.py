# -*- coding: utf-8 -*-
"""
Created on Wed Nov 24 12:51:18 2021

@author: umave
"""
import os
import argparse
import moviepy.editor as mpe
import shutil


class ExtractAudio(object):

    def __init__(self,
                 name='aex_1',
                 counter_limit=10):
        self.name = name
        self.counter_limit = counter_limit
        # self.source = source_folder
        # self.target = target_folder

    @staticmethod
    def get_audio(_video_clip,
                  _audio_file_name,
                  extn='.mp3'):
        print(f'audio file name is {_audio_file_name}')
        try:
            _vid_clip = mpe.VideoFileClip(_video_clip)
            _vid_clip.audio.write_audiofile(_audio_file_name)
            return 1
        except Exception as e:
            # print(1)
            print('error >> {}'.format(e))
            return 0

    def rip_audio(self,
                  vid_file,
                  audio_filename,
                  counter=0):

        if not os.path.isfile(audio_filename):  # checking for pre existing file
            ret_code = self.get_audio(vid_file,audio_filename)
            return ret_code
        else:
            fname,extn = os.path.basename(audio_filename).split('.')
            new_name = os.path.basename(audio_filename) + str(counter) + f'.{extn}'
            new_file_path = os.path.join(os.path.dirname(audio_filename),new_name)
            return self.rip_audio(vid_file,
                                  new_file_path)


# depl #test


#
# agp = argparse.ArgumentParser()
# agp.add_argument('-s','--source',help = 'source_dir')
# agp.add_argument('-t','--target',help = 'target_dir')
# agp.add_argument('-e','--extension',help = 'file extension : mp4 or 'mp4,aac' etc')
# args = agp.parse_args()

# audioex = ExtractAudio()
# files =os.listdir(args.source)
# print(files)
# failed = []
# for file in files:
#     filename = get_sanitized_filename(file)
# success = audioex.get_audio(vid_file,audio_file)
# if not success:
#     failed.append(file)

# dev


from funcs import *

source = r'D:\4K_Video_Downloader\IDM_videos\idm_music_videos\failed_to_extract'

# source = r'D:\4K_Video_Downloader\IDM_videos\idm_music_videos\t2'
dest = r'D:\4K_Video_Downloader\IDM_videos\idm_music_extracted_audio'

if dest:
    dest = dest
else:
    dest = os.path.join(source,'extracted_audio_files')
    os.mkdir(dest)
vid_files = os.listdir(source)
vid_files = [file for file in vid_files if os.path.isfile(os.path.join(source,file))]

file_type = '.mkv'

failed_files = []
fail_folder = os.path.join(source,'failed_to_extract')
audioex = ExtractAudio()


def get_unique_file_name(file_path,
                         counter=0,
                         counter_limit=10):
    if not '.m' in file_path:
        file_path = file_path + '.mp3'
    print(f'verifying {file_path}')

    if os.path.isfile(file_path):
        if counter < counter_limit:
            counter = counter + 1
            fname,extn = os.path.basename(file_path).split('.')

            new_name = f'{fname}_{counter}_.{extn}'
            new_file_path = os.path.join(os.path.dirname(file_path),new_name)
            print(f'updating name to  {new_file_path}')
        return get_unique_file_name(new_file_path,
                                    counter)
    return file_path


num_total_files = len(vid_files)
num_files_failed = 0
num_files_extracted = 0
try:
    for vid_file in vid_files:
        file_ext = file_type
        success = 0
        try:
            # TODO maybe do not need get a success status to check
            # if doing a try except. directly append in except block
            print(f'processing {vid_file}')
            audio_filename = get_sanitized_filename(vid_file,
                                                    file_ext)
            audio_filename = audio_filename + '.mp3'
            print(f'audio_filename is {audio_filename}')

            vid_file = os.path.join(source,vid_file)
            audio_filename = os.path.join(dest,audio_filename)
            audio_filename = get_unique_file_name(audio_filename)

            success = audioex.get_audio(vid_file,
                                        audio_filename)
            num_files_extracted += 1
            if not success:
                failed_files.append(vid_file)
                num_files_failed += 1
        except Exception as e1:
            print(f'error >> {e1}')
            failed_files.append(vid_file)
            num_files_failed += 1
            # print(2)
except Exception as e:
    print(f'error >> {e}')
    # print(3)
finally:
    print(f'deleting audio extractor object {audioex.name}')
    del audioex
#

print('failed >> ',failed_files)

move_failed_files = False
if move_failed_files:
    #
    if failed_files:
        print(f'creating fail folder at {fail_folder}')

        try:
            os.mkdir(fail_folder)
        except Exception as e:
            print(f'error >> {e}')
            # print(4)

    if failed_files:
        for failed_file in failed_files:
            try:
                shutil.move(os.path.join(source,
                                         failed_file),
                            fail_folder)
            except Exception as e:
                print(f'error >> {e}')
                # print(5)

print(f'num given files : {num_total_files} , '
      f'num success files : {num_files_extracted} ,'
      f'num failed files : {num_files_failed} ')
