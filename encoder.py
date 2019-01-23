#Code adapted for better usability XF0X KV0RED
#Thanks to KJ7ONP
#Documentation probably will be terrible. I can be reached on discord Zorro#0621
#This encoder will turn a 640x480 PNG image into a .dat file to be used with the GNU Radio flowgraph

from PIL import Image
from array import array
import math
import sys


COLOR_FREQ = 3579545.0
HCOUNT = 772 #HCOUNT is calcualted using 63.556 e-6 sec * 12.15 e6 pixels/sec = 772 pixels/line 
SAMP_RATE = HCOUNT * 60 * .999 * 525 / 2
RADIANS_PER_SAMPLE = 2 * math.pi * COLOR_FREQ / SAMP_RATE 

SYNCH_LEVEL = -40.0 # -40 IRE standard for NTSC while PAL and SECAM use -43 IRE
BLANKING_LEVEL = 0.0 # For NTSC, a setup of 7.5 IRE is usually applied, moving the black level to +7.5 IRE. For PAL and SECAM, the black level is aligned with the blanking level at 0 IRE.
BLACK_LEVEL = 7.5 # 7.4 IRE is standard for NTSC , PAL and SECAM both have 0 IRE black levels
WHITE_LEVEL = 100.0 # 100 IRE is standard for NTSC, PAL, and SECAM

EQUALIZING_PULSE = [SYNCH_LEVEL] * 28 + [BLANKING_LEVEL] * 358 #Interlaced Scanning Concept
SYNCHRONIZING_PULSE = [SYNCH_LEVEL] * 329 + [BLANKING_LEVEL] * 57 #Interlaced Scanning Concept
INTERVALS = EQUALIZING_PULSE * 6 + SYNCHRONIZING_PULSE * 6 + EQUALIZING_PULSE * 6 #Interlaced Scanning Concept
EXTRA_HALF_LINE = [BLANKING_LEVEL] * 386 #Interlaced Scanning Concept

FRONT_PORCH = [BLANKING_LEVEL] * 18
SYNCH_PULSE = [SYNCH_LEVEL] * 57


def main():
    # Argument checker
    if len(sys.argv) < 3:
        print("Usage: " + sys.argv[0] + " '<input_filename> [output_filename] [framecount]' If you are using multiple frames make sure they are named with 'imgxxxx' format. Ie: img0001.png")
        exit()

    framecount = int(sys.argv[3])
    input_filename = sys.argv[1]
    output_filename = sys.argv[2]
    #framecount = 4115
    #input_filename = multiple frames for 'video' or single frame for still image
    #output_filename = output file will be name.dat 

    if framecount <= 1:
        image = Image.open(input_filename)
        pixels = list(image.getdata())
        analog_baseband = genFields(pixels)
        writeFile(analog_baseband, output_filename, 'wb')

    else:
        extension = input_filename[-4:]
        file = input_filename[:-4]
        for i in range(framecount):
            currentframe = file + "%04d" % (i + 1,) + extension
            print(currentframe)
            image = Image.open(currentframe)
            pixels = list(image.getdata())
            analog_baseband = genFields(pixels)
            if i == 0:
                writeFile(analog_baseband, output_filename, 'wb')
            else:
                writeFile(analog_baseband, output_filename, 'ab')




def addBackPorch(analog_signal):
    analog_signal += [BLANKING_LEVEL] * 13
    l = len(analog_signal)
    for x in range(l, l + 31):
        analog_signal += [BLANKING_LEVEL + 20 * math.sin(math.pi + RADIANS_PER_SAMPLE * x)]
    analog_signal += [BLANKING_LEVEL] * 13
    return analog_signal


def addNonVisibleLine(analog_signal):
    analog_signal += SYNCH_PULSE
    analog_signal = addBackPorch(analog_signal)
    analog_signal += [BLANKING_LEVEL] * 658
    return analog_signal


def addFirstHalfFrame(analog_signal):
    analog_signal += SYNCH_PULSE
    analog_signal = addBackPorch(analog_signal)
    analog_signal += [BLACK_LEVEL] * 272
    return analog_signal


def addSecondHalfFrame(analog_signal):
    analog_signal += SYNCH_PULSE
    analog_signal = addBackPorch(analog_signal)
    analog_signal += [BLANKING_LEVEL] * 272 + [BLACK_LEVEL] * 368 + FRONT_PORCH
    return analog_signal


def addPixel(analog_signal, p):
    Er = float(p[0]) / 255
    Eg = float(p[1]) / 255
    Eb = float(p[2]) / 255

    Ey = 0.30 * Er + 0.59 * Eg + 0.11 * Eb
    Eq = 0.41 * (Eb - Ey) + 0.48 * (Er - Ey)
    Ei = -0.27 * (Eb - Ey) + 0.74 * (Er - Ey)

    #Genererates in phase COS SIN
    phase = RADIANS_PER_SAMPLE * len(analog_signal) + (33.0 / 180 * math.pi)
    Em = Ey + Eq * math.sin(phase) + Ei * math.cos(phase)

    analog_signal += [BLACK_LEVEL + (WHITE_LEVEL - BLACK_LEVEL) * Em]
    return analog_signal


def genFields(pixels):
    # Generated in phase field
    analog_signal = []
    analog_signal += INTERVALS
    for x in range(13):
        analog_signal = addNonVisibleLine(analog_signal)
    for line in range(0, 480, 2):
        analog_signal += SYNCH_PULSE
        analog_signal = addBackPorch(analog_signal)
        for x in range(line * 640, (line + 1) * 640):
            analog_signal = addPixel(analog_signal, pixels[x])
        analog_signal += FRONT_PORCH
    analog_signal = addFirstHalfFrame(analog_signal)

    #Generates put of phase field
    analog_signal += INTERVALS + EXTRA_HALF_LINE
    for x in range(12):
        analog_signal = addNonVisibleLine(analog_signal)
    analog_signal = addSecondHalfFrame(analog_signal)
    for line in range(1, 481, 2):
        analog_signal += SYNCH_PULSE
        analog_signal = addBackPorch(analog_signal)
        for x in range(line * 640, (line + 1) * 640):
            analog_signal = addPixel(analog_signal, pixels[x])
        analog_signal += FRONT_PORCH

    analog_signal = [0.75 - (0.25 / 40) * x for x in analog_signal]
    return analog_signal


def writeFile(analog_signal, filename, mode):
    f = open(filename, mode)
    ntsc_array = array('f', analog_signal)
    ntsc_array.tofile(f)
    f.close()

main()
