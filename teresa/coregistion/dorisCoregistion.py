import os
import shutil
from coregistion.coregistion import coregistration
from teresa.processor.DorisExpert import DorisExpert

# 还没有实现的地方
# 这两个，也是要单独放在一个文件中，然后 import 进来
# self.dump_data_funcs[radar_type](data_path, date_path)     
# self.dump_header2doris_funcs[radar_type](meta_path, date_path)
# anotation

class dorisCoregistion(coregistration):
    def __init__(self, slc_stack, params):
        self.slc_stack = slc_stack
        self.params    = params
        self.doris     = DorisExpert()
    
    def run(self):
        """
        Run the coregistration process.
        """
        # 1. 创建工作路径
        self.create_work_dir()

        # 2. 将参数写入 dorisin 文件中
        self.write_params_to_dorisin()

        # 3. 用 python 脚本实现 国产卫星数据的 的 读入 和 crop 操作 。
        for date in self.slc_stack.dates:
            date_path = self.slc_stack.work_dir + os.sep + "workspace" + os.sep + date
            self.read_files(date, date_path)

        # 4. 确定 master ，并且把对应的复制到 master 文件夹中，
        self.get_master()

        # 5. 执行 doris 的核心处理流程
        for date in self.slc_stack.dates:
            if date == self.slc_stack.master_date:
                continue
            # 这里的 date_path 是指每个日期对应的文件夹
            # TODO 尝试用 多进程/多线程 实现，考虑一下日志要怎么处理
            date_path = self.slc_stack.work_dir + os.sep + date
            self.doris.coarseorb(date_path)
            self.doris.coarsecorr(date_path)
            self.doris.fine(date_path)
            self.doris.coregpm(date_path)
            self.doris.resample(date_path)
            self.doris.dem(date_path)

    def create_work_dir(self):
        """
        Create the working directory for coregistration.
        """
        # 生成工作目录
        work_dir = self.slc_stack.work_dir + os.sep + "workspace"
        if not os.path.exists(work_dir):
            os.makedirs(work_dir)
        
        # 生成 dem 目录
        dem_path = work_dir + os.sep + "dem"
        if not os.path.exists(dem_path):
            os.makedirs(dem_path)

        # 生成 master 目录
        master_path = work_dir + os.sep + "master"
        if not os.path.exists(master_path):
            os.makedirs(master_path)

        # 生成所有 date 的目录
        for date in self.slc_stack.dates:
            date_path = work_dir + os.sep + date
            if not os.path.exists(date_path):
                os.makedirs(date_path)

            # 创建 meta 和 数据文件 的软连接
            src_meta = self.slc_stack.meta_path_map[date]
            dst_meta = date_path + os.sep + os.path.basename(src_meta)
            if not os.path.exists(dst_meta):
                os.symlink(src_meta, dst_meta)

            src_data = self.slc_stack.data_path_map[date]
            dst_data = date_path + os.sep + os.path.basename(src_data)
            if not os.path.exists(dst_data):
                os.symlink(src_data, dst_data)
        
        # 生成 dorisin 目录
        dorisin_path = work_dir + os.sep + "dorisin"
        os.makedirs(dorisin_path)
        cp_cmd = f"cp ../processor/dorisin/*.dorisin {dorisin_path}"
        os.system(cp_cmd)

    def write_params_to_dorisin(self):
        """
        Write the parameters to the dorisin file.
        """
        for dorisin, params in self.params.items():
            if dorisin == "Stack_parameters":
                continue
            dorisin_path = self.slc_stack.work_dir + os.sep + "workspace" + os.sep + "dorisin" + os.sep + dorisin + ".dorisin"
            for param, value in params.items():
                with open(dorisin_path, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                # 确定参数是否是需要重新写入
                updated_lines = []
                modified = False
                for line in lines:
                    if line.startswith(param):
                        updated_lines.append(f"{param}{value}\n")
                        modified = True
                    else:
                        updated_lines.append(line)
                # 写入参数值
                if modified:
                    with open(dorisin_path, 'w', encoding='utf-8') as f:
                        f.writelines(updated_lines)

    def read_files(self, date, date_path):
        """
        Read files from the specified date path.
        
        Parameters:
            date_path (str): The path to the date directory.
        """
        radar_type = self.slc_stack.radar_type

        # 两个参数，一个是 data 数据的路径，一个是 date 日期对应的工作路径，只差一个字母，不要混淆
        data_path = self.slc_stack.data_path_map[date]
        self.dump_data_funcs[radar_type](data_path, date_path)       # ! 函数里又要判断是否已经存在的逻辑，如果已经存在就不要重新执行了

        meta_path = self.slc_stack.meta_path_map[date]
        self.dump_header2doris_funcs[radar_type](meta_path, date_path)
        
    def get_master(self):
        """
        Determine the master image and copy it to the master folder.
        """
        master_data_path = self.slc_stack.work_dir + os.sep + "workspace" + os.sep + self.slc_stack.master_date + os.sep + "image.raw"
        if not os.path.exists(master_data_path):
            raise FileNotFoundError(f"Master data file not found: {master_data_path}")
        
        # 生成 master 的数据文件软连接
        master_symlink_path = self.slc_stack.work_dir + os.sep + "workspace" + os.sep + "master" + os.sep + "image.raw"
        if not os.path.exists(master_symlink_path):
            os.symlink(master_data_path, master_symlink_path)

        # 生成 master 的 res 文件
        master_res_path = self.slc_stack.work_dir + os.sep + "workspace" + os.sep + "master" + os.sep + "master.res"
        date_res_path = self.slc_stack.work_dir + os.sep + "workspace" + os.sep + self.slc_stack.master_date + os.sep + "slave.res"
        if not os.path.exists(master_res_path):
            with open(master_res_path, 'w') as master_res:
                for line in open(date_res_path):
                    master_res.write(line.replace('image.raw', '../master/image.raw'))
        
        # 生成 slavedem 的 res 文件
        slavedem_res_path = self.slc_stack.work_dir + os.sep + "workspace" + os.sep + "dem" + os.sep + "slavedem.res"
        if not os.path.exists(slavedem_res_path):
            shutil.copyfile(master_res_path, slavedem_res_path)
