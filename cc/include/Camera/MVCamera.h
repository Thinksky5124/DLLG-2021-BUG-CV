#ifndef _MVCAMERA_H_
#define _MVCAMERA_H_

#include "CameraApi.h"  //相机SDK头文件

#include <iostream>
#include <opencv2/opencv.hpp>

using namespace std;
using namespace cv;

class MVCamera
{
public:
  static CameraHandle hCamera;
  static tSdkCameraCapbility tCapability;

  static BYTE *pbyBuffer;
  static BYTE *g_pRgbBuffer;

  static void Init();
  static void UnInit();
  static void GetFrame(Mat &frame);

private:
  MVCamera();
};


#endif
