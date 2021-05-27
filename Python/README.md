# 2021-0BUG-CV
RoboMaster2021大连理工大学凌BUG战队视觉代码 Python实现

开发者：
- Thyssen Wen
- and so on

开发环境安装
```shell
conda env create -f RMCVenv.yaml
```

开发环境导出
```shell
conda env export  >  env.yaml
```

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