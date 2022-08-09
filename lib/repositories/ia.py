import json
import os
from internetarchive import get_item


def sizeof_fmt(num, suffix="B"):
    for unit in ["", "Ki", "Mi", "Gi", "Ti", "Pi", "Ei", "Zi"]:
        if abs(num) < 1024.0:
            return f"{num:3.1f}{unit}{suffix}"
        num /= 1024.0
    return f"{num: .1f}Yi{suffix}"


class InternetArchive:

    dirs = set()

    def __init__(self, url):
        self.url = url
        self.get_item()

    def get_item(self):
        self.item = get_item(self.url)
        return self.item

    def get_download_path(self):
        self.path = f"https://{self.item.item_metadata['d1']}{self.item.item_metadata['dir']}"
        return self.path

    def files_from_folder(self, dir):
        files = self.item.item_metadata['files']
        for file in files:
            if file['name'].startswith(f'{dir}/') or (dir in ('','/') and '/' not in file['name']):
                yield file

    def folders(self):
        files = self.item.item_metadata['files']
        for file in files:
            self.dirs.add(f"{os.path.dirname(file['name'])}")
        return list(self.dirs)


if __name__ == "__main__":
    ia = InternetArchive("En-ROMs")
    for i in ia.list_files_from_dir("DATs"):
        print(i['name'])

    print(ia.folders())
    # , sizeof_fmt(i['size'])
    # print(json.dumps(ia.item.item_metadata, indent=4))
