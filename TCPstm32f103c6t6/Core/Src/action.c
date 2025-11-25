/*
 * action.c
 *
 *  Created on: Nov 5, 2025
 *      Author: aliya
 */

#include "action.h"
#include  "pid.h"

uint8_t Motor_Flag_Status = 1;
static PIDParameters_t PID_SoH;






void servopwm(long pulse_width){

    __HAL_TIM_SET_COMPARE(&SERVO1_TIM, SERVO1_CHA, pulse_width);        // buradaki değerleri ayarla


}



void hareket(float angle){


    float pid_value = PID_Currently(&PID_SoH, (float)angle, SoH_SRV_SaturationMax, 10, Motor_Flag_Status);

    float servo_signal = 1500 + pid_value * (SoH_SRV_SaturationMax / SoH_SRV_SaturationMax);   // buradaki 1500 değeri servonun orta pozisyonu

    if (servo_signal > 2000) servo_signal = 2000;          // servonun max ve min sınırlarını ayarla
    if (servo_signal < 1000) servo_signal = 1000;

    servopwm((long)servo_signal);

}
































