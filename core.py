import os
import re
import shutil
import json
import ffmpeg
from log import logger

rm_src_dir = False

def sanitize_filename(filename):
    # replace illegal characters
    rstr = r'[\/\\\:\*\?\"\<\>\|]'
    new_title = re.sub(rstr, "_", filename)  # 替换为下划线
    return new_title
    # avoid long name
    max_length = 255
    if len(sanitized) > max_length:
        base_name = sanitized[:-4]
        sanitized = base_name[:max_length - 4] + '.mp4'
    return sanitized

def convert_and_merge(src_dir, dset_dir):
    # get title and generate dest mp4 path
    mp4_name = ""
    try:
        with open(os.path.join(src_dir, ".videoInfo"), 'r', encoding='utf-8') as file:
            data = json.load(file)
            mp4_name = sanitize_filename(f'{data["title"]}.mp4')
    except Exception as e:
        logger.error(f'Fail to open file ".videoInfo" in dir "{src_dir}".')
        return
    dest_mp4_path = os.path.join(dset_dir, mp4_name)

    # check the dest mp4 path is not existed
    if os.path.exists(dest_mp4_path):
        logger.warning(f'The file "{mp4_name}" has existed in dest dir.')
        return
    
    # get names of m4s files (first one is video, second one is audio)
    m4s_fnames = [file for file in os.listdir(src_dir) if file.endswith('.m4s')]
    m4s_fpaths = ["",""]
    # delete first 9 bits of m4s file to restore it's data
    for i in range(0, len(m4s_fnames)):
        try:
            m4s_fpaths[i] = src_dir + "\\" + m4s_fnames[i]
            with open(m4s_fpaths[i], "rb") as file:
                data = file.read()
            if data[0:9] == b'\x30\x30\x30\x30\x30\x30\x30\x30\x30':
                new_data = data[9:]
                with open(m4s_fpaths[i], "wb") as file:
                    file.write(new_data)
        except IOError:
            logger.error(f'Fail to read/write file "{m4s_fpaths[0]}".')
            return
    # merge m4s video and m4s audio to mp4
    try:
        (
            ffmpeg.input(m4s_fpaths[0]).output(ffmpeg.input(m4s_fpaths[1]), dest_mp4_path, codec='copy')
            .run(capture_stdout=True, capture_stderr=True)
        )
        if rm_src_dir:
            shutil.rmtree(src_dir)
        logger.info(f'dest mp4 file "{dest_mp4_path}" has been output')
    except Exception as e:
        logger.error(f'Fail to merge "{m4s_fpaths[0]}" and "{m4s_fpaths[1]}" to "{dest_mp4_path}".')
        return

def multiprocess(bili_dir, dest_dir):
    os.chdir(bili_dir)
    subdirectories = [name for name in os.listdir(bili_dir) if os.path.isdir(os.path.join(bili_dir, name))]
    for subdir in subdirectories:
        convert_and_merge(subdir, dest_dir)



