from os import path
import os, fnmatch


'''
Utils
'''
class utils:
    def print_progress_line(string):
        print '\033[94m  ' + string              + '  \033[0m'
    def print_progress(string):
        print '\033[94m'   + '='*(len(string)+4) + '\033[0m'
        print_progress_line(string)
        print '\033[94m'   + '='*(len(string)+4) + '\033[0m'

    def print_error(string):
        print '\033[31m'   + '='*(len(string)+4) + '\033[0m'
        print '\033[31m  ' + string              + '  \033[0m'
        print '\033[31m'   + '='*(len(string)+4) + '\033[0m'

    def locate1st_dir(pattern, root = os.curdir):
        '''
        Locate first directory matching supplied name pattern (recursively)
        '''
        for path, dirs, files in os.walk(os.path.abspath(root), followlinks=True):
            for dir_name in fnmatch.filter(dirs, pattern):
                return os.path.join(path, dir_name)

    def locate_dirs(pattern, root = os.curdir):
        '''
        Locate all directories matching supplied filename pattern (recursively)
        '''
        for path, dirs, files in os.walk(os.path.abspath(root), followlinks=True):
            for dir_name in fnmatch.filter(dirs, pattern):
                yield os.path.join(path, dir_name)
                
    def locate1st(pattern, root = os.curdir):
        '''
        Locate first file matching supplied filename pattern (recursively)
        '''
        for path, dirs, files in os.walk(os.path.abspath(root), followlinks=True):
            for filename in fnmatch.filter(files, pattern):
                return os.path.join(path, filename)

    def locate(pattern, root = os.curdir):
        '''
        Locate all files matching supplied filename pattern (recursively)
        '''
        for path, dirs, files in os.walk(os.path.abspath(root), followlinks=True):
            for filename in fnmatch.filter(files, pattern):
                yield os.path.join(path, filename)

    def get_image_dirs(dates, nr_bursts, nr_subswaths):
        '''
        Generate image directories of the form DDMMYYYY_SxxBzz
        where DDMMYYYY is the date, xx is the subswath number, and
        zz is the burst number. It returns a list which can be
        indexed to extract the directory corresponding to a specific
        date, burst, and subswath. For example: image_dirs[0][1][4]
        corresponds to the first date, second burst, and fifth subswath
        '''
        nr_dates     = len(dates)
        image_dirs   = [[[None for i in range(nr_subswaths)]
                        for j in range(nr_bursts)]
                        for k in range(nr_dates)]
        for k, item in enumerate(dates):
            for i in range(nr_subswaths):
                for j in range(nr_bursts):            
                    image_dirs[k][j][i] = os.path.join("S%02dB%02d" % (i+1, j+1), dates[k])
        return image_dirs

    def plot_baselines(bperp):
        '''
        Prints baselines
        '''
        bp    = bperp.values()
        mi    = min(bp)
        ra    = max(bp) - mi
        fact  = 70./ra
        for s, b in sorted(bperp.iteritems()):
            print('{0}: {1: 5.0f}'.format(s, b) + ' '*int((b-mi)*fact) + '*')
