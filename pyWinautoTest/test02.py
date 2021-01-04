from pywinauto import application
from pywinauto.keyboard import send_keys
from pywinauto import mouse
import time

# 打开程序
app = application.Application().connect(handle=0x1207A8)
# 选择窗口
wind_calc = app["计算器"]
wind_calc.print_control_identifiers()
# edit = wind_notepad1[""]
