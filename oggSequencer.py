import audiofile


from pathlib import Path


# Folder mode
def ogg_batch(ogg_folder):
    a_byte_files = ogg_folder.rglob('*.a.bytes')
    for a_byte_file in a_byte_files:
        a_byte_file.rename(a_byte_file.with_suffix('.ogg'))

    ogg_files = ogg_folder.rglob('*.a.ogg')

    if ogg_files:
        print("ogg: duration")
        for ogg_file in ogg_files:
            ogg_dur = audiofile.duration(ogg_file)
            if ogg_dur > 13:
                minutes, seconds = dur_split(ogg_dur)
                print(f"{ogg_file.name}: {minutes}:{seconds}")
            ogg_file.rename(ogg_file.with_suffix('.bytes'))
    else:
        print("Error: No audio file in folder")


# File mode
def ogg_details(ogg_file):
    if ogg_file.name.endswith('.a.bytes'):
        ogg_file.rename(ogg_file.with_suffix('.ogg'))
        ogg_file = ogg_file.with_suffix('.ogg')

    if ogg_file.suffix != '.ogg':
        print("Error: Not an audio file")
    else:
        ogg_dur = audiofile.duration(ogg_file)
        if ogg_dur > 13:
            minutes, seconds = dur_split(ogg_dur)
            print(f"{ogg_file.name}: {minutes}:{seconds}")
        ogg_file.rename(ogg_file.with_suffix('.bytes'))


def dur_split(dur):
    minutes = int(dur // 60)
    seconds = int(dur % 60)
    return minutes, seconds


def main():
    ogg_path = Path(input("Path: "))

    if not ogg_path.exists():
        print("Error: Invalid path")
    elif ogg_path.is_dir():
        ogg_batch(ogg_path)
    elif ogg_path.is_file():
        ogg_details(ogg_path)


if __name__ == "__main__":
    main()
