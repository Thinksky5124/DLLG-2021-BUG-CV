#include "ArmorDetector.h"
#include "opencv2/img_hash/phash.hpp"

std::vector<cv::Point2f> ARMOR;
int ARMOR_type = 2;
//
ArmorDetector::ArmorDetector()
{
    // enemy_color = ENEMY_BLUE;
    // enemy_color = ENEMY_RED;
    ArmorDetector::LoadTemplate();
    detect_update_flag = false;
}

/**
 * @brief load template from file
 * @param  fileroot         My Param doc
 * @param  TemplateCrossVectorMy Param doc
 * @return true 
 * @return false 
 */
bool ArmorDetector::LoadTemplate(){
    for (size_t i = 1; i <= TEMPLATE_NUMBER; i++)
    //for (int i = 1; i <= 9; i++)
    {
        cv::Mat ROIGray;
        cv::Mat ROIBinary;
        cv::Mat ROI_vec;
        cv::Mat ROICrossMatrix;
        cv::Mat ROIhashvalue;
        
        cv::Mat img = cv::imread("/home/dji/dut0bug/DUT0BUG_RM_CV_2021_ThyssenWen_V0.2/Template/"+std::to_string(i)+".jpg");
        //Reshape
        cv::resize(img,ROI_vec,cv::Size(MTACH_IMG_SIZE,MTACH_IMG_SIZE), cv::INTER_NEAREST);
        cvtColor(ROI_vec, ROIGray, cv::COLOR_BGR2GRAY);
        //binary
        threshold(ROIGray, ROIBinary, int(255*IMAGE_BINARY_THRESOLD), 255, cv::THRESH_BINARY); 
        //phash
        cv::img_hash::pHash(ROIBinary,ROIhashvalue);
        // Phash(ROIBinary,ROIhashvalue);
        this->TemplateCrossVector.emplace_back(ROIhashvalue);
    }
    return true;
}

//
bool ArmorDetector::findLightBars(const cv::Mat &src, LightBars &light_bars)
{
    //cv::Mat src_img = src.clone();
    cv::Mat color_channel;
    cv::Mat color_channel_binary;
    std::vector<cv::Mat> channels; // 通道拆分

    //根据目标颜色进行通道提取
    cv::split(src, channels);
    if(enemy_color == ENEMY_BLUE) {color_channel = channels[0];} //blue
    else if(enemy_color == ENEMY_RED) {color_channel = channels[2]-channels[0];} //red-blue

    //二值化对应通道
    cv::threshold(color_channel, color_channel_binary, 150, 255, cv::THRESH_BINARY);
    
    //开闭运算
    cv::Mat kernel = getStructuringElement(cv::MORPH_RECT, cv::Size(3, 3));
    cv::erode(color_channel_binary, color_channel_binary, kernel); cv::dilate(color_channel_binary, color_channel_binary, kernel);
    cv::dilate(color_channel_binary, color_channel_binary, kernel); cv::erode(color_channel_binary, color_channel_binary, kernel);
    
    //找轮廓
    vector<vector<cv::Point>> lightbar_contours;
    vector<cv::Vec4i> hierarchy_lightbar;
    cv::findContours(color_channel_binary, lightbar_contours, hierarchy_lightbar, cv::RETR_TREE, cv::CHAIN_APPROX_NONE);
    //cv::drawContours(src_img,lightbar_contours,-1,cv::Scalar(0,255,0),1);
    
    //找灯条
    for(int i = 0; i < lightbar_contours.size(); i++)
    {
        if (hierarchy_lightbar[i][2] == -1)
        {
            cv::RotatedRect rect = cv::minAreaRect(lightbar_contours[i]);

            //计算轮廓参数
            float lw_rate, lw_angle;
            if(rect.size.height > rect.size.width) //left rotate
            {
                lw_rate = rect.size.height/rect.size.width;
                lw_angle = rect.angle;
            } 
            else //right rotate
            {
                lw_rate = rect.size.width/rect.size.height;
                lw_angle = rect.angle-90;
            }
            //cout << i << "-lw_rate:" << lw_rate << endl;
            //cout << i << "-lw_angle:" << lw_angle <<  endl;
            //cout << i << "-rect_area:" << rect.size.area() <<  endl;

            //判断轮廓是否为一个灯条
            if((3.0<lw_rate)&&(lw_rate<20.0)&&(abs(lw_angle)<50.0)&&(rect.size.area()>20.0))
            {
                light_bars.emplace_back(rect, lw_angle);
            }
        }
    }
    
    //
    //test = color_channel; //color_channel color_channel_binary src_img
    return (light_bars.size()>=2);
}

//
bool ArmorDetector::matchArmorBoxes(const LightBars &light_bars, ArmorBoxes &armor_boxes, cv::Mat &img)
{
    armor_boxes.clear();

    //匹配装甲板
    for(int i=0; i<light_bars.size()-1; i++)
    {
        for (int j=i+1; j<light_bars.size(); j++)
        {
            //计算灯条组参数
            float length_rate, height_distance, angle_distance, center_distancelength_rate; 
            cv::Point2f centers = light_bars.at(i).rect.center-light_bars.at(j).rect.center; //中心向量
            float center_distance = sqrt(centers.ddot(centers)); //中心距

            length_rate = light_bars.at(i).length/light_bars.at(j).length; //灯条长度比
            height_distance = abs(centers.y); //灯条高度差
            angle_distance = abs(light_bars.at(i).angle-light_bars.at(j).angle); //灯条角度差(平行度)
            center_distancelength_rate = center_distance/((light_bars.at(i).length+light_bars.at(j).length)/2); //灯条中心距与长度比
            //cout << i << "-length_rate:" << length_rate << endl;
            //cout << i << "-height_distance:" << height_distance << endl;
            //cout << i << "-angle_distance:" << angle_distance << endl;
            //cout << i << "-center_distancelength_rate:" << center_distancelength_rate << endl;

            //判断灯条组是否为一个装甲板
            if((0.5<length_rate) && (length_rate<1.5) &&
               (height_distance<30) &&
               (angle_distance<10) &&
               (2.0<center_distancelength_rate) && (center_distancelength_rate<4.5))
            {
                cv::Rect2f rect_i = light_bars.at(i).rect.boundingRect();
                cv::Rect2f rect_j = light_bars.at(j).rect.boundingRect();
                float min_x, min_y, max_x, max_y;
                min_x = fmin(rect_i.x, rect_j.x) - 4;
                max_x = fmax(rect_i.x + rect_i.width, rect_j.x + rect_j.width) + 4;
                min_y = fmin(rect_i.y, rect_j.y) - 4;
                max_y = fmax(rect_i.y + rect_i.height, rect_j.y + rect_j.height) + 4;
                
                if (center_distancelength_rate < 3.5)
                    ARMOR_type = 2;
                else
                    ARMOR_type = 3;
                ARMOR = {
                cv::Point2f(min_x, min_y),  //tl
                cv::Point2f(max_x, min_y),	//tr
                cv::Point2f(max_x, max_y),	//br
                cv::Point2f(min_x, max_y)	//bl
                };
                LightBars pair_blobs = {light_bars.at(i), light_bars.at(j)};
                armor_boxes.emplace_back(cv::Rect2f(min_x,min_y,max_x-min_x,max_y-min_y), pair_blobs);
            }else
            {
                float rectcor_x1;
                float rectcor_y1;
                float rectcor_x2;
                float rectcor_y2;
                cv::Mat ROIGray;
                cv::Mat ROIBinary;
                cv::Mat ROIReszie;
                cv::Mat vec_ROI;
                cv::Mat ROIhashvalue;
                std::vector<int> probROI;
                //extract ROI
                rectcor_x1 = light_bars[i].rect.center.x;
                rectcor_y1 = std::max(light_bars[i].rect.center.y - light_bars[i].length*rect_cut_thresflod,float(0));
                rectcor_x2 = light_bars[j].rect.center.x;
                rectcor_y2 = std::min(light_bars[j].rect.center.y + light_bars[j].length*rect_cut_thresflod,float(480));
                vec_ROI = img(cv::Rect(int(std::min(rectcor_x1,rectcor_x2)),int(std::min(rectcor_y1,rectcor_y2)),int(std::abs(rectcor_x1 - rectcor_x2)),int(std::abs(rectcor_y1 - rectcor_y2))));
                if(vec_ROI.rows<=0){continue;}
                //Reshape
                cv::resize(vec_ROI,ROIReszie,cv::Size(MTACH_IMG_SIZE,MTACH_IMG_SIZE), cv::INTER_NEAREST);
                //RGB2GRAY
                cvtColor(ROIReszie, ROIGray, cv::COLOR_BGR2GRAY);
                //灰度归一化
                ROIGray.convertTo(ROIGray, CV_64F, 1.0 / 255, 0);
                //伽马变换
                pow(ROIGray, GAMMA, ROIGray);//dist 要与imageGamma有相同的数据类型
                ROIGray.convertTo(ROIGray, CV_8U, 255, 0);
                // cv::imshow("Gamma",ROIGray);
                // // binary
                cv::threshold(ROIGray,ROIGray,int(255*IMAGE_BINARY_THRESOLD),255,cv::THRESH_BINARY);
                // cv::imshow("Binary",ROIGray);
                // hash
                cv::img_hash::pHash(ROIGray,ROIhashvalue);
                
                for (size_t j = 0; j < TEMPLATE_NUMBER; j++)
                {
                    int HammingDistance = 0;
                    for (size_t n = 0; n < ROIhashvalue.size[1]; n++){
                            HammingDistance += __builtin_popcount(ROIhashvalue.at<uchar>(0,n) ^ this->TemplateCrossVector[j].at<uchar>(0,n));
                        }
                    
                    probROI.emplace_back(HammingDistance);
                }
                auto smallest = std::min_element(std::begin(probROI), std::end(probROI));
                //detect armor
                if(*smallest < TEMPLATE_MATCH_THRESOLD){
                    cv::Rect2f rect_i = light_bars.at(i).rect.boundingRect();
                    cv::Rect2f rect_j = light_bars.at(j).rect.boundingRect();
                    float min_x, min_y, max_x, max_y;
                    min_x = fmin(rect_i.x, rect_j.x) - 4;
                    max_x = fmax(rect_i.x + rect_i.width, rect_j.x + rect_j.width) + 4;
                    min_y = fmin(rect_i.y, rect_j.y) - 4;
                    max_y = fmax(rect_i.y + rect_i.height, rect_j.y + rect_j.height) + 4;
                    
                    ARMOR_type = std::distance(std::begin(probROI), smallest) + 1;
                    if (ARMOR_type != 1)
                        ARMOR_type = 2;
                    else
                        ARMOR_type = 3;
                    ARMOR = {
                        cv::Point2f(min_x, min_y),  //tl
                        cv::Point2f(max_x, min_y),	//tr
                        cv::Point2f(max_x, max_y),	//br
                        cv::Point2f(min_x, max_y)	//bl
                    };
                    LightBars pair_blobs = {light_bars.at(i), light_bars.at(j)};
                    armor_boxes.emplace_back(cv::Rect2f(min_x,min_y,max_x-min_x,max_y-min_y), pair_blobs);
                    probROI.clear();
                }
                else{
                    probROI.clear();
                    continue;
                }
            }
            
            
        }
    }

    return !armor_boxes.empty();
}
