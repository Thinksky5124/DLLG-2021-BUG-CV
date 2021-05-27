#ifndef _SERIAL_H_
#define _SERIAL_H_

#include  <unistd.h>
#include  <fcntl.h>
#include  <termios.h>

class Serial
{
public:
    Serial();
    ~Serial();
    bool setPara(int speed, int databits, int stopbits, int parity);
    int writeData(const char *data, int datalength);
    int readData(char *data, int datalength = 64);

private:
    int fd;
    int speed_arr[14] = {B115200, B19200, B9600, B4800, B2400, B1200, B300, B115200, B19200, B9600, B4800, B2400, B1200, B300};
    int name_arr[14] = {115200, 19200, 9600, 4800, 2400, 1200, 300, 115200, 19200, 9600, 4800, 2400, 1200, 300};
};


#endif
