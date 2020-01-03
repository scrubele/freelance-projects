
#include "main.h"
char adc_string[1000];

void port_init(void)
{
	PORTD=0x00;
	DDRD=0xFF;
}

int main(void)
{
	unsigned int adc_value;
	float n;
	port_init();
	LCD_init(); 
	ADC_Init ();
	LCD_clear();
	set_position(0,0);

    while(1)
    {
		adc_value = ADC_convert();       
		n = (adc_value * 5.0 / 1024.0);
		set_position(0,0);
		sprintf(adc_string, "%.2u", adc_value);
		str_lcd(adc_string);
    }
}