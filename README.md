# 2021-BUG-CV
RoboMaster2021大连理工大学凌BUG战队视觉代码

开发者：
- Thyssen Wen
- and so on

开发环境
- opencv 4.5.2
- opencv-contribute 4.5.2
- qt creator 5.14.2
- eigen 3.9

# 代码格式规范
- 尽量不使用全局变量
- 函数名、变量名、类名命名有含义
- 注释规范，全英文
## 类注释-类前
```C++
//例子
/**
 * @brief 
 */
```
## 函数注释-函数前
```C++
//例子
/**
 * @brief 
 * @param  src              My Param doc
 * @param  armorDetector    My Param doc
 * @param  config           My Param doc
 * @return true 
 * @return false 
 */
```
## 参数统一
所有的参数，比如二值化阈值、相机参数等，统一写到param_xml文件夹的camera_param.xml文件中，并且在函数Config进行载入。