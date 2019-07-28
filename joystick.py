import pyvjoy

JOY_AXIS_MIN = 0
JOY_AXIS_MAX = 0x7fff
JOY_AXIS_CTR = 0x3fff
stick = pyvjoy.VJoyDevice(1)
stick.set_axis(pyvjoy.HID_USAGE_Y, JOY_AXIS_CTR)
stick.set_axis(pyvjoy.HID_USAGE_X, JOY_AXIS_CTR)
stick.set_axis(pyvjoy.HID_USAGE_RY, JOY_AXIS_CTR)
stick.set_axis(pyvjoy.HID_USAGE_RX, JOY_AXIS_CTR)
stick.set_axis(pyvjoy.HID_USAGE_Z, JOY_AXIS_MIN)
stick.set_axis(pyvjoy.HID_USAGE_RZ, JOY_AXIS_MIN)

