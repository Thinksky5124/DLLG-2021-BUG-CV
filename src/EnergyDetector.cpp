#include "EnergyDetector.h"

EnergyDetector::EnergyDetector(int index, uint8_t color)
{
    cap = VideoCapture(index);
    cap.set(CAP_PROP_FRAME_WIDTH, 640);
    cap.set(CAP_PROP_FRAME_HEIGHT, 480);
    enemy_color = color;
}

EnergyDetector::EnergyDetector(const string& filename, uint8_t color)
{
    cap = VideoCapture(filename);
    enemy_color = color;
//    im_templete = imread("templete.jpg", IMREAD_GRAYSCALE);
}

EnergyDetector::EnergyDetector()
{

}

EnergyDetector::~EnergyDetector()
{
    if(cap.isOpened())
    {
        cap.release();
    }
}

Mat EnergyDetector::pre_process(Mat img)
{
    vector<Mat> img_channels;
    split(img, img_channels);
    Mat img_single, img_close;
    if(!enemy_color)
    {
        img_single = img_channels[0];
    }
    else
    {
        img_single = img_channels[2]-img_channels[0];
    }
    threshold(img_single, img_single, 150, 255, THRESH_BINARY);
    
    Mat kernel_1 = getStructuringElement(MORPH_RECT, Size(5,5));
    Mat kernel_2 = getStructuringElement(MORPH_CROSS, Size(7,7));
    dilate(img_single, img_single, kernel_1);
    morphologyEx(img_single, img_single, MORPH_CLOSE, kernel_2);
//    cvtColor(img_single, img_single, COLOR_BGR2GRAY);
    return img_single;
}

bool EnergyDetector::rect_roi(Mat img, Mat& img_draw)
//vector<Mat> EnergyDetector::rect_roi(Mat img, Mat &img_draw)
{
    img_draw = img.clone();
    cvtColor(img_draw, img_draw, COLOR_GRAY2BGR);
    vector<vector<Point>> contours;
    vector<Vec4i> hierarcy;
    findContours(img, contours, hierarcy, RETR_CCOMP, CHAIN_APPROX_SIMPLE);
    vector<RotatedRect> box(contours.size()); //定义最小外接矩形集合
    vector<Point2d> rect_v;
    Point2f rect[4], rect_src[4], rect_dst[4];
    vector<Mat> roi;
    Point2f target;
    double width;
    double height;
    int roi_type = -1;
    int finished_block = 0;
    Point2f pts[4];
    if(contours.size() > 0)
    {
        for(int i = contours.size()-1; i>=0; i--)
        {
            box[i] = minAreaRect(Mat(contours[i]));
            box[i].points(rect);  //把最小外接矩形四个端点复制给rect数组
            //cout << rect[0] << " " << rect[1] << " " << rect[2] << " " << rect[3] << endl;
            for (int j = 0; j < 4; j++)
            {
                line(img_draw, rect[j], rect[(j+1)%4], Scalar(0,255,0), 2);
            }
            width = get_distance(rect[0], rect[1]);
            height = get_distance(rect[1], rect[2]);
            if(width>height)
            {
                rect_src[0]=rect[0];
                rect_src[1]=rect[1];
                rect_src[2]=rect[2];
                rect_src[3]=rect[3];
            }
            else
            {
                swap(width,height);
                rect_src[0]=rect[1];
                rect_src[1]=rect[2];
                rect_src[2]=rect[3];
                rect_src[3]=rect[0];
            }
            cout << "height: " << height << " width: " << width << endl;
            if(height*width > 5000 && height/width > 0.40 && height/width < 0.55)
            {
                getchar();
                //cout << "find......." << endl;
                rect_dst[0]=Point2f(0,0);
                rect_dst[1]=Point2f(width,0);
                rect_dst[2]=Point2f(width,height);
                rect_dst[3]=Point2f(0,height);
                // 应用透视变换，矫正成规则矩形
                Mat transform = getPerspectiveTransform(rect_src,rect_dst);
                Mat perspectMat;
                warpPerspective(img,perspectMat,transform,Size(width,height));
                transpose(perspectMat, perspectMat);
                // img_draw1 = perspectMat.clone();
                // cvtColor(img_draw1, img_draw1, COLOR_GRAY2BGR);
                roi_type = Judge(perspectMat);
                // cout << "type: " << roi_type << endl;
                if(roi_type == 0 && hierarcy[i][2] > 0)
                {
                    RotatedRect strike_area = minAreaRect(Mat(contours[hierarcy[i][2]]));
                    
                    target = strike_area.center;
                    strike_area.points(pts);
                    for(int i=0;i<4;i++)
                    {
                        rect_v.push_back(pts[i]);
                    };
                    estimate_angle(rect_v, 10, 20);
                    cout << "center: " << target << endl;
                    // circle(img_draw, target, 10, Scalar(0,0,255), -1);
                    if(center_vector.size()>1 && abs(target.x - center_vector[center_vector.size()-2].x)>50
                                              && abs(target.x - center_vector[center_vector.size()-1].x)>50)
                    {
                        finished_task++;
                        cout << "finished one" << endl;
                    }
                    if(center_vector.size() == 31)
                    {
                        cout << "detect rotate direction: ";
                        double angle = get_angle_diff(center_vector[29], center_vector[28]);
                        if(angle < 0)
                        {
                            rotate_dir = 1;
                            cout << "clockwise" << endl;
                        }
                        else if(angle > 0)
                        {
                            rotate_dir = -1;
                            cout << "anticlockwise" << endl;
                        }
                        else
                        {
                            rotate_dir = 0;
                            cout << "still" << endl;
                        }
                        // cout << "------------angle is :" << angle << "------------" << endl;                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  
                    }
                    
                    center_vector.push_back(target);

                }
                else if(roi_type == 1 && hierarcy[i][2] > 0)
                {
                    finished_block++;
                }
            }
        }
    }
    if(finished_block == 5)
    {
        cout << "finished all" << endl;
        return false;
    }
    else if(estimate_center(center_vector, circle_center, circle_radius))
    {
        // circle(img_draw, circle_center, circle_radius, Scalar(255,0,255),5);
        // double angle_now = get_angle_diff(center_vector[center_vector.size()-1], center_vector[center_vector.size()-2]);
        // cout << "angle now " << angle_now << endl;
        // double test = estimate_rot(angle_now, 60);
        // cout << "estimate rot: " << test << endl;
        target_point.target_pt = target;
        target_point.c_center = circle_center;
        target_point.c_radius = circle_radius;
        double angle_offset = 30;
        Mat rot_mat = getRotationMatrix2D(circle_center, rotate_dir*angle_offset, 1);
        float sin_rot = rot_mat.at<double>(0,1);
        float cos_rot = rot_mat.at<double>(0,0);
        float x_offset = target.x-circle_center.x;
        float y_offset = target.y-circle_center.y;
        Point2f target_offset = Point2f(circle_center.x+cos_rot*x_offset-sin_rot*y_offset,
                                        circle_center.y+sin_rot*x_offset+cos_rot*y_offset);
        target_point.predict_pt = target_offset;
        estimate_angle(rect_v, 10, 10);
        // circle(img_draw, target_offset, 10, Scalar(255,255,0), -1);
        return true;
    }
    else
        return false;
    
}

int EnergyDetector::Judge(Mat img)
{
    int filter = int(img.rows*0.5);
    int count = 0;
    vector<int> pass_band, stop_band;
    uchar* data = img.ptr<uchar>(filter);
    for(int i = 0; i < img.cols; i++)
    {
        // if((i == 0 && data[i] == 255) || (i >0 && data[i] == 255 && data[i-1] != 255))
        // {
        //     count++;
        // }
        // cout << "data[i]: " << int(data[i]) << endl;
        if((i == 0 && data[i] != 0) || (i > 0 && data[i] != 0 && data[i-1] == 0)) //posedge
        {
            pass_band.push_back(i);
            // cout << "detected posedge" << endl;
        }
        else if(i > 0 && data[i] == 0 && data[i-1] != 0) //negedge
        {
            stop_band.push_back(i);
            // cout << "detected negedge" << endl;
        }
    }
    for(int j = 0; j < stop_band.size(); j++)
    {
        int dx = stop_band[j]-pass_band[j];
        // cout << "dx: " << dx << endl;
        if(dx > 5)
        {
            count++;
        }
    }
    // cout << "count " << count << endl;
    if(count == 1)
        return 0;
    else if(count == 3)
        return 1;     
    else
        return -1;
}

bool EnergyDetector::estimate_center(vector<Point2f> pts, Point2f &circle_center, float &R)
{
    // https://blog.csdn.net/liyuanbhu/article/details/50889951
    if(pts.size()<30)
    {
        return false;
    }
    else
    {
        circle_center.x = 0;
        circle_center.y = 0;
        R = 0;
        
        double sum_x = 0.0f, sum_y = 0.0f;
        double sum_x2 = 0.0f, sum_y2 = 0.0f;
        double sum_x3 = 0.0f, sum_y3 = 0.0f;
        double sum_xy = 0.0f, sum_x1y2 = 0.0f, sum_x2y1 = 0.0f;

        int N = pts.size();
        for (int i = 0; i < N; i++)
        {
            double x = pts[i].x;
            double y = pts[i].y;
            double x2 = x * x;
            double y2 = y * y;
            sum_x += x;
            sum_y += y;
            sum_x2 += x2;
            sum_y2 += y2;
            sum_x3 += x2 * x;
            sum_y3 += y2 * y;
            sum_xy += x * y;
            sum_x1y2 += x * y2;
            sum_x2y1 += x2 * y;
        }

        double C, D, E, G, H;
        double a, b, c;

        C = N * sum_x2 - sum_x * sum_x;
        D = N * sum_xy - sum_x * sum_y;
        E = N * sum_x3 + N * sum_x1y2 - (sum_x2 + sum_y2) * sum_x;
        G = N * sum_y2 - sum_y * sum_y;
        H = N * sum_x2y1 + N * sum_y3 - (sum_x2 + sum_y2) * sum_y;
        a = (H * D - E * G) / (C * G - D * D);
        b = (H * C - E * D) / (D * D - G * C);
        c = -(a * sum_x + b * sum_y + sum_x2 + sum_y2) / N;

        circle_center.x = a / (-2);
        circle_center.y = b / (-2);
        R = sqrt(a * a + b * b - 4 * c) / 2;
        
        return true;
    }
}

double EnergyDetector::get_angle_diff(Point2f pt1, Point2f pt2)
{
    double x = circle_center.x;
    double y = circle_center.y;
    double a = sqrt(pow((pt1.x-pt2.x),2) + pow((pt1.y-pt2.y),2));
    double b = sqrt(pow((x-pt2.x),2) + pow((y-pt2.y),2));
    double c = sqrt(pow((pt1.x-x),2) + pow((pt1.y-y),2));
    // 余弦定理
    double cosA = (pow(b,2) + pow(c,2) - pow(a,2)) / (2*b*c);
    // cout << "x: " << x << " y: "<<  y <<" a: " << a << " b: " << b << " c: " << c << endl;
    double arcA = acos(cosA);
    double degree = arcA*180 / M_PI;

    // 第1、2象限
    if(pt1.y < y && pt2.y < y)
    {
        if(pt1.x < x && pt2.x > x)
        {
            // 由2象限向1象限滑动
            return degree;
        }
        else
        {
            // 由1象限向2象限滑动
            return -degree;
        }
    }
    // 第3、4象限
    if (pt1.y > y && pt2.y > y)
    {
        // 由3象限向4象限滑动
        if (pt1.x < x && pt2.x > x)
        {
            return -degree;
        }
        // 由4象限向3象限滑动
        else if (pt1.x > x && pt2.x < x)
        {
            return degree;
        }

    }
    // 第2、3象限
    if (pt1.x < x && pt2.x < x)
    {
        // 由2象限向3象限滑动
        if (pt1.y < y && pt2.y > y)
        {
            return -degree;
        }
        // 由3象限向2象限滑动
        else if (pt1.y > y && pt2.y < y)
        {
            return degree;
        }
    }
    // 第1、4象限
    if (pt1.x > x && pt2.x > x)
    {
        // 由4向1滑动
        if (pt1.y > y && pt2.y < y)
        {
            return -degree;
        }
        // 由1向4滑动
        else if (pt1.y < y && pt2.y > y)
        {
            return degree;
        }
    }

    // 在特定的象限内
    float tanB = (pt1.y - y) / (pt1.x - x);
    float tanC = (pt2.y - y) / (pt2.x - x);
    if ((pt1.x > x && pt1.y > y && pt2.x > x && pt2.y > y && tanB > tanC)// 第一象限
            || (pt1.x > x && pt1.y < y && pt2.x > x && pt2.y < y && tanB > tanC)// 第四象限
            || (pt1.x < x && pt1.y < y && pt2.x < x && pt2.y < y && tanB > tanC)// 第三象限
            || (pt1.x < x && pt1.y > y && pt2.x < x && pt2.y > y && tanB > tanC))// 第二象限
        return -degree;
    return degree;

}

double EnergyDetector::estimate_rot(double angle, double fps)
{
    double w0 = abs(M_PI*angle*fps/180);
    cout << "w0 " << w0 << endl;
    double t = asin((w0-1.305)/0.785)/1.884;
    double tf = 0.4;
    double angle_offset_w = -2.96*cos(1.884*(t+0.5*tf))*cos(1.884*0.5*tf)+1.305*tf;
    double angle_offset = angle_offset_w*180/M_PI;
    return angle_offset;
}


double EnergyDetector::get_distance(Point2f pt1, Point2f pt2)
{
    double d1 = pt1.x-pt2.x;
    double d2 = pt1.y-pt2.y;
    double d = sqrt(pow(d1,2) + pow(d2,2));
    //cout << "d1 "<< d1  << " d2 " << d2 << " d " << d << endl;
    return d;
}

bool EnergyDetector::estimate_angle(vector<Point2d> pts, double width, double height)
{

    FileStorage fsRead("/home/dji/dut0bug/DUT0BUG_RM_CV_2021_ThyssenWen_V0.1/camera_param/camera.xml", FileStorage::READ);

    if(!fsRead.isOpened())
    {
        cout << "failed to open xml" << endl;
        return -1;
    }
    float Y_DISTANCE_BETWEEN_GUN_AND_CAM, Z_DISTANCE_BETWEEN_MUZZLE_AND_CAM;
    Mat CameraIntrinsicMatrix, DistortionCoefficient,rot, rotM,tvcs;
    fsRead["Y_DISTANCE_BETWEEN_GUN_AND_CAM"] >> Y_DISTANCE_BETWEEN_GUN_AND_CAM;
    fsRead["Z_DISTANCE_BETWEEN_MUZZLE_AND_CAM"] >> Z_DISTANCE_BETWEEN_MUZZLE_AND_CAM;
    fsRead["Camera_Matrix"] >> CameraIntrinsicMatrix;
    fsRead["Distortion_Coefficients"] >> DistortionCoefficient;

    vector<Point3d> corner3d;
    // vector<Point2d> corner2d;
    // corner3d.push_back(Point3d(0,0,0));

    corner3d.push_back(Point3d(-width/2, -height/2, 0));
    corner3d.push_back(Point3d(-width/2,  height/2, 0));
    corner3d.push_back(Point3d( width/2,  height/2, 0));
    corner3d.push_back(Point3d( width/2, -height/2, 0));
    if(pts.size() > 0)
    {
        solvePnP(corner3d, pts, CameraIntrinsicMatrix, DistortionCoefficient, rot, tvcs);

    }
    // corner2d.push_back(target_point.predict_pt);
    target_point.result[0] = atan(tvcs.at<double>(0,0)/tvcs.at<double>(2,0));
    target_point.result[1] = atan(tvcs.at<double>(1,0)/tvcs.at<double>(2,0));
    return 0;
    
}

