class ReliabilityTool:
    @staticmethod
    def reliable(reliability: int) -> bool:
        if 2 <= reliability <= 7 and reliability != 5:
            return True
        return False

    @staticmethod
    def sequenced(reliability: int) -> bool:
        if reliability == 1 or reliability == 4:
            return True
        return False

    @staticmethod
    def ordered(reliability: int) -> bool:
        if 1 <= reliability <= 4 and reliability != 2 or reliability == 7:
            return True
        return False