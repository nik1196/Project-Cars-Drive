import pyvjoy

JOY_AXIS_MIN = 1
JOY_AXIS_MAX = 32768//2
JOY_AXIS_CTR = 32768//2
stick = pyvjoy.VJoyDevice(1)
stick.set_axis(pyvjoy.HID_USAGE_Y, JOY_AXIS_CTR)
stick.set_axis(pyvjoy.HID_USAGE_X, JOY_AXIS_CTR)
stick.set_axis(pyvjoy.HID_USAGE_RY, JOY_AXIS_CTR)
stick.set_axis(pyvjoy.HID_USAGE_RX, JOY_AXIS_CTR)
stick.set_axis(pyvjoy.HID_USAGE_Z, JOY_AXIS_MIN)
stick.set_axis(pyvjoy.HID_USAGE_RZ, JOY_AXIS_MIN)

