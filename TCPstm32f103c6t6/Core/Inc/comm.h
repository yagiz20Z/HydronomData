#ifndef INC_COMM_H_
#define INC_COMM_H_


#include "main.h"
#include "usart.h"
#include "string.h"
#include <stdio.h>

#include "usb_device.h" // usb ile stm'e veri atıp çekmeyi sağlamak için yapılır

// veri çekmek için olanlar
void receiveData_Init(void);
void HAL_UART_RxCpltCallback(UART_HandleTypeDef *huart);

// veri göndermek için olanlar
void HAL_UART_RxCpltCallback(UART_HandleTypeDef *huart);
void transmitData_Init(void);
void transmitData(uint8_t *data, uint16_t len);







#endif /* INC_COMM_H_ */

