/*
 * @Author: Thyssen Wen
 * @Date: 2021-05-26 10:47:42
 * @LastEditors: Thyssen Wen
 * @LastEditTime: 2021-05-26 14:36:12
 * @Description: load config function implement
 * @FilePath: /DLLG-2021-BUG-CV/src/Config.cpp
 */
#include "Config.h"

/**
 * @brief Construct a new Config:: Config object
 * @param  FILEROOT         My Param doc
 */
Config::Config(std::string FILEROOT)
{
    loadConfig(FILEROOT);
}

/**
 * @brief Destroy the Config:: Config object
 */
Config::~Config()
{
}

/**
 * @brief load config param from file
 * @param  FILEROOT         My Param doc
 */
void Config::loadConfig(std::string FILEROOT)
{
    cv::FileStorage fsRead(FILEROOT, cv::FileStorage::READ);

    if(!fsRead.isOpened())
    {
        std::cout << "failed to open xml" << std::endl;
        return;
    }

    fsRead["Y_DISTANCE_BETWEEN_GUN_AND_CAM"] >> Y_DISTANCE_BETWEEN_GUN_AND_CAM;
    fsRead["Z_DISTANCE_BETWEEN_MUZZLE_AND_CAM"] >> Z_DISTANCE_BETWEEN_MUZZLE_AND_CAM;
    fsRead["Camera_Matrix"] >> CameraIntrinsicMatrix;
    fsRead["Distortion_Coefficients"] >> DistortionCoefficient;
    return;
}