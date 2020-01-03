
#include "main.h"
//----------------------------------------
void port_ini(void)
{
	PORTD=0x00;
	DDRD=0xFF;
}
//----------------------------------------
int main(void)
{
	unsigned int adc_value;
	float n;
	port_ini(); //Инициализируем порты
	LCD_ini();  //Инициализируем дисплей
	ADC_Init(); //Инициализируем АЦП
	clearlcd(); //Очистим дисплей
	setpos(0,0);
	str_lcd("hello");
    while(1)
    {
		adc_value = ADC_convert(); //Вызовем преобразование
	/*	setpos(0,0);
		sendcharlcd(adc_value/1000+0x30);//Преобразуем число в код числа
		sendcharlcd((adc_value%1000)/100+0x30);//Преобразуем число в код числа
		sendcharlcd((adc_value%100)/10+0x30);//Преобразуем число в код числа
		sendcharlcd(adc_value%10+0x30);//Преобразуем число в код числа
		setpos(8,0);
		n= (float) adc_value / 400;
		sendcharlcd((unsigned char) n +0x30);//Преобразуем число в код числа
		sendcharlcd('.');//Преобразуем число в код числа
		sendcharlcd(((unsigned char) (n*10))%10 +0x30);//Преобразуем число в код числа
		sendcharlcd(((unsigned char) (n*100))%10 +0x30);//Преобразуем число в код числа*/
		_delay_ms(500);
    }
}