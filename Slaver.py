
class Slave():
    def __init__(self, master, slaveName, ts=0.9):
        self.master = master
        self.slaveName = slaveName
        self.Stime = 0
        self.master.register(self)
        # slave的时钟
        self.ts = ts

        # 记录 T1 T2 T3 T4
        self.timeData = []
        self.timeReallData = []
        # 记录随机生成的 Delay; cycle为标准时间; cycle * ts 为时钟偏移
        self.realDelay = [[0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0]]
        self.cycle = -777
        # 记录 offset
        self.offset = []

    def reInit(self, cycle):
        self.cycle = cycle
        self.timeData = []
        self.timeMasterData = []

    def setOffset(self, master, T):
        self.offset.append((master.tm - self.ts) * T)

    def getSlaveClock(self):
        return self.ts * self.cycle

    def sendDelay_Req(self, master, cycle, T1):
        # 初始化数据仓库
        self.reInit(cycle)

        print(f'[{self.slaveName}]: got Sync, send Delay_Req')
        self.timeData.append(T1)
        self.timeMasterData.append(cycle)

        # ===========================================
        # 看到这里了，要一步一步过，排查问题。
        # ===========================================

        # 计算T2，添加T2
        T2 = self.timeData[0] + self.realDelay[0][0] + (master.tm - self.ts) * self.timeData[0]
        self.timeData.append(T2)
        T2r = self.timeData[0] + self.realDelay[0][0]
        self.timeMasterData.append(T2r)

        # 计算T3，添加T3
        # 一段传输流时延 = np.random() / 2 ； 立即发送前时延 = 0
        T3 = self.timeData[1] + 0 + 0
        self.timeData.append(T3)
        T3r = self.timeMasterData[1] + 0 + 0
        self.timeMasterData.append(T3r)

        # print(f'[{self.slaveName}]: cycle:{cycle}, time T:{self.timeData}.')
        self.master.sendDelay_Resp(self)

    def countOffset(self, master):
        # 计算T4，添加T4
        T4 = self.timeData[2] + self.realDelay[0][1] - (master.tm - self.ts) * self.timeData[2]
        self.timeData.append(T4)
        T4r = self.timeMasterData[2] + self.realDelay[0][1]

        offset = ((self.timeData[1] - self.timeData[0]) + (self.timeData[2] - self.timeData[3])) / 2
        self.offset.append(offset)

        # ================================
        # 问题：时间 T1 到 T4 没有记录正确📝
        # ================================
        print(self.timeMasterData)
        print(self.timeData)
        print(f'offset: {offset}')
        # 将数据传递给 master.count
        master.count.appendTheoryMasterClock(master.getMasterClock())
        master.count.appendTheorySlaveClock(self.getSlaveClock())
        master.count.appendCountSlaveClock(self.getSlaveClock() + offset)
        master.count.appendCountOffset(master.getMasterClock() - (self.getSlaveClock() + offset))
