#ifndef Q_SERIAL_H
#define Q_SERIAL_H

#include <QSerialPort>
#include <QSerialPortInfo>
#include <QDebug>

#define STATUS_OK 0
#define STATUS_ERR -1
#define SERIAL_SOF 0xFF
#define SERIAL_EOF 0x01

struct send_pkg
{
    int16_t yaw_angle;
    int16_t pitch_angle;
    int16_t distance;
};

struct recieve_pkg
{
    uint8_t color;
    uint8_t mode;
};

class serial
{
public:
    serial();
    void serial_config();
    int serial_open();
    int serial_close();
    int serial_read();
    int serial_write(const char *a);

private:
    QSerialPort Q_Port;
    char *pack(send_pkg);
    recieve_pkg unpack(char* data);
    char buffer[8];
    int num_read = 0;
};

#endif // SERIAL_H
