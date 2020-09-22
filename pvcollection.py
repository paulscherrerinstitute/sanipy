import epics

from config import load
from execute import parallel
#from execute import serial as parallel


class PVCollection:

    def __init__(self, chans):
        self.chans = chans
        self.pvs = [PV(ch) for ch in chans]

    @classmethod
    def from_file(cls, fname):
        chans = load(fname)
        return cls(chans)

    def connected(self):
        return self._run_all(lambda pv: pv.wait_for_connection(0.01))

    def status(self):
        return self._run_all(lambda pv: pv.status)

    def severity(self):
        return self._run_all(lambda pv: pv.severity)

    def value(self):
        return self._run_all(lambda pv: pv.value)

    def _run_all(self, func):
        return parallel(func, self.pvs)



class PV(epics.PV):

    @property
    def status(self):
        if not self.connected:
            return -1
        return super().status

    @property
    def severity(self):
        if not self.connected:
            return -1
        return super().severity

    @property
    def value(self):
        if not self.connected:
            return None
        return super().value



