#ifndef UART_DRIVER
#define  UART_DRIVER

#include <stdint.h>
#include <avr/io.h>

void init_USART(uint32_t baud_rate);
void transmit_USART_data(char* data);
void transmit_USART_char(uint8_t data);

#endif /*UART_DRIVER*/
