# YAATT

This is an analog television transmitter for the HackRF using GNU Radio version 3.7.10
I am unsure if it will work on older versions.
For now it is designed to work with the HackRF but should be compatible with almost all SDR's with some modification.

# Usage

You will first need to encode an image or video into the correct format for GNU Radio. The file must be a 
640x480 PNG. I will include sample images and videos in the repository. You can encode a single image using encoder.py
with the following command line argument:

encoder.py test.png test.dat 1 

Replace 'test.png' and 'test.dat' with the correct file name and location.

