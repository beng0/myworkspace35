from pywinauto.application import Application
from pywinauto.keyboard import send_keys
from pywinauto import mouse
import time

# 打开程序
app = Application(backend="uia").start("notepad.exe")
# 选择窗口
wind_notepad1 = app["无标题 - 记事本"]
# 获取窗口所有控件,数字表示深度，表示打印出几层的子窗口
wind_notepad1.print_control_identifiers(3)
# 选择控件
edit = wind_notepad1["Edit"]
# 输入
edit.type_keys("python自动化12")
edit.type_keys("music")
# 键盘操作
# 全选
send_keys("^a")
# 复制
send_keys("^c")
#粘贴
send_keys("^v")
# 回车键
send_keys("{VK_RETURN}")
# 粘贴
send_keys("^v")
"""常用的一些按键操作：
字母按键用按键小写字母表示
常用的一些按键
ESC键：VK_ESCAPE 
回车键：VK_RETURN 
TAB键：VK_TAB 
Shift键：VK_SHIFT 
Ctrl键：VK_CONTROL
Alt键：VK_MENU
对于一些常用的按键，可以通过修饰符来表示，使用的时候比较方便
'+': {VK_SHIFT}
'^': {VK_CONTROL}
'%': {VK_MENU} Alt键
"""

# 鼠标操作
# 鼠标移动
for i in range(10):
    x = 10*i
    y = 10*i
    time.sleep(0.5)
    mouse.move(coords=(x,y))

# 鼠标点击
# 指定位置单击
# button指定左击还是右击，coords指定鼠标点击的位置
mouse.click(button='left', coords=(40, 40))
mouse.click('right',(800,800))

# 鼠标双击
mouse.double_click("left",(400,100))
# 按下鼠标,移动，释放鼠标
mouse.press("left",(400,400))
# mouse.move((900,900))
mouse.release("left",(900,900))

# 右键单击指定坐标
mouse.right_click(coords=(400,400))
# 鼠标中键点击指定坐标
mouse.wheel_click(coords=(400,400))
# 滚动鼠标
mouse.scroll(coords=(1200,300),wheel_dist=-3)















