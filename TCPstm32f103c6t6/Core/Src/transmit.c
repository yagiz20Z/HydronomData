/*
 * transmit.c
 *
 *  Created on: Nov 5, 2025
 *      Author: aliya
 */


#include "transmit.h"

void transmitData(uint8_t *data, uint16_t len)
{
    if (data != NULL && len > 0)
    {
        CDC_Transmit_FS(data, len);
    }
}
