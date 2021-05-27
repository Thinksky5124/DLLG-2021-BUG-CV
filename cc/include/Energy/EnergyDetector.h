#ifndef _ENERGYDETECTOR_H_
#define _ENERGYDETECTOR_H_
#define _USE_MATH_DEFINES
#include <iostream>
#include <cstdio>
#include <string>
#include <vector>
#include <cmath>
#include <opencv2/opencv.hpp>

using namespace std;
using namespace cv;

class Target {
public:
    Point2f target_pt;
    Point2f predict_pt;
    Point2f c_center;
    double c_radius;
    vector<double> result;
};

class EnergyDetector {
public:
    EnergyDetector(int index, uint8_t color);
    EnergyDetector(const string& filename, uint8_t color); // test with video input
    EnergyDetector();
    ~EnergyDetector();

    Mat pre_process(Mat img);
    bool rect_roi(Mat img, Mat &img_draw);
    int Judge(Mat img);
    Point2f estimate_circle();
    Mat image_origin, ROI;
    VideoCapture cap;
    vector<Point2f> center_vector;
    int finished_task = 0;
    bool detect_update_flag;
    uint8_t enemy_color;
    Target target_point;
    
private:
    bool stage = true; // true for stage 1, false for stage 2
    
    // bool aimbot_enable = true; // enable automatic aim
    int rotate_dir = 0; // 1 if clockwise, -1 if anticlockwise, 0 if unknown
    double get_distance(Point2f pt1, Point2f pt2);
    bool estimate_center(vector<Point2f> pts, Point2f &circle_center, float &R);
    bool estimate_angle(vector<Point2d> pts, double width, double height);
    double get_angle_diff(Point2f pt1, Point2f pt2);
    double estimate_rot(double angle, double fps);
    Point2f circle_center;
    float circle_radius;    
//    Mat im_templete;
};

#endif
