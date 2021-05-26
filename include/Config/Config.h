/*
 * @Author: Thyssen Wen
 * @Date: 2021-05-26 10:47:59
 * @LastEditors: Thyssen Wen
 * @LastEditTime: 2021-05-26 14:13:50
 * @Description: load config function header
 * @FilePath: /DLLG-2021-BUG-CV/include/Config.h
 */

#include "opencv2/opencv.hpp"
#include <vector>

/**
 * @brief storage and load config class 
 */
class Config
{
private:
    
public:
    Config(std::string FILEROOT);
    ~Config();
    void loadConfig(std::string FILEROOT);

    cv::Mat CameraIntrinsicMatrix; //相机内参矩阵
    cv::Mat DistortionCoefficient; //相机畸变系数
    //单位为mm
    std::vector<cv::Point3f> POINT_3D_OF_ARMOR_BIG;
    std::vector<cv::Point3f> POINT_3D_OF_ARMOR_SMALL;
    float Y_DISTANCE_BETWEEN_GUN_AND_CAM;//如果摄像头在枪管的上面，这个变量为正
    float Z_DISTANCE_BETWEEN_MUZZLE_AND_CAM;//如果摄像头在枪口的后面，这个变量为正
    float BINARY_THRESHOLD;
};

