/*
 * transmit.c
 *
 *  Created on: Nov 5, 2025
 *      Author: aliya
 * 
 * @brief Bu kütüphane bize java'dan aldığımız verileri stm'e atmamızı sağlar
 * 
 */


#include "receive.h"

#define RX_BUFFER_SIZE 64   // bana gelen verilerin byte'larına göre





extern UART_HandleTypeDef huart1;  // main.c'de tanımlı olmalı
uint8_t uart_rx_buffer[RX_BUFFER_SIZE];


void receiveData_Init(void)
{
    HAL_UART_Receive_IT(&huart1, uart_rx_buffer, RX_BUFFER_SIZE);
}



void HAL_UART_RxCpltCallback(UART_HandleTypeDef *huart)
{
    if (huart == &huart1)
    {


        memset(uart_rx_buffer, 0, RX_BUFFER_SIZE);


        HAL_UART_Receive_IT(&huart1, uart_rx_buffer, RX_BUFFER_SIZE);


        
    }
}



