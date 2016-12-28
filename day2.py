# -*- coding=utf-8 -*-

"""
事件

pygame.event.get():来处理所有的事件，这好像打开大门让所有的人进入
pygame.event.wait():Pygame就会等到发生一个事件才继续下去，就好像你在门的猫眼上盯着外面一样，
                   来一个放一个……一般游戏中不太实用，因为游戏往往是需要动态运作的；
pygame.event.poll():根据现在的情形返回一个真实的事件，或者一个“什么都没有”

"""

import pygame
from pygame.locals import *
from sys import exit


def print_mouse_position():
    """
     屏幕滚动鼠标移动事件
    """
    # 初始化
    pygame.init()
    # 设置屏幕大小
    SCREEN_SIZE = (640, 480)
    screen = pygame.display.set_mode(SCREEN_SIZE, 0, 32)

    font = pygame.font.SysFont("arial", 16);
    font_height = font.get_linesize()

    # 定义事件列表
    event_text = []

    while True:

        event = pygame.event.wait()
        event_text.append(str(event))
        # 获得时间的名称
        event_text = event_text[-SCREEN_SIZE[1] / font_height:]
        # 这个切片操作保证了event_text里面只保留一个屏幕的文字

        if event.type == QUIT:
            exit()

        screen.fill((255, 255, 255))

        y = SCREEN_SIZE[1] - font_height
        # 找一个合适的起笔位置，最下面开始但是要留一行的空
        for text in reversed(event_text):
            screen.blit(font.render(text, True, (0, 255, 0)), (0, y))
            # 以后会讲
            y -= font_height
            # 把笔提一行

        pygame.display.update()


"""
处理鼠标事件
        MOUSEMOTION事件会在鼠标动作的时候发生，它有三个参数：

        buttons – 一个含有三个数字的元组，三个值分别代表左键、中键和右键，1就是按下了。
        pos     – 就是位置了……
        rel     – 代表了现在距离上次产生鼠标事件时的距离


        和MOUSEMOTION类似的，我们还有 MOUSEBUTTONDOWN 和 MOUSEBUTTONUP 两个事件，看名字就明白是什么意思了。
        很多时候，你只需要知道鼠标点下就可以了，那就可以不用上面那个比较强大（也比较复杂）的事件了。
        它们的参数为：
        button – 看清楚少了个s，这个值代表了哪个按键被操作
        pos    – 和上面一样

"""


def print_key_envent():
    """
    使用方向键控制图片位置
    """
    from config import static_path
    background_image_filename = static_path + '/2.png'
    pygame.init()
    screen = pygame.display.set_mode((640, 480), 0, 32)
    background = pygame.image.load(background_image_filename).convert()

    x, y = 0, 0
    move_x, move_y = 0, 0

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()
            if event.type == KEYDOWN:
                # 键盘有按下？
                if event.key == K_LEFT:
                    # 按下的是左方向键的话，把x坐标减一
                    move_x = -1
                elif event.key == K_RIGHT:
                    # 右方向键则加一
                    move_x = 1
                elif event.key == K_UP:
                    # 类似了
                    move_y = -1
                elif event.key == K_DOWN:
                    move_y = 1
            elif event.type == KEYUP:
                # 如果用户放开了键盘，图就不要动了
                move_x = 0
                move_y = 0

        print move_x, move_y
        # 计算出新的坐标
        x += move_x
        y += move_y

        screen.fill((0, 0, 0))
        screen.blit(background, (x, y))
        # 在新的位置上画图
        pygame.display.update()


"""
处理键盘事件
        KEYDOWN和KEYUP的参数描述如下：
        key – 按下或者放开的键值，是一个数字，估计地球上很少有人可以记住，
        所以Pygame中你可以使用K_xxx来表示，比如字母a就是K_a，还有K_SPACE和K_RETURN等。

        mod – 包含了组合键信息，如果mod & KMOD_CTRL是真的话，表示用户同时按下了Ctrl键。
        类似的还有KMOD_SHIFT，KMOD_ALT。

        unicode – 代表了按下键的Unicode值


事件过滤
        并不是所有的事件都需要处理的，就好像不是所有登门造访的人都是我们欢迎的一样。
        比如，俄罗斯方块就无视你的鼠标，而在游戏场景切换的时候，你按什么都是徒劳的。
        我们应该有一个方法来过滤掉一些我们不感兴趣的事件（当然我们可以不处理这些没兴趣的事件，
        但最好的方法还是让它们根本不进入我们的事件队列，就好像在门上贴着“XXX免进”一样），
        我们使用pygame.event.set_blocked(事件名)来完成。如果有好多事件需要过滤，
        可以传递一个列表，比如pygame.event.set_blocked([KEYDOWN, KEYUP])，
        如果你设置参数None，那么所有的事件有被打开了。与之相对的，我们使用
        pygame.event.set_allowed()来设定允许的事件。



产生事件
        通常玩家做什么，Pygame就产生对应的事件就可以了，不过有的时候我们需要模拟出一些事件来，
        比如录像回放的时候，我们就要把用户的操作再现一遍。

        为了产生事件，必须先造一个出来，然后再传递它：

        my_event = pygame.event.Event(KEYDOWN, key=K_SPACE, mod=0, unicode=u' ')
        #你也可以像下面这样写，看起来比较清晰（但字变多了……）
        my_event = pygame.event.Event(KEYDOWN, {"key":K_SPACE, "mod":0, "unicode":u' '})
        pygame.event.post(my_event)


        你甚至可以产生一个完全自定义的全新事件：

        CATONKEYBOARD = USEREVENT+1
        my_event = pygame.event.Event(CATONKEYBOARD, message="Bad cat!")
        pgame.event.post(my_event)

        #然后获得它
        for event in pygame.event.get():
            if event.type == CATONKEYBOARD:
                print event.message



"""

if __name__ == "__main__":
    print_key_envent()
