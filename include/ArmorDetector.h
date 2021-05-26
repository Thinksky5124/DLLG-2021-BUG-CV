#ifndef _ARMORDETECTOR_H_
#define _ARMORDETECTOR_H_

#include <opencv2/opencv.hpp>

const enum enemy_color_enum {ENEMY_BLUE,ENEMY_RED};

class Proposal
{
private:
    /* data */
public:
    Proposal(/* args */);
    ~Proposal();

    bool Proposal::findProposal(const cv::Mat &src,const ArmorDetector &armorDetector,const Config &config);
};


class Armor
{
private:
    
public:
    Armor(/* args */);
    ~Armor();

    std::vector<cv::Point2f> ARMOR;
    int ARMOR_type = 0;
};

class ArmorDetector
{
private:
    /* data */
public:
    ArmorDetector(/* args */);
    ~ArmorDetector();

    enemy_color_enum enemy_color = ENEMY_RED;
};


#endif
