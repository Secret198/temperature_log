#ifndef ADC_DRIVER
#define ADC_DRIVER

#include <stdint.h>

void init_analog_2_digital(uint8_t channel);
uint16_t readAnalogValue();

#endif /*ADC_DRIVER*/
