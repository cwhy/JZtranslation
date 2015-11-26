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

while True:
    command = input(">> ")
    if command == "exit" or (not command):
        break
    elif command in file_list:
        edit(command)
    elif command == "next":
        for _file_name in glob.glob(op.join(TR_DIR, '*.json')):
            file_list.remove(_file_name.split('/')[-1].split('.')[0])
        edit(sorted(file_list)[0])
    else:
        command = input(">> ")



