#ifndef _ARMORDETECTOR_H_
#define _ARMORDETECTOR_H_

#include <iostream>
#include <opencv2/opencv.hpp>

#define ENEMY_BLUE 0
#define ENEMY_RED  1

const int MTACH_IMG_SIZE = 32;
const float rect_cut_thresflod = 1.2;
const float IMAGE_BINARY_THRESOLD = 0.02;
const int TEMPLATE_MATCH_THRESOLD = 23;//the more small ,the mall accurate
const size_t TEMPLATE_NUMBER = 5;
const float HIGHT_DISTANCE_THRESHOLD = 0.5;
const double GAMMA = 0.05;


using namespace std;

/******************* 灯条类定义 ***********************/
class LightBar
{
public:
    cv::RotatedRect rect; //灯条位置
    float length; //灯条长度
    float angle; //灯条角度

    LightBar()=default;
    LightBar(cv::RotatedRect &r, float a):rect(r),angle(a){length = max(rect.size.height,rect.size.width);}
};

typedef vector<LightBar> LightBars;

/******************* 装甲板类定义　**********************/
class ArmorBox
{
public:
    cv::Rect2f rect; //装甲板位置
    LightBars light_bars; //装甲板灯条组
    cv::Point2f center; //装甲板中心

    ArmorBox()=default;
    ArmorBox(const cv::Rect2f &r, LightBars &bars):rect(r),light_bars(bars)
    {
        center.x = (light_bars[0].rect.center.x+light_bars[1].rect.center.x)/2;
        center.y = (light_bars[0].rect.center.y+light_bars[1].rect.center.y)/2;
    };
};

typedef vector<ArmorBox> ArmorBoxes;

/********************* 自瞄检测定义 **********************/
class ArmorDetector
{
private:
    std::vector<cv::Mat> TemplateCrossVector;
public:
    ArmorDetector();

    bool LoadTemplate();
    bool findLightBars(const cv::Mat &src, LightBars &light_bars);
    bool matchArmorBoxes(const LightBars &light_bars, ArmorBoxes &armor_boxes, cv::Mat &img);

    bool detect_update_flag;
    ArmorBox target_box;
    uint8_t enemy_color;
};


#endif
