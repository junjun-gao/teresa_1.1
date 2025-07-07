import os
import subprocess

# DorisExpert
class dorisProcessor():
    def __init__(self, params):
        self.params = params   

    def _doris(self, arg):
        _DORIS = os.getenv('STACK_BUILDER_DORIS', '/home/junjun/.local/doris/doris')  
        return subprocess.call([_DORIS, arg])
    
    def coarseorb(self, path):
        os.chdir(path)
        if os.path.exists('coreg.out'):
            with open('coreg.out') as coreg_out:
                if [line for line in coreg_out if 'coarse_orbits:' in line][0].split()[1] == '1':
                    print('Coarse orbit already done, skipping...')
                    return

        self._doris('../dorisin/coarseorb.dorisin')


    def coarsecorr(self, path):
        os.chdir(path)
        if os.path.exists('coreg.out'):
            with open('coreg.out') as coreg_out:
                if [line for line in coreg_out if 'coarse_correl:' in line][0].split()[1] == '1':
                    print('Coarse coregistration already done, skipping...')
                    return

        self._doris('../dorisin/coarsecorr.dorisin')


    def fine(self, path):
        os.chdir(path)
        if os.path.exists('coreg.out'):
            with open('coreg.out') as coreg_out:
                if [line for line in coreg_out if 'fine_coreg:' in line][0].split()[1] == '1':
                    print('Fine coregistration already done, skipping...')
                    return

        self._doris('../dorisin/fine.dorisin')



    def coregpm(self, path):
        os.chdir(path)
        if os.path.exists('coreg.out'):
            with open('coreg.out') as coreg_out:
                if [line for line in coreg_out if 'comp_coregpm:' in line][0].split()[1] == '1':
                    print('Computation of coregistration polynomial already done, skipping...')
                    return

        self._doris('../dorisin/coregpm.dorisin')

    def resample(self, path):
        
        os.chdir(path)
        if os.path.exists('slave.res'):
            with open('slave.res') as coreg_out:
                if [line for line in coreg_out if 'resample:' in line][0].split()[1] == '1':
                    print('Resample slave already done, skipping...')
                    return

        self._doris('../dorisin/resample.dorisin')
    
    def dem(self, path):
        os.chdir(path)
        if os.path.exists('coreg.out'):
            with open('coreg.out') as coreg_out:
                if [line for line in coreg_out if 'dem_assist:' in line][0].split()[1] == '1':
                    print('DEM-based coregistration already done, skipping...')
                    return

        self._doris('../dorisin/dem.dorisin')
