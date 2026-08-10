


#include "UART_driver.h"

#ifndef F_CPU
#define F_CPU 16000000UL
#endif

void init_USART(uint32_t baud_rate){
	uint16_t ubrr = (F_CPU / (16UL * baud_rate)) - 1;
	UBRR0H = (uint8_t)(ubrr >> 8);
	UBRR0L = (uint8_t) ubrr;
	
	UCSR0B |= (1 << TXEN0);
	
	UCSR0C |= (1 << UCSZ01) | (1 << UCSZ00);
}

void transmit_USART_data(char* data){
	while(*data != '\0'){
		transmit_USART_char(*data);
		data++;
	}
}

void transmit_USART_char(uint8_t data){

	while(!(UCSR0A & (1 << UDRE0))){}
		
	UDR0 = data;
}

