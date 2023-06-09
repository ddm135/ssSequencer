from pathlib import Path


from ssSEQ import ssSEQ


# Folder mode
def seq_batch(seq_folder):
    seq_detected = False
    seq_files = seq_folder.rglob('*.seq')

    if seq_files:
        seq_detected = True
        print("seq | ogg: noteCount / noteCountUncheck (invalid)")
        for seq_file in seq_files:
            seq = ssSEQ(seq_file)
            print(seq_file.name, "|", seq)
    else:
        print("Error: No beatmap file in folder.")

    return seq_detected


# File mode
def seq_details(seq_file):
    seq_detected = False

    if seq_file.suffix != '.seq':
        print("Error: Not a beatmap file.")
        return seq_detected

    seq = ssSEQ(seq_file)
    print(repr(seq))
    seq_detected = True

    return seq_detected


def main():
    seq_detected = False
    seq_path = Path(input("Path: "))

    if not seq_path.exists():
        print("Error: Invalid path")
    elif seq_path.is_dir():
        seq_detected = seq_batch(seq_path)
    elif seq_path.is_file():
        seq_detected = seq_details(seq_path)

    if seq_detected:
        print("\nPlease send me a message if the noteCount and noteCountUncheck numbers do not match up.")


if __name__ == "__main__":
    main()
