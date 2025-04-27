import os
import subprocess

if __name__ == '__main__':
    subprocess.check_call(['gftools.exe', 'builder', 'sources/config.yaml'])
    os.remove('sources/build.ninja')
    os.remove('sources/.ninja_log')
