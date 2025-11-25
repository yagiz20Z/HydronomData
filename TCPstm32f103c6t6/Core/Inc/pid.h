/*
 * pid.h
 *
 *  Created on: Aug 23, 2025
 *      Author: Yagiz
 */

#ifndef INC_PID_H_
#define INC_PID_H_

#include <stdint.h>
#include <math.h>

#define SoH_ERROR_THRESHOLD 1.0f               // Integral birikiminin önüne geçmek için 
#define SoH_INTEGRAL_MAX_WINDUP_THRESHOLD 20       // Integral için dogunluk max ve min değeri
#define SoH_INTEGRAL_MIN_WINDUP_THRESHOLD -20
#define SoH_SRV_SaturationMax  20

#define MAX_PID 30                          // burayı da ayarla
#define MIN_PID -30                         // Bureayı ayarla

extern uint8_t Motor_Flag_Status;

typedef struct PIDParameters_t{         // kafadan rastgele kp,kd ve ki değerleri yazdım
    float kp;
    float kd;
    float ki;
    float integralBirikimi;
    float prev_error;
    float SRV_RVS;
    float Servo_Calib;
}PIDParameters_t;

PIDParameters_t pid;

void PID_Init(PIDParameters_t* pid, float kp, float ki, float kd);   

void PID_reset(PIDParameters_t* pid);    // Hata birikiminin önüne geçeriz

float PID_Currently(PIDParameters_t* pid, float angle, float limit ,uint32_t Dt, uint8_t MotorFlag);




#endif /* INC_PID_H_ */
