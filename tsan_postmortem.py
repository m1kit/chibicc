import sys
import collections

class EventHandler:
    def __init__(self):
        self.variables = set()
        self.locks = set()
        self.tids = set()

        self.locksets = collections.defaultdict(lambda: set())
        self.read_guards = collections.defaultdict(lambda: dict())
        self.write_guards = collections.defaultdict(lambda: dict())

    def event_read(self, tid, target):
        self.variables.add(target)
        self.tids.add(tid)
        guards = self.read_guards[target]
        if tid not in guards:
            guards[tid] = set(self.locksets[tid])
        else:
            guards[tid] &= self.locksets[tid]

    def event_write(self, tid, target):
        self.variables.add(target)
        self.tids.add(tid)
        guards = self.write_guards[target]
        if tid not in guards:
            guards[tid] = set(self.locksets[tid])
        else:
            guards[tid] &= self.locksets[tid]

    def event_lock(self, tid, target):
        self.locks.add(target)
        self.tids.add(tid)
        ls = self.locksets[tid]
        assert target not in ls
        ls.add(target)

    def event_unlock(self, tid, target):
        self.locks.add(target)
        self.tids.add(tid)
        ls = self.locksets[tid]
        assert target in ls
        ls.remove(target)

    def event(self, kind, *args):
        return {
            'R': self.event_read,
            'W': self.event_write,
            'L': self.event_lock,
            'U': self.event_unlock,
        }[kind](*args)

    def report_race(self):
        print(f"{self.variables=}")
        print(f"{self.tids=}")
        print(f"{self.locks=}")

        global_variables = set(self.variables)
        for v in self.variables:
            vts = set(self.read_guards[v].keys()) | set(self.write_guards[v].keys())
            if len(vts) == 1:
                # local or thread-local.
                global_variables.remove(v)
        
        for v in global_variables:
            print(f"* Variable @{v}")

            for write0_tid, write0_guards in self.write_guards[v].items():
                for write1_tid, write1_guards in self.write_guards[v].items():
                    if write0_tid == write1_tid:
                        continue
                    common_guards = write0_guards & write1_guards
                    print('  [OK] ' if common_guards else '  [NG] ', end='')
                    print(f"WRITEs at {write0_tid} and WRITEs at {write1_tid} are guarded by {common_guards}")
                for read_tid, read_gurads in self.read_guards[v].items():
                    if write0_tid == read_tid:
                        continue
                    common_guards = write0_guards & read_gurads
                    print('  [OK] ' if common_guards else '  [NG] ', end='')
                    print(f"WRITEs at {write0_tid} and READs at {read_tid} are guarded by {common_guards}")

def main():
    handler = EventHandler()
    for line in sys.stdin:
        tag, kind, tid, target = line.strip().split()
        assert tag == '[TSan]'
        tid = int(tid)
        handler.event(kind, tid, target)
    handler.report_race()

if __name__ == '__main__':
    main()
