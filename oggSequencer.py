import audiofile

from glob import glob
from os import path, rename


# Folder mode
def ogg_batch(ogg_folder):
    a_byte_files = glob(path.join(ogg_folder, '**', '*.a.bytes'), recursive=True)
    for a_byte_file in a_byte_files:
        rename(path.abspath(a_byte_file), path.splitext(path.abspath(a_byte_file))[0] + '.ogg')

    ogg_files = glob(path.join(ogg_folder, '**', '*.ogg'), recursive=True)

    if ogg_files:
        print("ogg: duration")
        for ogg_file in ogg_files:
            if audiofile.duration(ogg_file) > 13:
                minutes = int(audiofile.duration(ogg_file) // 60)
                seconds = int(audiofile.duration(ogg_file) % 60)
                print(f"{path.basename(ogg_file)}: {minutes}:{seconds}")
    else:
        print("Error: No audio file in folder")


# File mode
def ogg_details(ogg_file):
    if not ogg_file.endswith('.a.bytes', '.ogg'):
        print("Error: Not an audio file")
    else:
        minutes = int(audiofile.duration(ogg_file) // 60)
        seconds = int(audiofile.duration(ogg_file) % 60)
        print(f"{path.basename(ogg_file)}: {minutes}:{seconds}")


def main():
    ogg_path = input("Path: ")

    if not path.exists(ogg_path):
        print("Error: Invalid path")
    elif path.isdir(ogg_path):
        ogg_batch(ogg_path)
    elif path.isfile(ogg_path):
        ogg_details(ogg_path)


if __name__ == "__main__":
    main()
