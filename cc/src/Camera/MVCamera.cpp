#include "MVCamera.h"

//
CameraHandle MVCamera::hCamera;
tSdkCameraCapbility MVCamera::tCapability;

BYTE *MVCamera::pbyBuffer = NULL;
BYTE *MVCamera::g_pRgbBuffer = NULL;

//
MVCamera::MVCamera()
{
}

//
void MVCamera::Init()
{
  CameraSdkStatus iStatus;
  tSdkCameraDevInfo tCameraEnumList;
  int iCameraCounts = 1;

  //相机SDK初始化。在调用任何SDK其他接口前，必须先调用该接口进行初始化
  cout << "CAMERA SDK INIT...";
  CameraSdkInit(0);
  cout << "DONE!" << endl;

  //枚举设备，并建立设备列表
  cout << "ENUM CAMERA DEVICES...";
	CameraEnumerateDevice(&tCameraEnumList,&iCameraCounts);
  if(iCameraCounts==0)
  {
	  cout << "ERROR: NO CAMERA CONNECTED." << endl;
		return;
	} 
	else
  {
    cout << "CONNECTED CAMERA NUMBERS: " << iCameraCounts << endl;
	}

	//相机初始化。初始化成功后，才能调用任何其他相机相关的操作接口
  cout << "CAMERA INIT...";
	iStatus = CameraInit(&tCameraEnumList, -1, -1, &hCamera);
	if(iStatus != CAMERA_STATUS_SUCCESS)
  {
    cout << "FAILED！" << endl;
		return;
	}
  else
  {
    cout << "SUCCESS！" << endl;
	}

	//获得相机的特性描述结构体。该结构体中包含了相机可设置的各种参数的范围信息。决定了相关函数的参数
	CameraGetCapability(hCamera, &tCapability);

  //初始化缓冲区
  g_pRgbBuffer = (BYTE *)malloc(tCapability.sResolutionRange.iHeightMax*tCapability.sResolutionRange.iWidthMax*3);

  //其他的相机参数设置
  CameraSetIspOutFormat(hCamera, CAMERA_MEDIA_TYPE_BGR8); //设置输出为彩色
  CameraSetUserClrTempGain(hCamera,168,136,100); ////手动白平衡得到的RGB增益
  CameraSetAeState(hCamera, false); //设置手动曝光
  CameraSetExposureTime(hCamera, 1000); //设置曝光时间
  // CameraSetGamma(hCamera, 100); ////设置Gamma值
  CameraSetContrast(hCamera,150); //设置对比度值
  
  cout << "CAMERA PARAMETERS SET DONE！" << endl;

  //让SDK进入工作模式，开始接收来自相机发送的图像数据
  CameraPlay(hCamera);
  cout << "CAMERA PLAYING！" << endl;
}

//
void MVCamera::UnInit()
{
  CameraSdkStatus iStatus;

  cout << "CAMERA UNINIT...";
  iStatus = CameraUnInit(hCamera);
  if(iStatus != CAMERA_STATUS_SUCCESS) {cout << "FAILED！" << endl;}
  else {cout << "SUCCESS！" << endl;}

  if (g_pRgbBuffer != NULL) {free(g_pRgbBuffer);}
}

//
void MVCamera::GetFrame(Mat &frame)
{
  tSdkFrameHead sFrameInfo;

  if(CameraGetImageBuffer(hCamera, &sFrameInfo, &pbyBuffer, 1000) == CAMERA_STATUS_SUCCESS)
	{
    CameraImageProcess(hCamera, pbyBuffer, g_pRgbBuffer, &sFrameInfo);
    Mat matImage(cv::Size(sFrameInfo.iWidth,sFrameInfo.iHeight), CV_8UC3, g_pRgbBuffer);
    CameraReleaseImageBuffer(hCamera, pbyBuffer);
    frame = matImage;
  }

}
