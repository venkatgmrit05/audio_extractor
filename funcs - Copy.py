import re

regex_audio = re.compile(r'')


def get_sanitized_filename(file_name,
                           file_extn='.mp4',
                           token_joiner='_',
                           intra_splitter='-',
                           limit=5):
    print(f'input name is {file_name}')
    try:
        file_name_str,*_,extension = file_name.split(file_extn)
        print(f'{file_name_str} || {_} || {extension}')
        splitters = []
        for item in file_name_str:
            if not item.isalpha():
                splitters.append(item)
        n_file_name = file_name_str
        for item in set(splitters):
            n_file_name = n_file_name.replace(item,intra_splitter)
        n_file_name = n_file_name.replace(intra_splitter,' ')
        n_file_name_tokens = n_file_name.split()
        sanitized_name = token_joiner.join(n_file_name_tokens[:limit])
        return sanitized_name
    except Exception as e:
        print(f'error >> {e}')

# fn = r'24.Preme Pora Baron -- Cover by Melissa Srivastava.mp4'
#
# print(get_sanitized_filename(fn))
