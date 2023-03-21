import yaml
import os
import subprocess
import tqdm
import json

KO_FLAGS = ["solver=KO_USE_THOROUPY", "KO_CC=clang-12", "KO_DONT_OPTIMIZE=1", f"METADATA={os.curdir}/ko.yaml"]
ko_flags = ' '.join(KO_FLAGS)
cc = "/workdir/ucsan/build/bin/ko-clang"


all = yaml.load(open("all.yaml", 'r'))

errors = {
    "p1": [],
    "p2": []
}

success = 0
len_all = 0


def execute(command):
    # print(command)
    # return 0
    # return os.system(command)
    p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    return *p.communicate(), p.returncode

def dump():
    global errors
    json.dump(errors , open("errors.json",'w'))

def compile(metadata):
    global errors, success, len_all
    len_all += 1
    path = metadata['_path']
    yaml.dump({"entry": metadata['entry'], "scope": metadata['scope']}, open("ko.yaml", "w"))
    
    execute(f"rm -f {path}")
    stdout, stderr, ret = execute(f"{ko_flags} make CC={cc} {path}")
    if ret != 0:
        errors['p1'].append(
            {"metadata": metadata, 
             "stdout": stdout.decode('latin2'), 
             "stderr":stderr.decode('latin2')
             }
             )
        # dump()
        return
    stdout, stderr, ret = execute(f"{ko_flags} {cc} {path} -o test")
    if ret != 0:
        errors['p2'].append(
            {"metadata": metadata, 
             "stdout": stdout.decode('latin2'), 
             "stderr":stderr.decode('latin2')
             }
             )
        # dump()
        return
    execute(f"rm -f {path}")
    success += 1


pbar = tqdm.tqdm(all)
for item in pbar:
    compile(item)
    pbar.display(f"r: {success/len_all*100 : .2f}%")
    if len_all % 1000 == 0:
        dump()
dump()

yaml.dump(errors, open("errors.yaml", "w"))

print(f"{len(errors)} / {len(all)}")