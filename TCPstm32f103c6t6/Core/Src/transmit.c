/*
 * transmit.c
 *
 *  Created on: Nov 5, 2025
 *      Author: aliya
 */
/* AMACI: UART üzerinden gelen verileri tekrar pcde yazdırmaktır */

#include "transmit.h"

#define TX_BUFFER_SIZE 64 
extern UART_HandleTypeDef huart1;               // main.c'de tanımlı olmalı
uint8_t uart_tx_buffer[TX_BUFFER_SIZE];


void HAL_UART_TxCpltCallback(UART_HandleTypeDef *huart)
{
    if (huart == &huart1)
    {

        memset(uart_tx_buffer, 0, TX_BUFFER_SIZE);


        HAL_UART_Transmit_IT(&huart1, uart_tx_buffer, TX_BUFFER_SIZE);
    }
}


void transmitData(uint8_t *data, uint16_t len)
{
    if (data != NULL && len > 0)
    {
        CDC_Transmit_FS(data, len);
    }
}
