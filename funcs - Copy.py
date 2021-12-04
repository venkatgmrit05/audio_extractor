import re
import os

regex_audio = re.compile(r'')


def get_sanitized_filename(file_name,
                           file_extn='.mp4',
                           token_joiner='_',
                           intra_splitter='-',
                           limit=5):
    # print(f'input name is {file_name}')
    try:
        file_name_str,*_,extension = file_name.split(file_extn)
        # print(f'token splits : {file_name_str} || {_} || {extension}')
        splitters = []
        for item in file_name_str:
            if not item.isalnum():
                splitters.append(item)
        n_file_name = file_name_str
        for item in set(splitters):
            n_file_name = n_file_name.replace(item,intra_splitter)
        n_file_name = n_file_name.replace(intra_splitter,' ')
        n_file_name_tokens = n_file_name.split()
        if limit:
            sanitized_name = token_joiner.join(n_file_name_tokens[:limit])
        else:
            sanitized_name = token_joiner.join(n_file_name_tokens[:])
        # print(f'sanitized name : {sanitized_name}')
        return sanitized_name
    except Exception as e:
        print(f'error >> {e}')


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

# test
# fn = r'24.Preme Pora Baron -- Cover by Melissa Srivastava.mp4'
#
# print(get_sanitized_filename(fn))
