class Player:
    __slots__ =["lifeTotal","counters", "deck", "field"]
    def __init__ (self):

        self.lifeTotal=40
        self.counters={"poison":0, "energy":0}
        self.deck=None
        self.field=None

    def getCounters(self):
        return self.counters

    def getLiveTotal(self):
        return self.lifeTotal

    def setLiveTotal(self, live):
        self.lifeTotal=live

    def changeLiveTotal(self,change):
        self.lifeTotal=self.lifeTotal+change

    def setDeck(self,deck):
        self.deck=deck
    def getPoisonCountersState(self):
        return self.counters["poison"]

    def isPlayerAlive(self):
        if self.getLiveTotal() >0 and self.getPoisonCountersState() <10:
            return True
        else:
            return False




