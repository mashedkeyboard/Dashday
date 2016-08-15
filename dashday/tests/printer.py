# Tests the escpos functionality

from escpos import *
import os

def testSetFont():
    p = printer.Dummy()
    p.set("LEFT", "B", "B", 2, 2)
    if str(p.output) != r"b'\x1b!\x00\x1b!0\x1b{\x00\x1db\x00\x1bE\x01\x1b-\x00\x1bM\x01\x1ba\x00\x1dB\x00'":
        raise escpos.Error("Could not successfully complete dummy setting of font or produced incorrect output on dummy set")

def testPrintText():
    p = printer.Dummy()
    p.text("Test print")
    if str(p.output) != r"b'Test print'":
        raise escpos.Error("Could not successfully complete dummy print of text or produced incorrect output on dummy print")

def testPrintImage():
    p = printer.Dummy()
    p.image(os.path.join(os.path.realpath('resources/images/weather') + os.path.sep + "cloudy.png"))
    if str(p.output) != r"b'\x1dv0\x00\t\x006\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x80\x00\x00\x00\x00\x00\x00\x00\x0f\xfc\x00\x00\x00\x00\x00\x00\x00?\xff\x00\x00\x00\x00\x00\x00\x00\xff\xff\xc0\x00\x00\x00\x00\x00\x01\xfe\xbf\xe0\x00\x00\x00\x00\x00\x03\xf0\x03\xf0\x00\x00\x00\x00\x00/\xe0\x01\xfe\x80\x00\x00\x00\x01\xff\x80\x00\x7f\xe0\x00\x00\x00\x03\xff\x00\x00\x7f\xf0\x00\x00\x00\x0f\xff\x00\x00?\xfc\x00\x00\x00\x0f\xc4\x00\x00\x01|\x00\x00\x00\x1f\x02\xa0\x00\x00>\x00\x00\x00>?\xfe\x00\x00\x1f\x00\x00\x00<\xff\xff\xc0\x00\x0f\x00\x00\x00}\xff\xff\xe0\x00\x0f\x80\x00\x00\x7f\xfd_\xf8\x00\x07\x80\x00\x00\x7f\xe0\x01\xfc\x00\x07\x80\x00\x00\x7f\x80\x00~\x00\x07\x80\x00\x00~\x00\x00?\x00\x07\x80\x00\x05|\x00\x00\x0f\xb4\x07\x80\x00?\xf8\x00\x00\x07\xff\x0f\x00\x00\xff\xf0\x00\x00\x07\xff\xdf\x00\x03\xff\xf0\x00\x00\x03\xff\xff\x00\x07\xfa\xa0\x00\x00\x01\xab\xfe\x00\x0f\xc0\x00\x00\x00\x00\x01\xfc\x00\x0f\x80\x00\x00\x00\x00\x00|\x00\x1e\x00\x00\x00\x00\x00\x00>\x00>\x00\x00\x00\x00\x00\x00\x1f\x00<\x00\x00\x00\x00\x00\x00\x0f\x00<\x00\x00\x00\x00\x00\x00\x0f\x00x\x00\x00\x00\x00\x00\x00\x07\x80x\x00\x00\x00\x00\x00\x00\x07\x80x\x00\x00\x00\x00\x00\x00\x07\x80x\x00\x00\x00\x00\x00\x00\x07\x80x\x00\x00\x00\x00\x00\x00\x07\x80x\x00\x00\x00\x00\x00\x00\x07\x80<\x00\x00\x00\x00\x00\x00\x0f\x00|\x00\x00\x00\x00\x00\x00\x0f\x00<\x00\x00\x00\x00\x00\x00\x0f\x00\x1e\x00\x00\x00\x00\x00\x00\x1e\x00\x1f\x00\x00\x00\x00\x00\x00>\x00\x0f\x80\x00\x00\x00\x00\x00|\x00\x0f\xe0\x1c\x00\x00\x0e\x01\xfc\x00\x07\xfe\xfe\x00\x00\x1f\xdf\xf0\x00\x01\xff\xff\x00\x00?\xff\xe0\x00\x00\xff\xff\x80\x00\xff\xff\xc0\x00\x00?\xef\xf0\x03\xfd\xfe\x00\x00\x00\x00\x07\xff\x7f\xf0\x00\x00\x00\x00\x00\x01\xff\xff\xe0\x00\x00\x00\x00\x00\x00\x7f\xff\x80\x00\x00\x00\x00\x00\x00\x1f\xfc\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'":
        raise escpos.Error("Could not successfully complete dummy print of image or produced incorrect output on dummy print")

def testCutPaper():
    p = printer.Dummy()
    p.cut()
    if str(p.output) != r"b'\n\n\n\n\n\n\x1dV\x00'":
        raise escpos.Error("Could not successfully complete dummy cut or produced incorrect output on dummy cut")