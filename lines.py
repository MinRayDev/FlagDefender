import os

lines = 0
files = 0


def add(path):
    global lines, files
    for file in os.listdir(path):
        if file.endswith(".py"):
            files += 1
            lines += len(open(os.path.join(path, file), "r").readlines())
        elif "." not in file and "venv" not in file:
            files += 1
            add(os.path.join(path, file))
        elif "venv" not in file:
            files += 1


add(os.getcwd())
print(files, "files")
print(lines, "lines")
