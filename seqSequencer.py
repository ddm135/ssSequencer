from glob import glob
from os import path


from ssSEQ import ssSEQ


# Folder mode
def seq_batch(seq_folder):
    seq_detected = False
    seq_files = glob(path.join(seq_folder, '**', '*.seq'), recursive=True)

    if seq_files:
        seq_detected = True
        print("seq | ogg: noteCount / noteCountUncheck (invalid)")
        for seq_file in seq_files:
            seq = ssSEQ(seq_file)
            print(path.basename(seq_file), "|", seq.quick_str())
    else:
        print("Error: No beatmap file in folder.")

    return seq_detected


# File mode
def seq_details(seq_file):
    seq_detected = False

    if not seq_file.endswith('.seq'):
        print("Error: Not a beatmap file.")
        return seq_detected

    seq = ssSEQ(seq_file)
    print(seq)
    seq_detected = True

    return seq_detected


def main():
    seq_detected = False
    seq_path = input("Path: ")

    if not path.exists(seq_path):
        print("Error: Invalid path")
    elif path.isdir(seq_path):
        seq_detected = seq_batch(seq_path)
    elif path.isfile(seq_path):
        seq_detected = seq_details(seq_path)

    if seq_detected:
        print("\nPlease send me a message if the noteCount and noteCountUncheck numbers do not match up.")


if __name__ == "__main__":
    main()
