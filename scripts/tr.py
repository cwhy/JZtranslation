import os
import os.path as op
import glob
from subprocess import call
import shutil

TR_DIR = op.join(op.pardir, 'translate')
CN_DIR = op.join(op.pardir, 'Chinese')
EDITOR = os.environ.get('EDITOR', 'vim')


def edit(file_id):
    file_name_orig = op.join(CN_DIR, file_id + '.md')
    file_name = op.join(TR_DIR, file_id + '.md')
    if not op.isfile(file_name):
        shutil.copy(file_name_orig, file_name)
    call([EDITOR, file_name])


os.makedirs(TR_DIR, exist_ok=True)
file_list = set()
for _file_name in glob.glob(op.join(CN_DIR, '*.md')):
    file_list.add(_file_name.split('/')[-1].split('.')[0])

current_file_id = ""
command = input(">> ")
while command:
    if command == "exit":
        break
    elif command in file_list:
        edit(command)
        command = input(">> ")
    elif command == "next":
        for _file_name in glob.glob(op.join(TR_DIR, '*.json')):
            file_list.discard(_file_name.split('/')[-1].split('.')[0])
        current_file_id = sorted(file_list)[0]
        edit(current_file_id)
        command = input(">> ")
    elif command == "complete" and current_file_id:
        _file_name_orig = op.join(CN_DIR, current_file_id + '.json')
        _file_name = op.join(TR_DIR, current_file_id + '.json')
        shutil.copy(_file_name_orig, _file_name)
        command = input(">> ")
    else:
        command = input(">> ")

