#
# Copyright (c) 2019 Analog Devices Inc.
#
# This file is part of libm2k
# (see http://www.github.com/analogdevicesinc/libm2k).
#
# This program is free software: you can redistribute it and/or modify
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

# This example assumes the following connection:
# W1 -> DIO0
#
# The application will generate a square wave on W1 which is fed into DIO0
# and serves as external clock signal for the digital device. A pattern generated
# on DIO1 is plotted and displayed.

import libm2k
import numpy as np
import matplotlib.pyplot as plt

max_dac_sample_rate = 75000000
number_of_samples = 1024
clock_frequency = 75000000
digital_sampling_frequency = 1000000000
samples_per_period = 1024
digital_ch = 15
clock_ch = 0
acquisition_buffer_size = 4096


def generate_clock_signal(number_of_samples):

    buffer = []
    for i in range(int(number_of_samples/2)):
        buffer.append(0)
    for i in range(int(number_of_samples/2)):
        buffer.append(3.3)
    print(buffer)
    return buffer


# Context setup

ctx = libm2k.m2kOpen()
aout = ctx.getAnalogOut()
dig = ctx.getDigital()

# Prevent bad initial config
dig.reset()
aout.reset()

ctx.calibrateDAC()
ctx.calibrateADC()
import time
time.sleep(3)
# AnalogOut setup

# aout.setCyclic(True)
# aout.enableChannel(clock_ch, True)
# aout.setSampleRate(clock_ch, max_dac_sample_rate)
# oversampling_ratio = max_dac_sample_rate/(clock_frequency * number_of_samples)
# aout.setOversamplingRatio(clock_ch, int(oversampling_ratio))
# buffer = generate_clock_signal(number_of_samples)
# aout.push(clock_ch, buffer)

# Digital Setup

dig.reset()
dig.setExternalClocksource(True)
print("Clocksource external --> "+str(dig.isClocksourceExternal()))
dig.setCyclic(True)
dig.setSampleRateIn(digital_sampling_frequency)
dig.setDirection(clock_ch, libm2k.DIO_INPUT)
dig.enableChannel(clock_ch, False)
dig.setDirection(digital_ch, libm2k.DIO_INPUT)
dig.setSampleRateOut(digital_sampling_frequency)
dig.enableChannel(digital_ch, True)

duty = samples_per_period / 2  # 50%
signal = np.arange(samples_per_period) < duty
digital_buffer = list(map(lambda s: int(s) << digital_ch, signal))  # generate signal on desired channel

# for i in range(8):
#     buffer.extend(buffer)

# dig.push(digital_buffer)

# digital_data = dig.getSamples(acquisition_buffer_size)

chosen_bits = [1,2,3,4,8,9,10,11,12]    
# data = dig.getSamples(int(2 * 3072000*2))
print("Data Collection Started")
data = dig.getSamples(int(2 * 3072000))
print("Data Collection FInished")
# Create a separate file for each bit
file_handles = {bit: open(f"output_bit_{bit}.txt", "w") for bit in chosen_bits}

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
