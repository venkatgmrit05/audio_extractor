# -*- coding: utf-8 -*-
"""
Created on Wed Nov 24 12:51:18 2021

@author: umave
"""

""

import argparse
import shutil
from ExtractAudio import *
from funcs import *


# depl #test


def extract_audio(args):
    source = args.source
    destination = args.target
    file_type = args.extension
    name_limit = args.name_limit
    if not '.' in args.extension:
        file_type = '.' + args.extension

    move_failed_files = args.move_failed_files

    print(f'source >> {source}')
    print(f'destination >> {destination}')
    print(f'file_type >> {file_type}')
    print(f'move_failed_files >> {move_failed_files}')

    if not destination:
        destination = os.path.join(source,'extracted_audio_files')
        print(f'extracting to folder {destination}')
        try:
            os.mkdir(destination)
        except Exception as e:
            print(f'error >> {e}')

    vid_files = os.listdir(source)
    vid_files = [file for file in vid_files if os.path.isfile(os.path.join(source,file))]

    failed_files = []
    fail_folder = os.path.join(source,'failed_to_extract')
    audioex = ExtractAudio()

    num_total_files = len(vid_files)
    num_files_failed = 0
    num_files_extracted = 0
    try:
        for vid_file in vid_files:
            file_ext = file_type
            success = 0
            try:
                # TODO move file to a success folder / track \
                #  succesful extractions to avoid duplications when run from the \
                #  same folder
                # print(f'processing {vid_file}')
                audio_filename = get_sanitized_filename(vid_file,
                                                        file_ext,
                                                        limit=name_limit)
                audio_filename = audio_filename + '.mp3'
                # print(f'audio_filename is {audio_filename}')

                vid_file = os.path.join(source,vid_file)
                audio_filename = os.path.join(destination,audio_filename)
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
    if failed_files:
        print('failed >> ',failed_files)

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


def main():
    print('enter the command as :')
    print(f'.\extract_audio.py -s "source_folder"  -t "target_folder \
    "-e "extension"  -m "move failed files')
    print('example:')
    print('for help on input parameters type : .\extract_audio.py -help')
    agp = argparse.ArgumentParser()
    agp.add_argument('-s','--source',type=str,help='source_dir')
    agp.add_argument('-t','--target',type=str,default=None,help='target_dir')
    agp.add_argument('-e','--extension',type=str,default='mp4',help='file extension : mp4 etc')
    # TODO extension can be given as a  csv : "mkv,mp4,3gp" etc\
    #  for batch mode operation when multiple video formats
    agp.add_argument('-m','--move_failed_files',type=int,default=0,help='move failed \
         files to another directory, default is 0')
    agp.add_argument('-l','--name_limit',type=int,default=5,help='number of words in track \
     title from original, default is 5')
    args = agp.parse_args()
    try:
        extract_audio(args)
    except Exception as e:
        print(f'error >> {e}')


if __name__ == '__main__':
    main()
