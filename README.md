# YAATT

This is an analog television transmitter for the HackRF using GNU Radio version 3.7.10
I am unsure if it will work on older versions.
For now it is designed to work with the HackRF but should be compatible with almost all SDR's with some modification.
This documentation is probably very hard to read and even harder to follow, if you need help send me an email or 
reach me via discord at Zorro#0621

# Usage

You will first need to encode an image or video into the correct format for GNU Radio. The file must be a 
640x480 PNG. I will include sample images and videos in the repository. You can encode a single image using encoder.py
with the following command line argument:

encoder.py test.png test.dat 1 

Replace 'test.png' and 'test.dat' with the correct file name and location.

# GNU Radio

Once you have the .dat file generated for your video or image open GNU radio and double click the block found on the far left
labeled 'File Source' and change the 'File' field to the location of the .dat file you just generated. 

I have the GNU radio frequency centered on 503 MHz which is the equivalent of channel 19.1 on a Television. If you want to test
decode with an RTL-SDR or something change this to 315 MHz as to not interfere with anything.

# Decoding

In Order to decode the transmitted signal, simply tune your Television to channel 19.1 to see the colored image/video.
You can also decode the transmitted signal in black and white using the SDR# TV plugin which can be found here: 

http://www.rtl-sdr.ru/page/no-title-2

