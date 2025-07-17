import os
import re
from utils.logger_util import Logger
from teresa.slcStack.radar_type import radar_type_pat_map, is_meta_file, is_data_file, get_date_from_filename

class dorisSlcStack():
    def __init__(self, params):

        self.logger = Logger().get_logger()

        self.params = params
        # ! 这些输入的参数，要检查一下，文件路径是否存在
        self.data_dir = self.params['stack_parameters']['data_dirs']
        self.work_dir = self.params['stack_parameters']['work_dir']
        self.master_date = self.params['stack_parameters']['masterDate']

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
                # self.logger.debug(f"Processing file: {filename}")
                data_file = is_data_file[self.radar_type](filename)
                # self.logger.debug(f"Is data file: {data_file}")
                if data_file:
                    date_str = get_date_from_filename[self.radar_type]['data'](filename)
                    # self.logger.debug(f"Extracted date string: {date_str} from filename: {filename}")
                    full_path = os.path.join(dirpath, filename)
                    # self.logger.debug(f"Full path for data file: {full_path}")
                    self.data_path_map[date_str] = full_path  


                # 通过正则匹配，找到 meta 元文件，初始化 self.meta_path_map
                meta_file = is_meta_file[self.radar_type](filename)
                if meta_file:
                    date_str = get_date_from_filename[self.radar_type]['meta'](filename)
                    self.logger.debug(f"Extracted date string: {date_str} from filename: {filename}")
                    full_path = os.path.join(dirpath, filename)
                    self.logger.debug(f"Full path for meta file: {full_path}")
                    self.meta_path_map[date_str] = full_path   

        # 初始化 self.dates 日期列表  
        #! 其实，这里可以检查一下 meta 和 data 的日期是否一致的，偷懒了 
        self.dates = sorted(set(self.meta_path_map.keys()) | set(self.data_path_map.keys()))

    def check_radar_type(self, pattern):
        """
        Check if the radar type matches the given pattern.
        """
        regex = re.compile(pattern)

        self.logger.debug(f"Checking radar type with pattern: {pattern}")
        self.logger.debug(f"Compiled regex: {regex}")
        self.logger.debug(f"Searching in directory: {self.data_dir}")

        # 遍历 data_dir 目录下的所有文件，检查是否有匹配
        for _, _, filenames in os.walk(self.data_dir, followlinks=True):
            for filename in filenames:
                self.logger.debug(f"Checking file: {filename}")
                # LT1B_MONO_MYC_STRIP1_013101_E2.1_N49.2_20240726_SLC_HH_S2A_0000464655.meta.xml
                if regex.match(filename):
                    return True
        return False