# 2021-0BUG-CV
RoboMaster2021大连理工大学凌BUG战队视觉代码 Python实现

开发者：
- Thyssen Wen
- and so on

开发环境安装
```shell
conda env create -f RMCVenv.yaml
pip install -r requirement.txt
```

开发环境导出
```shell
conda env export  >  RMCVenv.yaml
pip freeze > requirement.txt
```

# 开发进度

|功能|描述|进度|
| -----------| -----------| ----------- |
| 全局日志功能|使用logging函数即可写日志，支持多系统和进程安全|100%|
| 装甲板检测|灯条proposal + 小型卷积神经网络|70%(未训练网络)|
| 多进程运行|可以切换单核和多核运行，提升运行速度|90%|
| 统一配置文件|通过统一的函数接口获得所有设置参数|100%|
| 能量机关击打|检测和打击能量机关|0%|
| 角度解算|解算图片和世界坐标获得枪管移动参数|0%|
| 串口通信|与下位机进行串口通信|0%|


# 代码格式规范
- 尽量不使用全局变量
- 函数名、变量名、类名命名有含义
- 注释规范，全英文

## 类注释-类里
```python
# 例子
"""
summary
"""
```
## 函数注释-函数里
```python
# 例子
"""
proposal use hsv model

Args:
    img (cv::mat): src image
    enermy_color (enum): detetor enermy color

Returns:
    contours var: rect poposal
"""
```
## 参数统一
所有的参数，比如二值化阈值、相机参数等，统一写到param_xml文件夹的camera_param.xml文件中，并且在函数Config进行载入。

## 文件说明
2021.05.31日python文件结构
```
.
├── DataSet - 数据集
│   ├── README.md
│   ├── picture - 图片数据集
│   │   ├── picture1.jpg
│   │   ├── picture2.jpg
│   │   ├── picture3.jpg
│   │   ├── picture4.jpg
│   │   └── picture5.jpg
│   └── video - 视频
│       └── smallDataset.mp4
├── Debug - debug文件夹，运行时的缓存地址
│   ├── logs - 需手动创建，存储日志文件
│   │   ├── running.lock
│   │   └── running.log
│   └── outputVideo.mp4
├── LICENSE
├── Python - python版本目录
│   ├── README.md
│   ├── RMCVenv.yaml - conda环境配置
│   ├── __pycache__
│   │   └── run.cpython-38.pyc
│   ├── armor - 装甲板检测功能
│   │   ├── __init__.py
│   │   ├── __pycache__
│   │   │   ├── __init__.cpython-38.pyc
│   │   │   ├── classify.cpython-38.pyc
│   │   │   └── proposal.cpython-38.pyc
│   │   ├── classify.py
│   │   └── proposal.py
│   ├── config - 参数设置功能
│   │   ├── __init__.py
│   │   ├── __pycache__
│   │   │   ├── __init__.cpython-38.pyc
│   │   │   └── config.cpython-38.pyc
│   │   ├── config.conf
│   │   ├── config.py
│   │   └── logging_config.yaml
│   ├── energy - 能量机关功能
│   │   └── __init__.py
│   ├── logger - 日志功能
│   │   ├── __init__.py
│   │   ├── __pycache__
│   │   │   ├── __init__.cpython-38.pyc
│   │   │   └── logger.cpython-38.pyc
│   │   └── logger.py
│   ├── main.py - 程序开始入口
│   ├── multiProcess - 多进程功能
│   │   ├── __pycache__
│   │   │   ├── multiProcessManager.cpython-38.pyc
│   │   │   ├── runFunc.cpython-38.pyc
│   │   │   └── runProcess.cpython-38.pyc
│   │   ├── multiProcessManager.py
│   │   ├── runFunc.py
│   │   └── runProcess.py
│   ├── requirement.txt - 批评环境文件
│   ├── serial - 串口
│   │   └── serial.py
│   ├── shot - 角度解算功能
│   │   ├── __init__.py
│   │   ├── __pycache__
│   │   │   ├── __init__.cpython-38.pyc
│   │   │   └── angleSlove.cpython-38.pyc
│   │   └── angleSlove.py
│   └── train_classifier.py - 训练网络和采集数据集脚本
├── README.md
```