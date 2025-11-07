/*
 * transmit.c
 *
 *  Created on: Nov 5, 2025
 *      Author: aliya
 */


#include "transmit.h"

#define RX_BUFFER_SIZE 64

uint8_t uart_rx_buffer[RX_BUFFER_SIZE];
extern UART_HandleTypeDef huart1;  // main.c'de tanımlı olmalı

void transmitData_Init(void)
{
    HAL_UART_Receive_IT(&huart1, uart_rx_buffer, RX_BUFFER_SIZE);
}

void HAL_UART_RxCpltCallback(UART_HandleTypeDef *huart)
{
    if (huart == &huart1)
    {
        CDC_Transmit_FS(uart_rx_buffer, RX_BUFFER_SIZE);
        
        memset(uart_rx_buffer, 0, RX_BUFFER_SIZE);
        
        HAL_UART_Receive_IT(&huart1, uart_rx_buffer, RX_BUFFER_SIZE);
    }
}

void transmitData(uint8_t *data, uint16_t len)
{
    if (data != NULL && len > 0)
    {
        CDC_Transmit_FS(data, len);
    }
}
