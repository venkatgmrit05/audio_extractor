""
import os
import moviepy.editor as mpe


class ExtractAudio(object):

    def __init__(self,
                 name='aex_1',
                 counter_limit=10):
        self.name = name
        self.counter_limit = counter_limit

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
