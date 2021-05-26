#include "AngleSolver.h"
#include "cmath"

using namespace cv;
using namespace std;

#define SMALL_ARMOR 2
#define BIG_ARMOR 3
const float GRAVITY = 9.78;

AngleSolverParam::AngleSolverParam()
{
    //装甲板世界坐标,把装甲板的中心对准定义的图像中心
    POINT_3D_OF_ARMOR_BIG = {
        cv::Point3f(-117.5, -63.5, 0), //tl
        cv::Point3f(117.5, -63.5, 0),	//tr
        cv::Point3f(117.5, 63.5, 0),	//br
        cv::Point3f(-117.5, 63.5, 0)	//bl
    };
    
    POINT_3D_OF_ARMOR_SMALL = {
        cv::Point3f(-70.0, -62.5, 0),	//tl
        cv::Point3f(70.0, -62.5, 0),	//tr
        cv::Point3f(70.0, 62.5, 0),    //br
        cv::Point3f(-70.0, 62.5, 0)    //bl
    };
}

void AngleSolverParam::read_XMLFile(void)
{
    FileStorage fsRead("/home/dji/dut0bug/DUT0BUG_RM_CV_2021_ThyssenWen_V0.2/camera_param/camera.xml", FileStorage::READ);

    if(!fsRead.isOpened())
    {
        cout << "failed to open xml" << endl;
        return;
    }

    fsRead["Y_DISTANCE_BETWEEN_GUN_AND_CAM"] >> Y_DISTANCE_BETWEEN_GUN_AND_CAM;
    fsRead["Z_DISTANCE_BETWEEN_MUZZLE_AND_CAM"] >> Z_DISTANCE_BETWEEN_MUZZLE_AND_CAM;
    fsRead["Camera_Matrix"] >> CameraIntrinsicMatrix;
    fsRead["Distortion_Coefficients"] >> DistortionCoefficient;
    return;
}

AngleSolver::AngleSolver(const AngleSolverParam& angleSolverParam)
{
    _params = angleSolverParam;
}

void AngleSolver::init(const AngleSolverParam& angleSolverParam)
{
    _params = angleSolverParam;
}

void AngleSolver::onePointSolution(const vector<Point2f> centerPoint)
{
    double fx = _params.CameraIntrinsicMatrix.at<double>(0,0);
    double fy = _params.CameraIntrinsicMatrix.at<double>(1,1);
    double cx = _params.CameraIntrinsicMatrix.at<double>(0,2);
    double cy = _params.CameraIntrinsicMatrix.at<double>(1,2);

    vector<Point2f> dstPoint;
    //单点矫正
    undistortPoints(centerPoint,dstPoint,_params.CameraIntrinsicMatrix,
                    _params.DistortionCoefficient,noArray(),_params.CameraIntrinsicMatrix);
    Point2f pnt = dstPoint.front();//返回dstPoint中的第一个元素
    //去畸变后的比值，根据像素坐标系与世界坐标系的关系得出,pnt的坐标就是在整幅图像中的坐标
    double rxNew=(pnt.x-cx)/fx;
    double ryNew=(pnt.y-cy)/fy;

    yawErr = atan(rxNew)/CV_PI*180;
    pitchErr = atan(ryNew)/CV_PI*180;
}

std::vector<float> AngleSolver::p4pSolution(const std::vector<cv::Point2f> objectPoints,int objectType)
{
    float yawErr_current;
    float pitchErr_current;
    if(objectType == 3)
        solvePnP(_params.POINT_3D_OF_ARMOR_BIG,objectPoints,_params.CameraIntrinsicMatrix,
                 _params.DistortionCoefficient,rVec,tVec,false, SOLVEPNP_ITERATIVE);
    else
        solvePnP(_params.POINT_3D_OF_ARMOR_SMALL,objectPoints,_params.CameraIntrinsicMatrix,
                 _params.DistortionCoefficient,rVec,tVec,false, SOLVEPNP_ITERATIVE);
    //cout<< "tVec:" << tVec << endl;
    tVec.at<float>(1, 0) -= _params.Y_DISTANCE_BETWEEN_GUN_AND_CAM;
    tVec.at<float>(2, 0) -= _params.Z_DISTANCE_BETWEEN_MUZZLE_AND_CAM;

    yawErr_current = atan(tVec.at<float>(0, 0)/tVec.at<float>(2, 0))/CV_PI*180;
    pitchErr_current = atan(tVec.at<float>(1, 0)/tVec.at<float>(2, 0))/CV_PI*180;
    //计算三维空间下的欧氏距离
    _euclideanDistance = sqrt(tVec.at<float>(0, 0)*tVec.at<float>(0, 0) + tVec.at<float>(1, 0)*
                              tVec.at<float>(1, 0) + tVec.at<float>(2, 0)* tVec.at<float>(2, 0));
    vector<float> result;

    result.resize(3); //指定容器的大小为3
    if(yawErr != 0){
        result[0] = yawErr_current + 20*(yawErr_current - yawErr);
        result[1] = pitchErr_current + 20*(pitchErr_current - pitchErr);
        yawErr = yawErr_current;
        pitchErr = pitchErr_current;
    }
    else
    {
        result[0] = yawErr_current;
        result[1] = pitchErr_current;
        yawErr = yawErr_current;
        pitchErr = pitchErr_current;
    }
    result[2] =_euclideanDistance;
    return result;
}




//air friction is considered
float BulletModel(float x, float v, float angle) { //x:m,v:m/s,angle:rad
    float t, y;
    float init_k_;
    t = (float)((exp(init_k_ * x) - 1) / (init_k_ * v * cos(angle)));
    y = (float)(v * sin(angle) * t - GRAVITY * t * t / 2);
    return y;
}

//x:distance , y: height
float GetPitch(float x, float y, float v) {
    float y_temp, y_actual, dy;
    float a;
    y_temp = y;
    // by iteration
    for (int i = 0; i < 20; i++) {
        a = (float) atan2(y_temp, x);
        y_actual = BulletModel(x, v, a);
        dy = y - y_actual;
        y_temp = y_temp + dy;
        if (fabsf(dy) < 0.001) {
        break;
        }
        //printf("iteration num %d: angle %f,temp target y:%f,err of y:%f\n",i+1,a*180/3.1415926535,yTemp,dy);
    }
    return a;

}

void Transform(vector<double> result, float &pitch, float v, float angle) {
    pitch =
        -GetPitch(result[2] / 100, -BulletModel(result[2], v, angle) / 100, v) + result[1];

}

