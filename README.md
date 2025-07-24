TERESA
======


Teresa (Terrain Registration and Sampling Software) 是由西北工业大学电子信息学院 APRILab 团队自主研发的一款面向国产卫星的 SAR 图像批量配准工具。该工具以欧洲开发的 SAR 处理软件 DORIS 为基础，进行了深入的定制与优化，专门针对中国国产合成孔径雷达（SAR）卫星数据的特点进行适配与增强。

当前版本的 Teresa 已成功支持包括 Lutan-1（LT1）、BC3 和 BC4 等国产主力 SAR 卫星的图像数据处理，能够在保持高精度配准效果的同时，大幅提升处理效率与稳定性。工具支持自动化批量处理流程，适用于大规模干涉图生成、地表形变监测和相关 InSAR 应用。

未来版本将持续扩展更多国产SAR平台的兼容性，并进一步集成智能配准算法与并行加速框架，服务于国产遥感数据处理的自主可控与工程化落地。

------------------------------------------------------------

📦 安装方式
---------

方法一：克隆项目并安装依赖（conda 环境下）

    git clone https://github.com/aprilab-dev/teresa.git
    conda env create -f environment.yml 

方法二：通过 pip 安装（如已发布）！！！！！！！

    pip install teresa

------------------------------------------------------------

🚀 快速开始
---------
 安装 doris 

通过导入配置文件运行：

    python main.py templates/doris.parms

配置文件 doris.parms 中的参数

------------------------------------------------------------

⚙️ 配置文件 doris.params 参数说明
----------

参数             | 说明                             | 示例值
----------------|----------------------------------|--------------------------
work_dir      | 主工作目录                         | /data/tests/user
--slave          | 从图像路径                       | gf3a_20240501_slc.tif
--method         | 配准方法（cross / phase / fft） | phase
--roi            | 感兴趣区域 (lat1,lat2,lon1,lon2) | 34.2,34.8,108.9,109.5
--out            | 输出结果路径                     | output/reginfo.txt

------------------------------------------------------------

📁 项目结构
----------

    teresa/
    ├── log/           日志文件生成目录
    ├── templates/     参数文件目录
    ├── teresa/        配准逻辑实现
    ├── utils/         工具函数
    ├── cli.py         命令行文件
    ├── setup.py       命令行文件
    ├── main.py        主程序入口
    └── README.md      项目说明文档

------------------------------------------------------------

🧪 示例数据
----------

运行示例：

    python main.py templates/doris.params

输出日志保存在结果保存在 `output/` 文件夹中，包括配准偏移、精度估计和处理日志。

------------------------------------------------------------

👥 开发团队
----------

APRILab  
Applied Processing & Remote-sensing Intelligence Lab  
西北工业大学 电子信息学院 无限抗干扰研究所  
联系邮箱：yuxiao.qin@nwpu.edu.cn  
项目主页：https://aprilab.example.org

------------------------------------------------------------

📜 许可证
--------

本项目采用 MIT License 开源。详见 LICENSE 文件。

------------------------------------------------------------

📘 缩写解释
---------

SAR   : Synthetic Aperture Radar  
SLC   : Single Look Complex  
ROI   : Region of Interest  
RMSE  : Root Mean Square Error  
GF-3A : GaoFen-3A 卫星

------------------------------------------------------------

🧭 贡献指南
---------

欢迎任何形式的贡献，包括 issue、代码提交（PR）或文档补充。  

------------------------------------------------------------