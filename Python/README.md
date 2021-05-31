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