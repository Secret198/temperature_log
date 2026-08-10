#include <avr/io.h>
#include "ADC_driver.h"


void init_analog_2_digital(uint8_t channel){
	ADMUX |= (1 << REFS0);		//Set reference voltage to 5 volt i think
	ADMUX &= ~((1 << MUX3) |(1 << MUX2) |(1 << MUX1) | (1 << MUX0));	//Clear channels
	ADMUX |= channel & ((1 << MUX3) |(1 << MUX2) |(1 << MUX1) | (1 << MUX0));	//Select channels
	ADCSRA |= (1 << ADEN) | (1 <<ADPS0)| (1 <<ADPS1)| (1 <<ADPS2);
	
}

uint16_t readAnalogValue(){
	ADCSRA |= (1 << ADSC);
	while(ADCSRA & (1 << ADSC)){}
	return ADC;
}

