#include "lcd.h"


void send_half_byte(unsigned char c)
{
	c<<=4;
	e1; 
	_delay_us(50);
	PORTD&=0b00001111; 
	PORTD|=c;
	e0;
	_delay_us(50);
}

void send_byte(unsigned char c, unsigned char mode)
{
	if (mode==0) rs0;
	else         rs1;
	unsigned char hc=0;
	hc=c>>4;
	send_half_byte(hc); 
	send_half_byte(c);
}

void send_char_lcd(unsigned char c)
{
	send_byte(c,1);
}

void set_position(unsigned char x, unsigned y)
{
	char adress;
	adress=(0x40*y+x)|0b10000000;
	send_byte(adress, 0);
}

void LCD_init(void)
{
	_delay_ms(15); //Ждем 15 мс (стр 45)
	send_half_byte(0b00000011);
	_delay_ms(4);
	send_half_byte(0b00000011);
	_delay_us(100);
	send_half_byte(0b00000011);
	_delay_ms(1);
	send_half_byte(0b00000010);
	_delay_ms(1);
	send_byte(0b00101000, 0); //4 bit mode
	_delay_ms(1);
	send_byte(0b00001100, 0);
	_delay_ms(1);
	send_byte(0b00000110, 0); //left mode
	_delay_ms(1);
}

void LCD_clear(void)
{
	send_byte(0b00000001, 0);
	_delay_us(1500);
}

void str_lcd (char str1[])
{  
	wchar_t n;
	for(n=0;str1[n]!='\0';n++)
	send_char_lcd(str1[n]);
}
