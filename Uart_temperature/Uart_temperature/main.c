/*
 * Uart_temperature.c
 *
 * Created: 2026. 08. 08. 11:06:17
 * Author : Yeah
 */ 

#define F_CPU 16000000UL

#include <avr/io.h>
#include <util/delay.h>
#include "ADC_driver.h"
#include "UART_driver.h"
#include <stdint.h>

int main(void)
{
	
	init_analog_2_digital(0);
	init_USART(9600);
	
    while (1) 
    {
		uint16_t readValue = readAnalogValue();
		float voltage = (readValue * 5.0) / 1024.0;
		float temperature = (voltage-0.5f) / 0.01f;
		char uart_buf[6];
		dtostrf(temperature, 4, 2, uart_buf);
		sprintf(uart_buf, "%s\r\n", uart_buf);
		transmit_USART_data(uart_buf);
		
		//Don't pay attention to this
		for (int i = 0;i<60;i++)
		{
			_delay_ms(1000);
		}
    }
}

