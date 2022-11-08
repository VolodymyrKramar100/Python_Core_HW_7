import os
from pathlib import Path
import re
import shutil
import sys

dir_suf_dict = dict(Images=[".jpeg", ".jpg", ".png", ".svg"],
                     Video=[".avi", ".mov", ".mp4", "mkv"],
                     Audio=[".mp3", "ogg", ".raw", ".wav", ".wma"],
                     Documents=[".txt", ".docx", ".doc", "pdf", ".xlsx", ".pptx"],
                     Archives=[".tar", ".gz", ".zip"])

def normalize(name: str) -> str:
    cyrillic_symbols = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ'
    translation = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
                    "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "u", "ja", "je", "ji", "g")

    trans = {}
    for c, l in zip(cyrillic_symbols, translation):
        trans[ord(c)] = l
        trans[ord(c.upper())] = l.upper()
    t_name = name.translate(trans)
    t_name = re.sub(r'\W', '_', t_name)
    return t_name


def move_file(dir_p: Path, path_file: Path):
    dir_p.mkdir(exist_ok=True)
    if (Path(dir_p) / path_file.name).exists():
        path_file.rename(dir_p.joinpath(f'{path_file.name[0:-len(path_file.suffix)]}_c{path_file.suffix}'))
        print(f"Можливо дублікат: {path_file.name}")
    else:
        path_file.rename(dir_p / path_file.name)


def extension_comparison(curr_dir: Path, path_file: Path, suf: str) -> bool:
    if path_file.suffix in dir_suf_dict[suf]:
        move_file(Path(curr_dir) / suf, path_file)
        return True
    return False


def name_normalize(root: str, file: str) -> Path:
    path_file = Path(root) / file
    normalize_n = f"{normalize(path_file.name[0:-len(path_file.suffix)])}{path_file.suffix}"
    path_file = path_file.rename(Path(root) / normalize_n)
    return path_file


def remove_dir(subdir: list):
    for path in subdir:
        if len(os.listdir(path)) > 0 or Path(path).name in dir_suf_dict:
            continue
        Path(path).rmdir()


def sort_func(path_d: str) -> tuple:
    curr_dir = Path(path_d)
    subdir = []
    known_extensions, unknown_extensions = set(), set()
    for root, dirs, files in os.walk(path_d):
        for d in dirs:
            if not d:
                continue
            subdir.append(f"{curr_dir / d}")
        for file in files:
            path_file = name_normalize(root, file)
            ex_comp = False
            for suf in dir_suf_dict:
                ex_comp = extension_comparison(curr_dir, path_file, suf)
                if ex_comp:
                    known_extensions.add(path_file.suffix)
                    break
            if not ex_comp:
                move_file(Path(curr_dir) / "Other", path_file)
                unknown_extensions.add(path_file.suffix)

    remove_dir(subdir)
    return list(known_extensions), list(unknown_extensions)


def main():
    known, unknown = "", ""
    path_d = Path(sys.argv[1])
    if not Path(path_d).exists():
        print('Директорії не існує')
    else:
        known, unknown = sort_func(path_d)

    if len(known) >= 0:
        print(f"\nРозпознані розширення:\n{known}")
    if len(unknown) >= 0:
        print(f"Не розпознані розширення:\n{unknown}")

    print('Сортування завершено')


if __name__ == "__main__":
    main()