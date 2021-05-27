/*
 * @Author: Thyssen Wen
 * @Date: 2021-05-26 20:28:19
 * @LastEditors: Thyssen Wen
 * @LastEditTime: 2021-05-26 20:58:01
 * @Description: logger heads
 * @FilePath: /DLLG-2021-BUG-CV/include/Logger/Logger.h
 */

/** API
 * 第一步，通过给定三个日志文件的路径，调用初始化函数initLogger进行日志文件的创建。
 * 第二步，在需要插入日志的地方调用LOG(TYPE) << "yourinfo";即可。your info表示你要输入到日志文件中的信息。
 * 以WARN日志为例，输出的信息大致如下：
 * Sun Jul  5 09:49:48 2015
 * function (getNextTask) line 75 no task to berun
 * Sun Jul  5 09:49:53 2015
 * function (getNextTask) line 75 no task to berun
**/

/**
版权声明：本文为CSDN博主「小白的进阶」的原创文章，遵循CC 4.0 BY-SA版权协议，转载请附上原文出处链接及本声明。
原文链接：https://blog.csdn.net/laobai1015/article/details/80004504
**/

#ifndef  __LOGGER_H__
#define  __LOGGER_H__
 
#include <iostream>
#include <iomanip>
#include <fstream>
#include <string>
#include <cstdlib>
#include <stdint.h>
/**
 * @brief logger file type
 */
typedef enum log_rank {
   INFO,
   WARNING,
   ERROR,
   FATAL
}log_rank_t;

/**
 * @brief init logger file
 * @param  info_log_filenameMy logger info file name
 * @param  warn_log_filenameMy logger waring file name
 * @param  error_log_filenameMy logger error file name
 */
void initLogger(const std::string&info_log_filename,
                const std::string&warn_log_filename,
                const std::string&error_log_filename);

/**
 * @brief logger system class
 */
class Logger {
   friend void initLogger(const std::string& info_log_filename,const std::string& warn_log_filename,const std::string& erro_log_filename);
   
public:
   Logger(log_rank_t log_rank) : m_log_rank(log_rank) {};
   
   ~Logger();   
   
   /**
    * @brief write src file function name before write logger info 
    * @param  log_rank         logger level
    * @param  line             logger line number
    * @param  function         logger happen function
    * @return std::ostream& 
    */
   static std::ostream& start(log_rank_t log_rank,
                               const int32_t line,
                               const std::string& function);
   
private:
   /**
    * @brief according level get logger stream
    * @param  log_rank         logger level
    * @return std::ostream& 
    */
   static std::ostream& getStream(log_rank_t log_rank);
   
   static std::ofstream m_info_log_file; 
   static std::ofstream m_warn_log_file;
   static std::ofstream m_error_log_file;
   log_rank_t m_log_rank;                             
};
 

/**
 * @brief according level to write logger stream
 */
#define LOG(log_rank)   \
Logger(log_rank).start(log_rank, __LINE__,__FUNCTION__)

/**
 * @brief macro for check with logger
 */
#define CHECK(a)                                            \
   if(!(a)) {                                              \
       LOG(ERROR) << " CHECK failed " << endl              \
                   << #a << "= " << (a) << endl;          \
       abort();                                            \
   }                                                      \
 
#define CHECK_NOTNULL(a)                                    \
   if( NULL == (a)) {                                      \
       LOG(ERROR) << " CHECK_NOTNULL failed "              \
                   << #a << "== NULL " << endl;           \
       abort();                                            \
    }
 
#define CHECK_NULL(a)                                       \
   if( NULL != (a)) {                                      \
       LOG(ERROR) << " CHECK_NULL failed " << endl         \
                   << #a << "!= NULL " << endl;           \
       abort();                                            \
    }
 
 
#define CHECK_EQ(a, b)                                      \
   if(!((a) == (b))) {                                     \
       LOG(ERROR) << " CHECK_EQ failed "  << endl          \
                   << #a << "= " << (a) << endl           \
                   << #b << "= " << (b) << endl;          \
       abort();                                            \
    }
 
#define CHECK_NE(a, b)                                      \
   if(!((a) != (b))) {                                     \
       LOG(ERROR) << " CHECK_NE failed " << endl           \
                   << #a << "= " << (a) << endl           \
                   << #b << "= " << (b) << endl;          \
       abort();                                            \
    }
 
#define CHECK_LT(a, b)                                      \
   if(!((a) < (b))) {                                      \
       LOG(ERROR) << " CHECK_LT failed "                   \
                   << #a << "= " << (a) << endl           \
                   << #b << "= " << (b) << endl;          \
       abort();                                            \
    }
 
#define CHECK_GT(a, b)                                      \
   if(!((a) > (b))) {                                      \
       LOG(ERROR) << " CHECK_GT failed "  << endl          \
                  << #a <<" = " << (a) << endl            \
                   << #b << "= " << (b) << endl;          \
       abort();                                            \
    }
 
#define CHECK_LE(a, b)                                      \
   if(!((a) <= (b))) {                                     \
       LOG(ERROR) << " CHECK_LE failed "  << endl          \
                   << #a << "= " << (a) << endl           \
                   << #b << "= " << (b) << endl;          \
       abort();                                            \
    }
 
#define CHECK_GE(a, b)                                      \
   if(!((a) >= (b))) {                                     \
       LOG(ERROR) << " CHECK_GE failed "  << endl          \
                   << #a << " = "<< (a) << endl            \
                   << #b << "= " << (b) << endl;          \
       abort();                                            \
    }
 
#define CHECK_DOUBLE_EQ(a, b)                               \
   do {                                                    \
       CHECK_LE((a), (b)+0.000000000000001L);              \
       CHECK_GE((a), (b)-0.000000000000001L);              \
    }while (0)
 
#endif