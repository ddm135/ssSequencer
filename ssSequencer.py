from glob import glob
from os import path


from ssSEQ import ssSEQ


def seq_batch(seq_folder):
    print("seq | ogg: noteCount / noteCountUncheck (invalid)")
    for seq_file in glob(path.join(seq_folder, '**', '*.seq'), recursive=True):
        seq = ssSEQ(seq_file)
        print(path.basename(seq_file), "|", seq.quick_str())


# noinspection SpellCheckingInspection
def seq_detail(seq_file):
    if not seq_file.endswith(".seq"):
        print("Error: Not a beatmap file.")
        return

    seq = ssSEQ(seq_file)
    print(seq)


def main():
    seq_path = input("Path: ")

    if not path.exists(seq_path):
        print("Error: Invalid path")
    elif path.isdir(seq_path):
        seq_batch(seq_path)
    elif path.isfile(seq_path):
        seq_detail(seq_path)

    print("\nPlease send me a message if the noteCount and noteCountUncheck numbers do not match up.")


if __name__ == "__main__":
    main()
