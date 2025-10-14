from collections import namedtuple, deque

Instr = namedtuple("Instr", "op rd rs1 rs2 imm txt")


class StallStrategy:
    """Strategy base: how to handle RAW hazards."""
    name = "StallOnly"
    def resolve(self, IF_ID, ID_EX, EX_MEM, MEM_WB):
        if not IF_ID: 
            return 0
        cur = IF_ID
        hazards = 0
        producers = [p for p in (ID_EX, EX_MEM, MEM_WB) if p and p.rd is not None]
        for p in producers:
            if cur.rs1 is not None and cur.rs1 == p.rd: hazards = max(hazards, 1)
            if cur.rs2 is not None and cur.rs2 == p.rd: hazards = max(hazards, 1)
        return hazards

class ForwardingStrategy(StallStrategy):
    name = "Forwarding"
    def resolve(self, IF_ID, ID_EX, EX_MEM, MEM_WB):
        if not IF_ID: return 0
        cur = IF_ID
        stall = 0
        if ID_EX and ID_EX.op == "LW" and ID_EX.rd is not None:
            if cur.rs1 == ID_EX.rd or cur.rs2 == ID_EX.rd:
                stall = max(stall, 1)
        return stall

class Pipeline:
    def __init__(self, instrs, strategy=StallStrategy()):
        self.ifq = deque(instrs)
        self.IF_ID = self.ID_EX = self.EX_MEM = self.MEM_WB = None
        self.WB_retired = 0
        self.cycle = 0
        self.stalls = 0
        self.strategy = strategy
        self.trace = [] 

    def step(self):
        self.cycle += 1

        retired = self.MEM_WB
        if retired and retired.op != "NOP":
            self.WB_retired += 1

        self.MEM_WB = self.EX_MEM
        self.EX_MEM = self.ID_EX

        stall = self.strategy.resolve(self.IF_ID, self.ID_EX, self.EX_MEM, self.MEM_WB)
        if stall == 0:
            self.ID_EX = self.IF_ID
            self.IF_ID = None
        else:
            self.stalls += stall 
        if stall == 0 and self.ifq:
            self.IF_ID = self.ifq.popleft()

        def name(x): return x.txt if x else "."
        self.trace.append({
            "cycle": self.cycle,
            "IF": name(self.IF_ID),
            "ID": name(self.ID_EX),
            "EX": name(self.EX_MEM),
            "MEM": name(self.MEM_WB),
            "WB": name(retired),
            "stall": stall
        })

    def run(self):
        while self.ifq or self.IF_ID or self.ID_EX or self.EX_MEM or self.MEM_WB:
            self.step()
        ipc = self.WB_retired / self.cycle if self.cycle else 0.0
        return {"cycles": self.cycle, "retired": self.WB_retired, "stalls": self.stalls, "IPC": ipc, "trace": self.trace}

prog = [
    Instr("LW",  r1:=1, None, None, 0,  "LW  r1, 0(r0)"),
    Instr("ADD", r2:=2, r1,   3,    0,  "ADD r2, r1, r3"),  
    Instr("MUL", r4:=4, r2,   5,    0,  "MUL r4, r2, r5"),  
    Instr("ADD", r6:=6, r4,   7,    0,  "ADD r6, r4, r7"),
    Instr("SW",  None, r6,   None,  0,  "SW  r6, 4(r0)"),
]

p1 = Pipeline(prog, strategy=StallStrategy())
res1 = p1.run()

p2 = Pipeline(prog, strategy=ForwardingStrategy())
res2 = p2.run()

def print_summary(title, res):
    print(f"\n== {title} ==")
    print(f"Cycles: {res['cycles']}, Retired: {res['retired']}, Stalls: {res['stalls']}, IPC: {res['IPC']:.2f}")
    print("cycle | IF               | ID               | EX               | MEM              | WB               | stall")
    for row in res["trace"]:
        print(f"{row['cycle']:>5} | {row['IF']:<16} | {row['ID']:<16} | {row['EX']:<16} | {row['MEM']:<16} | {row['WB']:<16} | {row['stall']}")

print_summary("StallOnly", res1)
print_summary("Forwarding", res2)
