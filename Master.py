class Count():
    def __init__(self):
        self.sycle = 0
        self.theoryMasterClock = []
        self.theorySlaveClock = []
        self.countSlaveClock = []
        self.countOffset = []

    def appendTheoryMasterClock(self, t):
        self.theoryMasterClock.append(t)

    def appendTheorySlaveClock(self, t):
        self.theorySlaveClock.append(t)

    def appendCountSlaveClock(self, t):
        self.countSlaveClock.append(t)

    def appendCountOffset(self, offset):
        self.countOffset.append(offset)

class Master():
    def __init__(self, tm=1):
        self.__slaves = []

        # tm 是周期和主时钟的币制，cycle 是发送周期
        self.tm = tm
        self.cycle = -1
        # 实例化一个 count
        self.count = Count()

    def getMasterClock(self):
        return self.tm * self.cycle

    def register(self, slave):
        self.__slaves.append(slave)

    def deleteS(self, slave):
        for index, value in enumerate(self.__slaves):
            # print(index, value)
            if value == slave:
                return self.__slaves.pop(index)
        return False

    def showSlaves(self):
        list = []
        for slave in self.__slaves:
            list.append(slave.slaveName)
        return list

    def sendSync(self):
        print('[master]: send Sync')

        self.cycle = self.cycle + 1
        for slave in self.__slaves:
            slave.sendDelay_Req(self, self.cycle, self.getMasterClock())

    def sendDelay_Resp(self, slave):
        print(f'[master]: got {slave.slaveName} messages, send Delay_Resp')
        slave.countOffset(self)
