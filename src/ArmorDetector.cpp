#include "ArmorDetector.h"
#include "Config.h"

Proposal::Proposal(/* args */)
{
}

Proposal::~Proposal()
{
}
/**
 * @brief 
 * @param  src              My Param doc
 * @param  armorDetector    My Param doc
 * @param  config           My Param doc
 * @return true 
 * @return false 
 */
bool Proposal::findProposal(const cv::Mat &src,const ArmorDetector &armorDetector,const Config &config){
    cv::Mat image_hsv;
    cv::Mat mask;
    cv::Mat kernel = getStructuringElement(cv::MORPH_RECT, cv::Size(3, 3));
    std::vector<std::vector<cv::Point>> contours;
	std::vector<cv::Point3f> circles;
    // std::vector<cv::Mat> channels; // 通道拆分
    
    cv::cvtColor(src,image_hsv,cv::COLOR_BGR2HSV);
    // cv::split(image_hsv,channels);
    if (armorDetector.enemy_color == ENEMY_BLUE)
    {
        cv::inRange(image_hsv,cv::Scalar(100,43,46),cv::Scalar(124,255,255),mask);
        cv::threshold(mask,mask,int(config.BINARY_THRESHOLD*255),255,cv::THRESH_BINARY);
        cv::erode(mask, mask, kernel); 

    }else if(armorDetector.enemy_color == ENEMY_RED){
        cv::inRange(image_hsv,cv::Scalar(156,43,46),cv::Scalar(180,255,255),mask);
        cv::threshold(mask,mask,int(config.BINARY_THRESHOLD*255),255,cv::THRESH_BINARY);
        cv::dilate(mask, mask, kernel);

    }else{
        std::cout << "No set enemy color!" << std::endl;
        return false;
    }

	findContours(mask, contours,cv::RETR_EXTERNAL , cv::CHAIN_APPROX_NONE);

    std::vector<std::vector<cv::Point>>::const_iterator itc= contours.begin();
    int cmin = 50;  // minimum contour length
	int cmax = 9999;
	while (itc!=contours.end()){  
        if (itc->size() < cmin || itc->size() > cmax)  
            itc= contours.erase(itc);  
        else   
            ++itc;  
    }  
	drawContours(src, contours,-1,CV_RGB(0,255,255),1);
    
    
}


Armor::Armor(/* args */)
{
}

Armor::~Armor()
{
}

ArmorDetector::ArmorDetector(/* args */)
{
}

ArmorDetector::~ArmorDetector()
{
}
