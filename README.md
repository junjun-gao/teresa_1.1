TERESA
======

Tool for Enhanced Registration of Earth SAR imagery Automatically  
一个由 APRILab 开发的高效国产 SAR 图像批量配准工具。

------------------------------------------------------------

✨ 功能亮点
---------

- 支持国产卫星（lt1, bc3, bc4等）SAR 图像的批量配准
- 亚像素精度估计，配准精度优于 0.1 像素
- 多种配准方法（互相关、频域方法、相位差）
- 输出配准结果与质量指标（RMSE、偏移矢量等）
- 命令行工具，模块化架构，便于集成与扩展

------------------------------------------------------------

📦 安装方式
---------

方法一：克隆项目并安装依赖

    git clone https://github.com/aprilab-dev/teresa.git
    cd teresa
    pip install -r requirements.txt

方法二：通过 pip 安装（如已发布）

    pip install teresa

------------------------------------------------------------

🚀 快速开始
---------

命令行运行：

    teresa teresa.py templates/doris.parms

也可通过配置文件运行：

    python main.py templates/doris.parms

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