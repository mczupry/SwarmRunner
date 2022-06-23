import os, sys
import subprocess

def execute(cmd, wd = "./"):
        popen = subprocess.Popen(cmd, stdout=subprocess.PIPE, universal_newlines=True, shell = True, cwd = wd)
        for stdout_line in iter(popen.stdout.readline, ""):
            yield stdout_line 
        popen.stdout.close()
        return_code = popen.wait()
        if return_code:
            raise subprocess.CalledProcessError(return_code, cmd)

def get_absolute_path(file):
    if file is None:
        return file
    if not os.path.isabs(file):
        file = f"{os.getcwd()}/{file}"
    return file

def show(prefix, j, count, size=60, out=sys.stdout):
    """Function used to make a progress bar"""
    x = int(size*j/count)
    print(f'{prefix}[{u"#"*x}{"."*(size-x)}] {j}/{count}', end='\r', file=out, flush=True)
    if (j == count):
        print("\n", flush=True, file=out)