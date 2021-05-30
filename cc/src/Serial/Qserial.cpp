#include "Qserial.h"

serial::serial()
{
    Q_Port.setPortName("/dev/ttyTHS2");

}

int serial::serial_open()
{
    if(Q_Port.open(QIODevice::ReadWrite))
    {
        Q_Port.setBaudRate(QSerialPort::Baud115200);
        Q_Port.setDataBits(QSerialPort::Data8);
        Q_Port.setStopBits(QSerialPort::OneStop);
        Q_Port.setParity(QSerialPort::NoParity);
        Q_Port.setFlowControl(QSerialPort::NoFlowControl);
        Q_Port.clearError();
        Q_Port.clear();
        qDebug() << "OPEN ttyTHS2 SUCCESS";
        return STATUS_OK;
    }
    else
    {
        qDebug() << "OPEN ttyTHS2 FAILED" << Q_Port.errorString();
        Q_Port.clearError();
        return STATUS_ERR;
    }
}

char *pack(send_pkg pkg)
{
    static char buff[8];
    buff[0] = SERIAL_SOF;
    buff[1] = pkg.yaw_angle >> 8;
    buff[2] = pkg.yaw_angle;
    buff[3] = pkg.pitch_angle >> 8;
    buff[4] = pkg.pitch_angle;
    buff[5] = pkg.distance >> 8;
    buff[6] = pkg.distance;
    buff[7] = SERIAL_EOF;
    return buff;
}

recieve_pkg serial::unpack(char* data)
{
    recieve_pkg pkg;
    pkg.mode = *(data + 1);
    pkg.color = *(data + 2);
    return pkg;
}

int serial::serial_read()
{
    memset(buffer, 0x00, sizeof(buffer));
    num_read = Q_Port.read(buffer, 8);
    if(num_read > 0)
    {
        qDebug() << "read data: " << buffer;
        return STATUS_OK;
    }
    else
    {
        qDebug() << "waiting for data...";
        return STATUS_ERR;
    }
}

int serial::serial_write(const char *a)
{
    Q_Port.write(a);
    return 0;
}


