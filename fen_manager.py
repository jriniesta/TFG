class FenManager:
    def __init__(self):
        self.fen_list = [
            'r2k1r2/b2p3p/1p1n1pn1/2p1q1p1/P1P5/1Q1NBb2/1P1PP1PN/RB2K3 w - - 0 1',
            '8/3p4/8/1P5r/8/2n5/PPP1P3/2K1B3 w - - 0 1',
            '4r3/1p1b2k1/3p1np1/3Pp2p/1P2P3/2N1BPP1/5K1P/8 b - - 0 1',
        ]

    def add_fen(self, fen):
        if fen not in self.fen_list:
            self.fen_list.append(fen)

    def remove_fen(self, fen):
        if fen in self.fen_list:
            self.fen_list.remove(fen)

    def get_fens(self):
        return self.fen_list