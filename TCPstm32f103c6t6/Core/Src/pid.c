/*
 * pid.c
 *
 *  Created on: Aug 23, 2025
 *      Author: Yagiz
 */

#include "pid.h"
#include <string.h> 

/**
 * @brief 
 * 
 * @param pid 
 * @param kp 
 * @param ki 
 * @param kd
 * 
 * @note nurada kp, ki ve kd değerlerin ataması yapılmaktadır
 *  
 */
void PID_Init(PIDParameters_t* pid, float kp, float ki, float kd){

    if (pid == NULL) {
        return; 
    }
    memset(pid, 0, sizeof(PIDParameters_t));

    pid->kp = kp;
    pid->ki = ki;
    pid->kd = kd;

}

/**
 * @brief 
 * 
 * @param pid 
 * 
 * @note İntegral birikiminin önüne geçer
 */
void PID_reset(PIDParameters_t* pid){        
    if (pid == NULL){
        return;
    }
    pid->integralBirikimi = 0.0f;
    pid->prev_error = 0.0f;

}   

/**
 * @brief 
 * 
 * @param pid 
 * @param limit 
 * @param anlik 
 * 
 * @note burada pid içerisinde p, i ve d'nin tüm işlemleri ayrı ayrı 
 * @note toplanıp pid değeri bulunmaktadır
 */
float PID_Currently(PIDParameters_t* pid, float angle, float limit, uint32_t Dt, uint8_t MotorFlag){
    
    if (pid == NULL){
        return 0.0f;
    }    

    float error;
    error = limit - angle;
    // proportional 
    float Proportional  = pid-> kp * error;

    // Integral
    if (MotorFlag == 0 || fabs(error)< SoH_ERROR_THRESHOLD){
        pid->integralBirikimi = 0;
    }

      pid -> integralBirikimi += error * Dt;
      pid-> integralBirikimi = saturation(SoH_INTEGRAL_MIN_WINDUP_THRESHOLD, SoH_INTEGRAL_MAX_WINDUP_THRESHOLD, pid->integralBirikimi);
      float integral;
      integral = pid->ki * pid->integralBirikimi;

    // Derivative
    float derivative_Coefficient = (error - pid->prev_error)/Dt;
    pid->prev_error = error;
    float derivative = pid->kd * derivative_Coefficient;

    float PID_output;
    PID_output = Proportional + integral + derivative;

    float deger = saturation(MIN_PID, MAX_PID, PID_output);

    return deger;

}
