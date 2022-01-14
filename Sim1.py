import numpy as np
from decimal import Decimal
import matplotlib as mpl
import matplotlib.pyplot as plt

from Master import Master
from Slaver import Slave

if __name__ == '__main__':
    print("start")
    master = Master(1.5)
    slave1 = Slave(master, "slave1")
    # slave2 = Slave(master, "slave2")
    # print(master.showSlaves())

    # master send Sync info.
    for i in range(8):
        master.sendSync()

    print("slave1.offset")
    print(slave1.offset)
    # plt.plot([0, 1, 2, 3, 4, 5, 6, 7, 8], master.count.theoryMasterClock, master.count.theorySlaveClock)
    # plt.xlim(0, 10)
    # plt.ylim(0, 10)

    x = np.linspace(0, 8, 8)
    y1 = master.count.theoryMasterClock
    y2 = master.count.theorySlaveClock
    y3 = master.count.countSlaveClock
    y4 = master.count.countOffset
    plt.plot(x, y1, label='Master')
    plt.plot(x, y2, label='Slave')
    plt.plot(x, y3, ':b', label='Slave-offset')
    plt.legend()

    ##保存图片 直接输入文件路径，新建文件名字 
    ##dpi图片分辨率 越高越清晰。bbox_inches = 'tight',去掉空白部分
    plt.savefig('Sim1.png', dpi=400, bbox_inches = 'tight')

    plt.show()

    # print(y1)
    # print(y2)
    # print(y3)
    print("end")
