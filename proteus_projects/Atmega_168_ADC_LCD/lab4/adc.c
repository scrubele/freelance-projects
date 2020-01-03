#include "adc.h"

void ADC_Init(void)
{
	ADCSRA |= (1<<ADEN) // Access using ADC
	|(1<<ADPS2)|(1<<ADPS1)|(1<<ADPS0)| (1 << ADATE);//Frequency Devider
	ADMUX |= (1<<REFS1)|(1<<REFS0); //Source, enable on the port ADC0
}

unsigned int ADC_convert (void)
{
	 unsigned int result = 0;
	 
	 ADMUX = (ADMUX & 0XF0) | (0X0F & 0);          // Enable conversion on selected ADC channel
	 _delay_us(400);
	 ADCSRA |= (1<<ADSC);                                // Start ADC Conversion
	 while((ADCSRA & (1<<ADIF)));                // Wait till conversion is complete
	 result = ADC;                                       // Read the ADC Result
	 ADCSRA |= (1 << ADIF);                              // Clear ADC Conversion Interrupt Flag
	 return result;
}