#include "serial.h"
#include <iostream>

using namespace std;

//
Serial::Serial()
{
    string port_str = "/dev/ttyS0";

    char *dev=(char *)port_str.data();
    fd = open(dev, O_RDWR | O_NOCTTY | O_NONBLOCK); // no block
    if (-1 == fd)
    {
        cout << "Can't Open Serial Port!" << endl;
    }
    else
    {
        cout << "open success at dev ttyTHS2!" << endl;
    }

}

//
Serial::~Serial()
{
    close(fd);
}

//
bool Serial::setPara(int speed, int databits, int stopbits, int parity)
{
    int status;
    struct termios Opt;
    
    tcgetattr(fd, &Opt);
    for(int i= 0; i<sizeof(speed_arr)/sizeof(int);  i++)
    {
        if(speed == name_arr[i])
        {
            tcflush(fd, TCIOFLUSH);
            cfsetispeed(&Opt, speed_arr[i]);
            cfsetospeed(&Opt, speed_arr[i]);
            Opt.c_iflag &= ~(ICRNL | INLCR);
            Opt.c_lflag &= ~(ICANON | ECHO | ECHOE | ISIG); //edited
            status = tcsetattr(fd, TCSANOW, &Opt);
            if(status != 0)
            {
                cout << "tcsetattr fd1" << endl;
                return false;
            }
            tcflush(fd,TCIOFLUSH);
        }
    }

    struct termios options;
    options.c_lflag  &= ~(ICANON | ECHO | ECHOE | ISIG);  //Input
    options.c_oflag  &= ~OPOST;   //Output
    
    if(tcgetattr(fd,&options) != 0)
    {
        cout << "SetupSerial 1" << endl;
        return false;
    }

    options.c_cflag &= ~CSIZE;
    switch(databits) //设置数据位数
    {
        case 7:
            options.c_cflag |= CS7;
            break;
        case 8:
            options.c_cflag |= CS8;
            break;
        default:
            cout << "Unsupported data size" << endl;
            return false;
    }

    switch(parity)
    {
        case 'n':
        case 'N':
            options.c_cflag &= ~PARENB; //Clear parity enable
            options.c_iflag &= ~INPCK;  //Enable parity checking
            break;
        case 'o':
        case 'O':
            options.c_cflag |= (PARODD | PARENB); //设置为奇效验
            options.c_iflag |= INPCK;             //Disnable parity checking
            break;
        case 'e':
        case 'E':
            options.c_cflag |= PARENB;  //Enable parity
            options.c_cflag &= ~PARODD; //转换为偶效验
            options.c_iflag |= INPCK;   //Disnable parity checking
            break;
        case 'S':
        case 's':  //as no parity
            options.c_cflag &= ~PARENB;
            options.c_cflag &= ~CSTOPB;break;
        default:
            cout << "Unsupported parity" << endl;
            return false;
    }

    switch(stopbits) //设置停止位
    {
        case 1:
            options.c_cflag &= ~CSTOPB;
            break;
        case 2:
            options.c_cflag |= CSTOPB;
            break;
        default:
            cout << "Unsupported stop bits" << endl;
            return false;
    }

    //Set input parity option
    if(parity != 'n')
    {
        options.c_iflag |= INPCK;
    }
    tcflush(fd,TCIFLUSH);
    options.c_cc[VTIME] = 150; //设置超时15 seconds
    options.c_cc[VMIN] = 0; //Update the options and do it NO

    if(tcsetattr(fd,TCSANOW,&options) != 0)
    {
        cout << "SetupSerial 3" << endl;
        return false;
    }
    return true;
}

//
int Serial::writeData(const char *data, int datalength)
{
    int nwrite;
    nwrite = write(fd, data, datalength);
    return nwrite;
}

//
int Serial::readData(char *data, int datalength)
{
    int nread;
    nread = read(fd, data, datalength-1);
    data[nread] = '\0';
    return nread;
}
