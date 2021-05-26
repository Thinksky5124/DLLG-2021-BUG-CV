#include "MVCamera.h"
#include "ArmorDetector.h"
#include "AngleSolver.h"
#include "serial.h"
#include "EnergyDetector.h"
#include "Config.h"

#include <iostream>
#include <thread>
#include <mutex>
#include <unistd.h>
#include <opencv2/opencv.hpp>

#define DEBUG_MODEL
// #define RELEASE_MODEL

#define FROM_VIDEO
// #define FROM_CAMERA

int main(void){
    Config config = Config("./param_xml/camera_param.xml");
    cv::Mat frame;
    
    //Read data
    #ifdef FROM_VIDEO
    VideoCapture capture;
    capture.open("./a1.avi");
    if(!capture.isOpened())
    {
        printf("can not open ...\n");
        return -1;
    }
    namedWindow("output", cv::WINDOW_AUTOSIZE);

    capture >> frame;
    #else



    #endif
    //frame process
    #ifdef DEBUG_MODEL


    #else

    #endif
    //data release
    #ifdef FROM_VIDEO
    capture.release();
    #else



    #endif
}