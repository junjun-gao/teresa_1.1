import os
import shutil
from datetime import datetime
from utils.TeresaLog import global_log

from teresa.processor.dorisProcessor import dorisProcessor
from teresa.dump.dump_funcs_map import dump_header2doris_funcs, dump_data_funcs 

class dorisCoregistion():
    def __init__(self, params, slc_stack):
        self.slc_stack = slc_stack
        self.params    = params
        self.doris     = dorisProcessor(params)
    
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
            self.read_files(date)

        # 4. 确定 master ，并且把对应的复制到 master 文件夹中，
        self.get_master()

        # 5. 执行 doris 的核心处理流程
        for date in self.slc_stack.dates:
            if date == self.slc_stack.master_date:
                continue

            # 这里的 date_dir 是指每个日期对应的文件夹
            date_dir = self.slc_stack.work_dir + os.sep + "workspace" + os.sep + date

            global_log.start_task(self.get_task_info(date))
            
            self.doris.coarseorb(date_dir)
            self.doris.coarsecorr(date_dir)
            self.doris.fine(date_dir)
            self.doris.coregpm(date_dir)
            self.doris.resample(date_dir)
            self.doris.interfero(date_dir)

            global_log.end_task(success=True)

        # 6. 生成 dem 文件
        global_log.start_dem()

        dem_path = self.slc_stack.work_dir + os.sep + "workspace" + os.sep + "dem"
        self.doris.dem(dem_path)

        global_log.end_dem()

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
            # 每个日期对应的工作目录
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
        if not os.path.exists(dorisin_path):
            os.makedirs(dorisin_path)
            cp_cmd = f"cp ./teresa/processor/dorisin/*.dorisin {dorisin_path}"
            os.system(cp_cmd)

    def write_params_to_dorisin(self):
        """
        Write the parameters to the dorisin file.
        """
        for dorisin, params in self.params.items():
            if dorisin == "stack_parameters":
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
                        updated_lines.append(f"{param}    {value}\n")
                        modified = True
                    else:
                        updated_lines.append(line)
                # 写入参数值
                if modified:
                    with open(dorisin_path, 'w', encoding='utf-8') as f:
                        f.writelines(updated_lines)

    def read_files(self, date):
        """
        Read files from the specified date path.
        
        Parameters:
            date_path (str): The path to the date directory.
        """
        # 转为 "2024-07-18" 格式字符串
        dt = datetime.strptime(date, "%Y%m%d")
        formatted_date = dt.strftime("%Y-%m-%d")
        global_log.start_read(formatted_date)

        # 两个参数，一个是 data 数据的路径，一个是 date 日期对应的工作路径，只差一个字母，不要混淆
        date_dir = self.slc_stack.work_dir + os.sep + "workspace" + os.sep + date

        image_path = os.path.join(date_dir, "image.raw")
        resFile_path = os.path.join(date_dir, "slave.res")  
        if os.path.exists(image_path) and os.path.exists(resFile_path):
            global_log.read_status("SKIPPED")
            return

        radar_type = self.slc_stack.radar_type
        meta_name = os.path.basename(self.slc_stack.meta_path_map[date])
        data_name = os.path.basename(self.slc_stack.data_path_map[date])

        global_log.read_meta(os.path.basename(meta_name))
        meta_symlink = os.path.join(date_dir, meta_name)
        dump_header2doris_funcs[radar_type](meta_symlink, date_dir)

        global_log.read_data(os.path.basename(data_name))
        data_symlink = os.path.join(date_dir, data_name)
        dump_data_funcs[radar_type](data_symlink, date_dir)      

        global_log.read_status("SUCCESS") 


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

    def get_task_info(self, date):
        """
        Get the task information for logging.
        
        Parameters:
            date (str): The date of the task.
        
        Returns:
            dict: A dictionary containing the task information.
        """
        # 转为 "2024-07-18" 格式字符串
        dt = datetime.strptime(date, "%Y%m%d")
        formatted_date = dt.strftime("%Y-%m-%d")

        return {
            "processing_date": formatted_date,
            "meta_file": os.path.basename(self.slc_stack.meta_path_map[date]),
            "data_file": os.path.basename(self.slc_stack.data_path_map[date]),
            "master": self.slc_stack.master_date,
            "slave": date
        }
