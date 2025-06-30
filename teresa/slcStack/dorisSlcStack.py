import os
import re

# TODO: 正则匹配表达式不一定正确， debug 的时候，注意一点
# TODO: 注意这里的正则匹配的表达式，只支持一个，如果要支持多个，要新增功能
# TODO: 只支持一天只有衣服数据的，多的数据，要多看

# 还没有实现的地方
# self.dump_data_funcs[radar_type](data_path, date_path)     
# self.dump_header2doris_funcs[radar_type](meta_path, date_path)
# self.get_data_date_funcs
# self.get_meta_date_funcs

# 这些 map 以后要放在一个专门的文件中，然后 import 进来
# 这个 map 是放确定雷达的类型的正则项的
radar_type_pat_map = {
    'LT1': 'LT1*.meta.xml',
    'BC3': 'bc3*slc*.xml',
    'GF3': 'GF3*.meta.xml',
    'FC1': 'spacety_SLC_SM_*.h5'
}

# 这个 map 是用来放不同类型的雷达数据 匹配 meta/xml 的正则项的
is_meta_file = {
    'LT1': lambda x: bool(re.search(r'LT1*.meta.xml', x)),
    'BC3': lambda x: bool(re.search(r'bc3*slc*.xml', x)),
    'GF3': lambda x: bool(re.search(r'GF3*.meta.xml', x)),
    'FC1': lambda x: bool(re.search(r'spacety_SLC_SM_*.h5', x)),
}

# 这个 map 是用来放不同类型的雷达数据 匹配 data 的正则项的
is_data_file = { 
    'LT1': lambda x: bool(re.search(r'LT1*_(H|V)(H|V)_*.tiff', x)),
    'BC3': lambda x: bool(re.search(r'bc3*slc*.h5', x)),
    'GF3': lambda x: bool(re.search(r'GF3*_(H|V)(H|V)_*.tiff', x)),
    'FC1': lambda x: bool(re.search(r'spacety_SLC_SM_*.h5', x)),
}

get_date_of_filename = { 
    'LT1': {'meta': lambda x: re.search(r'LT1.*_(\d{8})', x).group(1),
            'data': lambda x: re.search(r'LT1.*_(\d{8})', x).group(1)},
    'BC3': {'meta': lambda x: re.search(r'bc3.*_(\d{8})', x).group(1),
            'data': lambda x: re.search(r'bc3.*_(\d{8})', x).group(1)},     
    'GF3': {'meta': lambda x: re.search(r'GF3.*_(\d{8})', x).group(1),
            'data': lambda x: re.search(r'GF3.*_(\d{8})', x).group(1)},
    'FC1': {'meta': lambda x: re.search(r'spacety_SLC_SM_(\d{8})', x).group(1),
            'data': lambda x: re.search(r'spacety_SLC_SM_(\d{8})', x).group(1)}
}

class dorisSlcStack():
    def __init__(self, params):
        self.params = params
        # ! 这些输入的参数，要检查一下，文件路径是否存在
        self.data_dir = self.params['Stack_parameters']['dataDirs']
        self.work_dir = self.params['Stack_parameters']['workDir']
        self.master_date = self.params['Stack_parameters']['masterDate']

        self.meta_path_map = dict()
        self.data_path_map = dict()
        self.dates = []
        self.radar_type = ""

        self.initialize()

    def initialize(self):
        """
        Initialize the dorisSlcStack object with parameters.
        """
        if not os.path.exists(self.data_dir):
            raise FileNotFoundError(f"Data directory {self.data_dir} does not exist.")

        # 确定雷达类型
        for radar_type, pattern in radar_type_pat_map.items():
            is_matched = self.check_radar_type(pattern)
            if is_matched:
                self.radar_type = radar_type
                break
        if not self.radar_type:
            raise ValueError("No matching radar type found in the data directory.")
        
        # 初始化 self.data_path_map，其中， key 是日期，value 是日期对应的数据文件路径
        for dirpath, _, filenames in os.walk(os.path.abspath(self.data_dir)):
            for filename in filenames:
                # 通过正则匹配，找到 data 数据文件，初始化 self.data_path_map
                data_file = is_data_file[self.radar_type](filename)
                if data_file:
                    date_str = get_date_of_filename[self.radar_type]['data'](filename)
                    full_path = os.path.join(dirpath, filename)
                    self.data_path_map[date_str] = full_path  

                # 通过正则匹配，找到 meta 元文件，初始化 self.meta_path_map
                meta_file = is_meta_file[self.radar_type](filename)
                if meta_file:
                    date_str = get_date_of_filename[self.radar_type]['meta'](filename)
                    full_path = os.path.join(dirpath, filename)
                    self.meta_path_map[date_str] = full_path   

        # 初始化 self.dates 日期列表  
        #! 其实，这里可以检查一下 meta 和 data 的日期是否一致的，偷懒了 
        self.dates = sorted(set(self.meta_path_map.keys()) | set(self.data_path_map.keys()))

    def check_radar_type(self, pattern):
        """
        Check if the radar type matches the given pattern.
        """
        regex = re.compile(pattern)
        for _, _, filenames in os.walk(self.data_dir, followlinks=True):
            for filename in filenames:
                if regex.match(filename):
                    return True
        return False