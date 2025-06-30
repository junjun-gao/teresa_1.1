import os

work_dir = "/home/junjun/junTeresa/templates/dor"
with open(work_dir) as coreg_out:
    print(os.path.basename(work_dir))
