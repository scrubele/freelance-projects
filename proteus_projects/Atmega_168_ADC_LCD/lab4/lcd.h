#ifndef LCD_H_
#define LCD_H_

#include "main.h"

void LCD_init(void);
void set_position(unsigned char x, unsigned y);
void str_lcd (char str1[]);
void LCD_clear(void);
void send_char_lcd(unsigned char c);

#define e1    PORTD|=1<<3//0b00001000
#define e0    PORTD&=0b11110111 
#define rs1    PORTD|=1<<2//0b00000100 
#define rs0    PORTD&=0b11111011 

#endif