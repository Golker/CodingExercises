"""
You receive 2 roman numbers and must sum them and return 
the result in the form of another roman number.

Constraints
1 ≤ Rom1 ≤ 4999
1 ≤ Rom2 ≤ 4999
1 ≤ Rom1 + Rom2 ≤ 4999
"""

import sys
import unittest

values = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100, "D": 500, "M": 1000}

def calculate_arabic(roman_number):
    """ 
        Transforms roman numbers into arabic and calculates the sum 
    
        roman_number: the roman number as a string
    """    
    rom_split = [char for char in roman_number]
    num = 0
    
    # little helper function to calculate the value of each letter, 
    # depending on its position
    def value_by_letter(i, num, letter, second_letter, third_letter):
        value = values.get(letter, 0)
        
        if i == len(rom_split) - 1:
            num += value
        elif i < len(rom_split) - 1:
            if rom_split[i + 1] in [second_letter, third_letter]:
                num -= value
            else:
                num += value
        
        return num
    
    for i, letter in enumerate(rom_split):
        if letter == "I":
            num = value_by_letter(i, num, letter, "V", "X")            
        elif letter == "V":
            num += 5  # some letters are just straightforward :)
        elif letter == "X":
            num = value_by_letter(i, num, letter, "L", "C")
        elif letter == "L":
            num += 50
        elif letter == "C":
            num = value_by_letter(i, num, letter, "D", "M")
        elif letter == "D":
            num += 500
        elif letter == "M":
            num += 1000
    
    return num

def calculate_roman(num):
    """ 
        Transforms arabic numbers into roman 
        
        num: the arabic number to be transformed
    """
    
    num_split = [char for char in str(num)]
    
    result_array = []
    
    # little helper function to calculate the corresponding letters for
    # each algarism in a number, depending on its position
    def letter_by_value(current, first_letter, second_letter, third_letter):
        if current in [0, 1, 2, 3]:
                result_array.append(current * first_letter)
        elif current == 4:
            result_array.append(first_letter + second_letter)
        elif current in [5, 6, 7, 8]:
            over_five = current - 5
            result_array.append(second_letter + (over_five * first_letter))
        elif current == 9:
            result_array.append(first_letter + third_letter)
    
    # reverses the arabic number to begin from the smallest power to the highest
    for i, n in enumerate(reversed(num_split)):
        current = int(n)
        if i == 0:            
            letter_by_value(current, "I", "V", "X")
        elif i == 1:
            letter_by_value(current, "X", "L", "C")
        elif i == 2:
            letter_by_value(current, "C", "D", "M")
        elif i == 3:
            result_array.append(current * "M")

    # reverses the result back so it has the proper order            
    return ''.join(reversed(result_array))

def run(rom_1, rom_2):		
	arabic1 = calculate_arabic(rom_1)
	arabic2 = calculate_arabic(rom_2)

	return calculate_roman(arabic1 + arabic2)
	
if __name__ == "__main__":
	assert run("VI", "VII") == "XIII"
	assert run("XII", "XXVII") == "XXXIX"
	assert run("CXXIII", "CCCXXI") == "CDXLIV"
	assert run("MMXVI", "CMXCIX") == "MMMXV"	
	