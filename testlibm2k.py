#
# Copyright (c) 2019 Analog Devices Inc.
#
# This file is part of libm2k
# (see http://www.github.com/analogdevicesinc/libm2k).
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 2.1 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#

# This example will generate a binary counter on the first N_BITS of the
# digital interface and read them back - no additional connection required

import libm2k

n_bits=1

ctx=libm2k.m2kOpen()
if ctx is None:
	print("Connection Error: No ADALM2000 device available/connected to your PC.")
	exit(1)

dig=ctx.getDigital()
dig.reset()

dig.setSampleRateIn(4*3072000)
dig.setSampleRateOut(4*3072000)

for i in range(n_bits):
    dig.setDirection(i,libm2k.DIO_OUTPUT)
    dig.enableChannel(i,True)

dig.setCyclic(True)
dig.push([0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1])


# while True:
#     data = dig.getSamples(100)
#     for val in data:
#         print(bin(val))
#         print((val >> 13) & 1)

chosen_bits = [8]  

data = dig.getSamples(int(4 * 3072000*0.5))

# Create a separate file for each bit
file_handles = {bit: open(f"uoutput_bit_{bit}.txt", "w") for bit in chosen_bits}

for val in data:
    for bit in chosen_bits:
        # Extract the specific bit value
        bit_value = (val >> bit) & 1
        # Write the corresponding value to the respective file
        if bit_value == 1:
            file_handles[bit].write("1\n")
        else:
            file_handles[bit].write("-1\n")

# Close all file handles
for file in file_handles.values():
    file.close()

