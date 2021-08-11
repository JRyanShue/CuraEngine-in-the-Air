"""
Allows for splicing gcode using the other python scripts
"""
# Test path: C:\Users\jryan\Documents\gcode tests\test.gcode
# Output path: C:\Users\jryan\Documents\gcode tests\spliced_test.gcode

import splicer

input_path = str(input("Specify initial gcode path: "))
output_path = str(input("Specify destination path: "))
number_of_parts = int(input("How many parts should be made? "))

print("Splicing:")
splicer.splice(input_path, output_path, number_of_parts)

