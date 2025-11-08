/*
 * transmit.h
 *
 *  Created on: Nov 5, 2025
 *      Author: yagiz
 */

#ifndef INC_TRANSMIT_H_
#define INC_TRANSMIT_H_

#include "main.h"
#include "usart.h"
#include "string.h"
#include "usb_device.h"
#include <stdio.h>



void HAL_UART_RxCpltCallback(UART_HandleTypeDef *huart);
void transmitData_Init(void);
void transmitData(uint8_t *data, uint16_t len);





#endif /* INC_TRANSMIT_H_ */
