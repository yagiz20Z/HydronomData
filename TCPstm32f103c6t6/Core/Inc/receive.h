/*
 * receive.h
 *
 *  Created on: Nov 5, 2025
 *      Author: yagiz
 */

#ifndef INC_RECEIVE_H_
#define INC_RECEIVE_H_

#include "main.h"
#include "usart.h"
#include "string.h"
#include <stdio.h>

void receiveData_Init(void);
void HAL_UART_RxCpltCallback(UART_HandleTypeDef *huart);









#endif