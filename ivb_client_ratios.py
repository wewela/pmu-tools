
#
# auto generated TopDown description for Intel 3rd gen Core (code named IvyBridge)
# Please see http://ark.intel.com for more details on these CPUs.
#


# Constants

PipelineWidth = 4
MEM_L3_WEIGHT = 7
MEM_STLB_HIT_COST = 7
MEM_SFB_COST = 13
MEM_4KALIAS_COST = 7
MEM_XSNP_HITM_COST = 60
MEM_XSNP_HIT_COST = 43
MEM_XSNP_NONE_COST = 29
MS_SWITCHES_COST = 3

# Aux. formulas

def FLOP_count(EV, level):
    return ( 1 *(EV("FP_COMP_OPS_EXE.SSE_SCALAR_SINGLE", level) + EV("FP_COMP_OPS_EXE.SSE_SCALAR_DOUBLE", level))+ 2 * EV("FP_COMP_OPS_EXE.SSE_PACKED_DOUBLE", level) + 4 *(EV("FP_COMP_OPS_EXE.SSE_PACKED_SINGLE", level) + EV("SIMD_FP_256.PACKED_DOUBLE", level))+ 8 * EV("SIMD_FP_256.PACKED_SINGLE", level) )
def FewUopsExecutedThreshold(EV, level):
    return EV("UOPS_EXECUTED.CYCLES_GE_3_UOPS_EXEC", level) if(IPC(EV, level) > 1.25)else EV("UOPS_EXECUTED.CYCLES_GE_2_UOPS_EXEC", level)
def BackendBoundAtEXE_stalls(EV, level):
    return ( EV("CYCLE_ACTIVITY.CYCLES_NO_EXECUTE", level) + EV("UOPS_EXECUTED.CYCLES_GE_1_UOP_EXEC", level) - FewUopsExecutedThreshold(EV, level) - EV("RS_EVENTS.EMPTY_CYCLES", level) + EV("RESOURCE_STALLS.SB", level) )
def BackendBoundAtEXE(EV, level):
    return BackendBoundAtEXE_stalls(EV, level) / CLKS(EV, level)
def MemL3HitFraction(EV, level):
    return EV("MEM_LOAD_UOPS_RETIRED.LLC_HIT", level) /(EV("MEM_LOAD_UOPS_RETIRED.LLC_HIT", level) + MEM_L3_WEIGHT * EV("MEM_LOAD_UOPS_RETIRED.LLC_MISS", level) )
def MispredClearsFraction(EV, level):
    return EV("BR_MISP_RETIRED.ALL_BRANCHES", level) /(EV("BR_MISP_RETIRED.ALL_BRANCHES", level) + EV("MACHINE_CLEARS.COUNT", level) )
def AvgRsEmptyPeriodClears(EV, level):
    return ( EV("RS_EVENTS.EMPTY_CYCLES", level) - EV("ICACHE.IFETCH_STALL", level))/ EV("RS_EVENTS.EMPTY_END", level)
def RetireUopFraction(EV, level):
    return EV("UOPS_RETIRED.RETIRE_SLOTS", level) / EV("UOPS_ISSUED.ANY", level)
def SLOTS(EV, level):
    return PipelineWidth * CLKS(EV, level)
def IPC(EV, level):
    return EV("INST_RETIRED.ANY", level) / CLKS(EV, level)
def UPI(EV, level):
    return EV("UOPS_RETIRED.RETIRE_SLOTS", level) / EV("INST_RETIRED.ANY", level)
def InstPerTakenBranch(EV, level):
    return EV("INST_RETIRED.ANY", level) / EV("BR_INST_RETIRED.NEAR_TAKEN", level)
def DSBCoverage(EV, level):
    return ( EV("IDQ.DSB_UOPS", level) + EV("LSD.UOPS", level))/(EV("IDQ.DSB_UOPS", level) + EV("LSD.UOPS", level) + EV("IDQ.MITE_UOPS", level) + EV("IDQ.MS_UOPS", level) )
def ILP(EV, level):
    return EV("UOPS_EXECUTED.THREAD", level) / EV("UOPS_EXECUTED.CYCLES_GE_1_UOP_EXEC", level)
def MLP(EV, level):
    return EV("L1D_PEND_MISS.PENDING", level) / EV("L1D_PEND_MISS.PENDING_CYCLES", level)
def L1dMissLatency(EV, level):
    return EV("L1D_PEND_MISS.PENDING", level) / EV("MEM_LOAD_UOPS_RETIRED.L1_MISS", level)
def CPUUtilization(EV, level):
    return EV("CPU_CLK_UNHALTED.REF_TSC", level) / XXX
def TurboUtilization(EV, level):
    return CLKS(EV, level) / EV("CPU_CLK_UNHALTED.REF_TSC", level)
def GFLOPs(EV, level):
    return FLOP_count(EV, level) / 1e9 / XXX
def CLKS(EV, level):
    return EV("CPU_CLK_UNHALTED.THREAD", level)

# Event groups


class FrontendBound:
    name = "FrontendBound"
    domain = "Slots"
    area = "FE"
    desc = """
This category reflects slots where the Frontend of the processor undersupplies
its Backend."""
    level = 1
    def compute(self, EV):
        try:
            self.val = EV("IDQ_UOPS_NOT_DELIVERED.CORE", 1) / SLOTS(EV, 1)
            self.thresh = (self.val > 0.2)
        except ZeroDivisionError:
            print "FrontendBound zero division"
            self.val = 0
            self.thresh = False
        return self.val

class FrontendLatency:
    name = "Frontend Latency"
    domain = "Slots"
    area = "FE"
    desc = """
This metric represents slots fraction CPU was stalled due to Frontend latency
issues."""
    level = 2
    def compute(self, EV):
        try:
            self.val = PipelineWidth * EV("IDQ_UOPS_NOT_DELIVERED.CYCLES_0_UOPS_DELIV.CORE", 2) / SLOTS(EV, 2)
            self.thresh = (self.val > 0.15) and self.parent.thresh
        except ZeroDivisionError:
            print "FrontendLatency zero division"
            self.val = 0
            self.thresh = False
        return self.val

class ICacheMisses:
    name = "ICache Misses"
    domain = "Clocks"
    area = "FE"
    desc = """
This metric represents cycles fraction CPU was stalled due to instruction
cache misses."""
    level = 3
    def compute(self, EV):
        try:
            self.val = ( EV("ICACHE.IFETCH_STALL", 3) - EV("ITLB_MISSES.WALK_DURATION", 3))/ CLKS(EV, 3)
            self.thresh = (self.val > 0.05) and self.parent.thresh
        except ZeroDivisionError:
            print "ICacheMisses zero division"
            self.val = 0
            self.thresh = False
        return self.val

class ITLBmisses:
    name = "ITLB misses"
    domain = "Clocks"
    area = "FE"
    desc = """
This metric represents cycles fraction CPU was stalled due to instruction TLB
misses."""
    level = 3
    def compute(self, EV):
        try:
            self.val = EV("ITLB_MISSES.WALK_DURATION", 3) / CLKS(EV, 3)
            self.thresh = (self.val > 0.05) and self.parent.thresh
        except ZeroDivisionError:
            print "ITLBmisses zero division"
            self.val = 0
            self.thresh = False
        return self.val

class BranchResteers:
    name = "Branch Resteers"
    domain = "Clocks"
    area = "FE"
    desc = """
This metric represents cycles fraction CPU was stalled due to Branch Resteers."""
    level = 3
    def compute(self, EV):
        try:
            self.val = ( EV("BR_MISP_RETIRED.ALL_BRANCHES", 3) + EV("MACHINE_CLEARS.COUNT", 3) + EV("BACLEARS.ANY", 3))* AvgRsEmptyPeriodClears(EV, 3) / CLKS(EV, 3)
            self.thresh = (self.val > 0.05) and self.parent.thresh
        except ZeroDivisionError:
            print "BranchResteers zero division"
            self.val = 0
            self.thresh = False
        return self.val

class DSBswitches:
    name = "DSB switches"
    domain = "Clocks"
    area = "FE"
    desc = """
This metric represents cycles fraction CPU was stalled due to switches from
DSB to MITE pipelines."""
    level = 3
    def compute(self, EV):
        try:
            self.val = EV("DSB2MITE_SWITCHES.PENALTY_CYCLES", 3) / CLKS(EV, 3)
            self.thresh = (self.val > 0.05) and self.parent.thresh
        except ZeroDivisionError:
            print "DSBswitches zero division"
            self.val = 0
            self.thresh = False
        return self.val

class LCP:
    name = "LCP"
    domain = "Clocks"
    area = "FE"
    desc = """
This metric represents cycles fraction CPU was stalled due to Length Changing
Prefixes (LCPs)."""
    level = 3
    def compute(self, EV):
        try:
            self.val = EV("ILD_STALL.LCP", 3) / CLKS(EV, 3)
            self.thresh = (self.val > 0.05) and self.parent.thresh
        except ZeroDivisionError:
            print "LCP zero division"
            self.val = 0
            self.thresh = False
        return self.val

class MSswitches:
    name = "MS switches"
    domain = "Clocks"
    area = "FE"
    desc = """
This metric represents cycles fraction CPU was stalled due to switches of uop
delivery to the Microcode Sequencer (MS)."""
    level = 3
    def compute(self, EV):
        try:
            self.val = MS_SWITCHES_COST * EV("IDQ.MS_SWITCHES", 3) / CLKS(EV, 3)
            self.thresh = (self.val > 0.05) and self.parent.thresh
        except ZeroDivisionError:
            print "MSswitches zero division"
            self.val = 0
            self.thresh = False
        return self.val

class FrontendBandwidth:
    name = "Frontend Bandwidth"
    domain = "Slots"
    area = "FE"
    desc = """
This metric represents slots fraction CPU was stalled due to Frontend
bandwidth issues."""
    level = 2
    def compute(self, EV):
        try:
            self.val = self.FrontendBound.compute(EV) - self.FrontendLatency.compute(EV)
            self.thresh = (self.val > 0.1) & (IPC(EV, 2) > 2.0) and self.parent.thresh
        except ZeroDivisionError:
            print "FrontendBandwidth zero division"
            self.val = 0
            self.thresh = False
        return self.val

class MITE:
    name = "MITE"
    domain = "Clocks"
    area = "FE"
    desc = """
This metric represents cycles fraction in which CPU was likely limited due to
the MITE fetch pipeline."""
    level = 3
    def compute(self, EV):
        try:
            self.val = ( EV("IDQ.ALL_MITE_CYCLES_ANY_UOPS", 3) - EV("IDQ.ALL_MITE_CYCLES_4_UOPS", 3))/ CLKS(EV, 3)
            self.thresh = (self.val > 0.1) and self.parent.thresh
        except ZeroDivisionError:
            print "MITE zero division"
            self.val = 0
            self.thresh = False
        return self.val

class DSB:
    name = "DSB"
    domain = "Clocks"
    area = "FE"
    desc = """
This metric represents cycles fraction in which CPU was likely limited due to
DSB (decoded uop cache) fetch pipeline."""
    level = 3
    def compute(self, EV):
        try:
            self.val = ( EV("IDQ.ALL_DSB_CYCLES_ANY_UOPS", 3) - EV("IDQ.ALL_DSB_CYCLES_4_UOPS", 3))/ CLKS(EV, 3)
            self.thresh = (self.val > 0.3) and self.parent.thresh
        except ZeroDivisionError:
            print "DSB zero division"
            self.val = 0
            self.thresh = False
        return self.val

class LSD:
    name = "LSD"
    domain = "Clocks"
    area = "FE"
    desc = """
This metric represents cycles fraction in which CPU was likely limited due to
LSD (Loop Stream Detector) unit."""
    level = 3
    def compute(self, EV):
        try:
            self.val = ( EV("LSD.CYCLES_ACTIVE", 3) - EV("LSD.CYCLES_4_UOPS", 3))/ CLKS(EV, 3)
            self.thresh = (self.val > 0.1) and self.parent.thresh
        except ZeroDivisionError:
            print "LSD zero division"
            self.val = 0
            self.thresh = False
        return self.val

class BadSpeculation:
    name = "BadSpeculation"
    domain = "Slots"
    area = "BAD"
    desc = """
This category reflects slots wasted due to incorrect speculations, which
include slots used to allocate uops that do not eventually get retired and
slots for which allocation was blocked due to recovery from earlier incorrect
speculation."""
    level = 1
    def compute(self, EV):
        try:
            self.val = ( EV("UOPS_ISSUED.ANY", 1) - EV("UOPS_RETIRED.RETIRE_SLOTS", 1) + PipelineWidth * EV("INT_MISC.RECOVERY_CYCLES", 1))/ SLOTS(EV, 1)
            self.thresh = (self.val > 0.1)
        except ZeroDivisionError:
            print "BadSpeculation zero division"
            self.val = 0
            self.thresh = False
        return self.val

class BranchMispredicts:
    name = "Branch Mispredicts"
    domain = "Slots"
    area = "BAD"
    desc = """
This metric represents slots fraction CPU was impacted by Branch
Missprediction."""
    level = 2
    def compute(self, EV):
        try:
            self.val = MispredClearsFraction(EV, 2) * self.BadSpeculation.compute(EV)
            self.thresh = (self.val > 0.05) and self.parent.thresh
        except ZeroDivisionError:
            print "BranchMispredicts zero division"
            self.val = 0
            self.thresh = False
        return self.val

class MachineClears:
    name = "Machine Clears"
    domain = "Slots"
    area = "BAD"
    desc = """
This metric represents slots fraction CPU was impacted by Machine Clears."""
    level = 2
    def compute(self, EV):
        try:
            self.val = self.BadSpeculation.compute(EV) - self.BranchMispredicts.compute(EV)
            self.thresh = (self.val > 0.05) and self.parent.thresh
        except ZeroDivisionError:
            print "MachineClears zero division"
            self.val = 0
            self.thresh = False
        return self.val

class Backend_Bound:
    name = "Backend_Bound"
    domain = "Slots"
    area = "BE"
    desc = """
This category reflects slots where no uops are being delivered due to a lack
of required resources for accepting more uops in the Backend of the pipeline."""
    level = 1
    def compute(self, EV):
        try:
            self.val = 1 -(self.FrontendBound.compute(EV) + self.BadSpeculation.compute(EV) + self.Retiring.compute(EV) )
            self.thresh = (self.val > 0.2)
        except ZeroDivisionError:
            print "Backend_Bound zero division"
            self.val = 0
            self.thresh = False
        return self.val

class MemoryBound:
    name = "MemoryBound"
    domain = "Clocks"
    area = "BE/Mem"
    desc = """
This metric represents how much Memory subsystem was a bottleneck."""
    level = 2
    def compute(self, EV):
        try:
            self.val = ( EV("CYCLE_ACTIVITY.STALLS_LDM_PENDING", 2) + EV("RESOURCE_STALLS.SB", 2))/ CLKS(EV, 2)
            self.thresh = (self.val > 0.2) and self.parent.thresh
        except ZeroDivisionError:
            print "MemoryBound zero division"
            self.val = 0
            self.thresh = False
        return self.val

class L1Bound:
    name = "L1 Bound"
    domain = "Clocks"
    area = "BE/Mem"
    desc = """
This metric represents how often CPU was stalled without missing the L1 data
cache."""
    level = 3
    def compute(self, EV):
        try:
            self.val = ( EV("CYCLE_ACTIVITY.STALLS_LDM_PENDING", 3) - EV("CYCLE_ACTIVITY.STALLS_L1D_PENDING", 3))/ CLKS(EV, 3)
            self.thresh = (self.val > 0.07) and self.parent.thresh
        except ZeroDivisionError:
            print "L1Bound zero division"
            self.val = 0
            self.thresh = False
        return self.val

class DTLBOverhead:
    name = "DTLBOverhead"
    domain = "Clocks"
    area = "BE/Mem"
    desc = ""
    level = 4
    def compute(self, EV):
        try:
            self.val = ( MEM_STLB_HIT_COST * EV("DTLB_LOAD_MISSES.STLB_HIT", 4) + EV("DTLB_LOAD_MISSES.WALK_DURATION", 4))/ CLKS(EV, 4)
            self.thresh = self.val > 0.0 and self.parent.thresh
        except ZeroDivisionError:
            print "DTLBOverhead zero division"
            self.val = 0
            self.thresh = False
        return self.val

class LoadsBlockedbyStoreForwarding:
    name = "Loads Blocked by Store Forwarding"
    domain = "Clocks"
    area = "BE/Mem"
    desc = ""
    level = 4
    def compute(self, EV):
        try:
            self.val = MEM_SFB_COST * EV("LD_BLOCKS.STORE_FORWARD", 4) / CLKS(EV, 4)
            self.thresh = self.val > 0.0 and self.parent.thresh
        except ZeroDivisionError:
            print "LoadsBlockedbyStoreForwarding zero division"
            self.val = 0
            self.thresh = False
        return self.val

class SplitLoads:
    name = "Split Loads"
    domain = "Clocks"
    area = "BE/Mem"
    desc = ""
    level = 4
    def compute(self, EV):
        try:
            self.val = L1dMissLatency(EV, 4) * EV("LD_BLOCKS.NO_SR", 4) / CLKS(EV, 4)
            self.thresh = self.val > 0.0 and self.parent.thresh
        except ZeroDivisionError:
            print "SplitLoads zero division"
            self.val = 0
            self.thresh = False
        return self.val

class G4KAliasing:
    name = "4K Aliasing"
    domain = "Clocks"
    area = "BE/Mem"
    desc = ""
    level = 4
    def compute(self, EV):
        try:
            self.val = MEM_4KALIAS_COST * EV("LD_BLOCKS_PARTIAL.ADDRESS_ALIAS", 4) / CLKS(EV, 4)
            self.thresh = self.val > 0.0 and self.parent.thresh
        except ZeroDivisionError:
            print "G4KAliasing zero division"
            self.val = 0
            self.thresh = False
        return self.val

class L2Bound:
    name = "L2 Bound"
    domain = "Clocks"
    area = "BE/Mem"
    desc = """
This metric represents how often CPU was stalled on L2 cache."""
    level = 3
    def compute(self, EV):
        try:
            self.val = ( EV("CYCLE_ACTIVITY.STALLS_L1D_PENDING", 3) - EV("CYCLE_ACTIVITY.STALLS_L2_PENDING", 3))/ CLKS(EV, 3)
            self.thresh = (self.val > 0.03) and self.parent.thresh
        except ZeroDivisionError:
            print "L2Bound zero division"
            self.val = 0
            self.thresh = False
        return self.val

class L3Bound:
    name = "L3 Bound"
    domain = "Clocks"
    area = "BE/Mem"
    desc = """
This metric represents how often CPU was stalled on L3 cache or contended with
a sibling Core."""
    level = 3
    def compute(self, EV):
        try:
            self.val = MemL3HitFraction(EV, 3) * EV("CYCLE_ACTIVITY.STALLS_L2_PENDING", 3) / CLKS(EV, 3)
            self.thresh = (self.val > 0.1) and self.parent.thresh
        except ZeroDivisionError:
            print "L3Bound zero division"
            self.val = 0
            self.thresh = False
        return self.val

class ContestedAccesses:
    name = "Contested Accesses"
    domain = "Clocks"
    area = "BE/Mem"
    desc = ""
    level = 4
    def compute(self, EV):
        try:
            self.val = MEM_XSNP_HITM_COST *(EV("MEM_LOAD_UOPS_LLC_HIT_RETIRED.XSNP_HITM", 4) + EV("MEM_LOAD_UOPS_LLC_HIT_RETIRED.XSNP_MISS", 4))/ CLKS(EV, 4)
            self.thresh = self.val > 0.0 and self.parent.thresh
        except ZeroDivisionError:
            print "ContestedAccesses zero division"
            self.val = 0
            self.thresh = False
        return self.val

class DataSharing:
    name = "Data Sharing"
    domain = "Clocks"
    area = "BE/Mem"
    desc = ""
    level = 4
    def compute(self, EV):
        try:
            self.val = MEM_XSNP_HIT_COST * EV("MEM_LOAD_UOPS_LLC_HIT_RETIRED.XSNP_HIT", 4) / CLKS(EV, 4)
            self.thresh = self.val > 0.0 and self.parent.thresh
        except ZeroDivisionError:
            print "DataSharing zero division"
            self.val = 0
            self.thresh = False
        return self.val

class L3Latency:
    name = "L3 Latency"
    domain = "Clocks"
    area = "BE/Mem"
    desc = """
This metric is a rough aggregate estimate of cycles fraction where CPU
accessed L3 cache for all load requests, while there was no contention/sharing
with a sibiling core."""
    level = 4
    def compute(self, EV):
        try:
            self.val = MEM_XSNP_NONE_COST * EV("MEM_LOAD_UOPS_RETIRED.LLC_HIT", 4) / CLKS(EV, 4)
            self.thresh = (self.val > 0.1) and self.parent.thresh
        except ZeroDivisionError:
            print "L3Latency zero division"
            self.val = 0
            self.thresh = False
        return self.val

class DRAMBound:
    name = "DRAM Bound"
    domain = "Clocks"
    area = "BE/Mem"
    desc = """
This metric represents how often CPU was stalled on main memory (DRAM)."""
    level = 3
    def compute(self, EV):
        try:
            self.val = ( 1 - MemL3HitFraction(EV, 3))* EV("CYCLE_ACTIVITY.STALLS_L2_PENDING", 3) / CLKS(EV, 3)
            self.thresh = (self.val > 0.1) and self.parent.thresh
        except ZeroDivisionError:
            print "DRAMBound zero division"
            self.val = 0
            self.thresh = False
        return self.val

class MEMBandwidth:
    name = "MEM Bandwidth"
    domain = "Clocks"
    area = "BE/Mem"
    desc = """
This metric represents how often CPU was likely stalled due to approaching
bandwidth limits of main memory (DRAM)."""
    level = 4
    def compute(self, EV):
        try:
            self.val = EV("OFFCORE_REQUESTS_OUTSTANDING.DEMAND_DATA_RD:cmask=6", 4) / CLKS(EV, 4)
            self.thresh = (self.val > 0.1) and self.parent.thresh
        except ZeroDivisionError:
            print "MEMBandwidth zero division"
            self.val = 0
            self.thresh = False
        return self.val

class MEMLatency:
    name = "MEM Latency"
    domain = "Clocks"
    area = "BE/Mem"
    desc = """
This metric represents how often CPU was likely stalled due to latency from
main memory (DRAM)."""
    level = 4
    def compute(self, EV):
        try:
            self.val = ( EV("OFFCORE_REQUESTS_OUTSTANDING.CYCLES_WITH_DEMAND_DATA_RD", 4) - EV("OFFCORE_REQUESTS_OUTSTANDING.DEMAND_DATA_RD:cmask=6", 4))/ CLKS(EV, 4)
            self.thresh = (self.val > 0.1) and self.parent.thresh
        except ZeroDivisionError:
            print "MEMLatency zero division"
            self.val = 0
            self.thresh = False
        return self.val

class StoresBound:
    name = "Stores Bound"
    domain = "Clocks"
    area = "BE/Mem"
    desc = """
This metric represents how often CPU was stalled on due to store operations."""
    level = 3
    def compute(self, EV):
        try:
            self.val = self.MemoryBound.compute(EV) -(EV("CYCLE_ACTIVITY.STALLS_LDM_PENDING", 3) / CLKS(EV, 3) )
            self.thresh = (self.val > 0.2) and self.parent.thresh
        except ZeroDivisionError:
            print "StoresBound zero division"
            self.val = 0
            self.thresh = False
        return self.val

class FalseSharing:
    name = "False Sharing"
    domain = "Clocks"
    area = "BE/Mem"
    desc = """
This metric represents how often CPU was stalled on due to store operations."""
    level = 4
    def compute(self, EV):
        try:
            self.val = MEM_XSNP_HITM_COST *(EV("MEM_LOAD_UOPS_LLC_HIT_RETIRED.XSNP_HITM", 4) + EV("OFFCORE_RESPONSE.DEMAND_RFO.LLC_HIT.HITM_OTHER_CORE", 4))/ CLKS(EV, 4)
            self.thresh = (self.val > 0.2) and self.parent.thresh
        except ZeroDivisionError:
            print "FalseSharing zero division"
            self.val = 0
            self.thresh = False
        return self.val

class SplitStores:
    name = "Split Stores"
    domain = "Stores"
    area = "BE/Mem"
    desc = """
This metric represents rate of split store accesses."""
    level = 4
    def compute(self, EV):
        try:
            self.val = EV("MEM_UOPS_RETIRED.SPLIT_STORES", 4) / EV("MEM_UOPS_RETIRED.ALL_STORES", 4)
            self.thresh = self.val > 0.0 and self.parent.thresh
        except ZeroDivisionError:
            print "SplitStores zero division"
            self.val = 0
            self.thresh = False
        return self.val

class DTLBStoreOverhead:
    name = "DTLB Store Overhead"
    domain = "Clocks"
    area = "BE/Mem"
    desc = """
This metric represents cycles fraction spent handling first-level data TLB
store misses."""
    level = 4
    def compute(self, EV):
        try:
            self.val = ( MEM_STLB_HIT_COST * EV("DTLB_STORE_MISSES.STLB_HIT", 4) + EV("DTLB_STORE_MISSES.WALK_DURATION", 4))/ CLKS(EV, 4)
            self.thresh = (self.val > 0.05) and self.parent.thresh
        except ZeroDivisionError:
            print "DTLBStoreOverhead zero division"
            self.val = 0
            self.thresh = False
        return self.val

class CoreBound:
    name = "CoreBound"
    domain = "Clocks"
    area = "BE/Core"
    desc = """
This metric represents how much Core non-memory issues were a bottleneck."""
    level = 2
    def compute(self, EV):
        try:
            self.val = BackendBoundAtEXE(EV, 2) - self.MemoryBound.compute(EV)
            self.thresh = (self.val > 0.1) and self.parent.thresh
        except ZeroDivisionError:
            print "CoreBound zero division"
            self.val = 0
            self.thresh = False
        return self.val

class DividerActive:
    name = "DividerActive"
    domain = "Clocks"
    area = "BE/Core"
    desc = ""
    level = 3
    def compute(self, EV):
        try:
            self.val = EV("ARITH.FPU_DIV_ACTIVE", 3) / CLKS(EV, 3)
            self.thresh = (self.val > 0.1) and self.parent.thresh
        except ZeroDivisionError:
            print "DividerActive zero division"
            self.val = 0
            self.thresh = False
        return self.val

class PortsUtilization:
    name = "PortsUtilization"
    domain = "Clocks"
    area = "BE/Core"
    desc = """
This metric represents cycles fraction application was stalled due to Core
computatio issues (non divider-related)."""
    level = 3
    def compute(self, EV):
        try:
            self.val = self.CoreBound.compute(EV) - self.DividerActive.compute(EV)
            self.thresh = (self.val > 0.1) and self.parent.thresh
        except ZeroDivisionError:
            print "PortsUtilization zero division"
            self.val = 0
            self.thresh = False
        return self.val

class G0_Ports:
    name = "0_Ports"
    domain = "Clocks"
    area = "BE/Core"
    desc = """
This metric represents cycles fraction CPU executed no uops on any execution
port."""
    level = 4
    def compute(self, EV):
        try:
            self.val = ( EV("CYCLE_ACTIVITY.CYCLES_NO_EXECUTE", 4) - EV("RS_EVENTS.EMPTY_CYCLES", 4))/ CLKS(EV, 4)
            self.thresh = (self.val > 0.1) and self.parent.thresh
        except ZeroDivisionError:
            print "G0_Ports zero division"
            self.val = 0
            self.thresh = False
        return self.val

class G1_Port:
    name = "1_Port"
    domain = "Clocks"
    area = "BE/Core"
    desc = """
This metric represents cycles fraction CPU executed total of 1 uop per cycle
on all execution ports."""
    level = 4
    def compute(self, EV):
        try:
            self.val = ( EV("UOPS_EXECUTED.CYCLES_GE_1_UOP_EXEC", 4) - EV("UOPS_EXECUTED.CYCLES_GE_2_UOPS_EXEC", 4))/ CLKS(EV, 4)
            self.thresh = (self.val > 0.1) and self.parent.thresh
        except ZeroDivisionError:
            print "G1_Port zero division"
            self.val = 0
            self.thresh = False
        return self.val

class G2_Ports:
    name = "2_Ports"
    domain = "Clocks"
    area = "BE/Core"
    desc = """
This metric represents cycles fraction CPU executed total of 2 uops per cycle
on all execution ports."""
    level = 4
    def compute(self, EV):
        try:
            self.val = ( EV("UOPS_EXECUTED.CYCLES_GE_2_UOPS_EXEC", 4) - EV("UOPS_EXECUTED.CYCLES_GE_3_UOPS_EXEC", 4))/ CLKS(EV, 4)
            self.thresh = (self.val > 0.1) and self.parent.thresh
        except ZeroDivisionError:
            print "G2_Ports zero division"
            self.val = 0
            self.thresh = False
        return self.val

class G3m_Ports:
    name = "3m_Ports"
    domain = "Clocks"
    area = "BE/Core"
    desc = """
This metric represents cycles fraction CPU executed total of 3 or more uops
per cycle on all execution ports."""
    level = 4
    def compute(self, EV):
        try:
            self.val = EV("UOPS_EXECUTED.CYCLES_GE_3_UOPS_EXEC", 4) / CLKS(EV, 4)
            self.thresh = (self.val > 0.1) and self.parent.thresh
        except ZeroDivisionError:
            print "G3m_Ports zero division"
            self.val = 0
            self.thresh = False
        return self.val

class Retiring:
    name = "Retiring"
    domain = "Slots"
    area = "RET"
    desc = """
This category reflects slots utilized by useful work i. Note that a high
Retiring value does not necessary mean there is no room for more performance.
A high Retiring value for non-vectorized code may be a good hint for
programmer to consider vectorizing his code."""
    level = 1
    def compute(self, EV):
        try:
            self.val = EV("UOPS_RETIRED.RETIRE_SLOTS", 1) / SLOTS(EV, 1)
            self.thresh = (self.val > 0.7)
        except ZeroDivisionError:
            print "Retiring zero division"
            self.val = 0
            self.thresh = False
        return self.val

class BASE:
    name = "BASE"
    domain = "Slots"
    area = "RET"
    desc = """
This metric represents slots fraction CPU was retiring uops not originated
from the microcode-sequencer."""
    level = 2
    def compute(self, EV):
        try:
            self.val = self.Retiring.compute(EV) - self.MicroSequencer.compute(EV)
            self.thresh = (self.val > 0.6) and self.parent.thresh
        except ZeroDivisionError:
            print "BASE zero division"
            self.val = 0
            self.thresh = False
        return self.val

class FP_Arith:
    name = "FP_Arith"
    domain = "Uops"
    area = "RET"
    desc = """
This metric represents overall arithmetic floating-point (FP) uops fraction
the CPU has executed."""
    level = 3
    def compute(self, EV):
        try:
            self.val = self.FP_x87.compute(EV) + self.FP_Scalar.compute(EV) + self.FP_Vector.compute(EV)
            self.thresh = (self.val > 0.2) and self.parent.thresh
        except ZeroDivisionError:
            print "FP_Arith zero division"
            self.val = 0
            self.thresh = False
        return self.val

class FP_x87:
    name = "FP_x87"
    domain = "Uops"
    area = "RET"
    desc = """
This metric represents floating-point (FP) x87 uops fraction the CPU has
executed."""
    level = 4
    def compute(self, EV):
        try:
            self.val = EV("FP_COMP_OPS_EXE.X87", 4) / EV("UOPS_EXECUTED.THREAD", 4)
            self.thresh = (self.val > 0.1) and self.parent.thresh
        except ZeroDivisionError:
            print "FP_x87 zero division"
            self.val = 0
            self.thresh = False
        return self.val

class FP_Scalar:
    name = "FP_Scalar"
    domain = "Uops"
    area = "RET"
    desc = """
This metric represents arithmetic floating-point (FP) scalar uops fraction the
CPU has executed."""
    level = 4
    def compute(self, EV):
        try:
            self.val = ( EV("FP_COMP_OPS_EXE.SSE_SCALAR_SINGLE", 4) + EV("FP_COMP_OPS_EXE.SSE_SCALAR_DOUBLE", 4))/ EV("UOPS_EXECUTED.THREAD", 4)
            self.thresh = (self.val > 0.1) and self.parent.thresh
        except ZeroDivisionError:
            print "FP_Scalar zero division"
            self.val = 0
            self.thresh = False
        return self.val

class FP_Vector:
    name = "FP_Vector"
    domain = "Uops"
    area = "RET"
    desc = """
This metric represents arithmetic floating-point (FP) vector uops fraction the
CPU has executed."""
    level = 4
    def compute(self, EV):
        try:
            self.val = ( EV("FP_COMP_OPS_EXE.SSE_PACKED_DOUBLE", 4) + EV("FP_COMP_OPS_EXE.SSE_PACKED_SINGLE", 4) + EV("SIMD_FP_256.PACKED_SINGLE", 4) + EV("SIMD_FP_256.PACKED_DOUBLE", 4))/ EV("UOPS_EXECUTED.THREAD", 4)
            self.thresh = (self.val > 0.2) and self.parent.thresh
        except ZeroDivisionError:
            print "FP_Vector zero division"
            self.val = 0
            self.thresh = False
        return self.val

class OTHER:
    name = "OTHER"
    domain = "Uops"
    area = "RET"
    desc = """
This metric represents non-floating-point (FP) uop fraction the CPU has
executed."""
    level = 3
    def compute(self, EV):
        try:
            self.val = self.BASE.compute(EV) - self.FP_Arith.compute(EV)
            self.thresh = (self.val > 0.3) and self.parent.thresh
        except ZeroDivisionError:
            print "OTHER zero division"
            self.val = 0
            self.thresh = False
        return self.val

class MicroSequencer:
    name = "MicroSequencer"
    domain = "Slots"
    area = "RET"
    desc = """
This metric represents slots fraction CPU was retiring uops fetched by the
Microcode Sequencer (MS) ROM."""
    level = 2
    def compute(self, EV):
        try:
            self.val = RetireUopFraction(EV, 2) * EV("IDQ.MS_UOPS", 2) / SLOTS(EV, 2)
            self.thresh = (self.val > 0.05)
        except ZeroDivisionError:
            print "MicroSequencer zero division"
            self.val = 0
            self.thresh = False
        return self.val

# Schedule


class Setup:
    def __init__(self, r):
        o = dict()
        n = FrontendBound() ; r.run(n) ; o["FrontendBound"] = n
        n = FrontendLatency() ; r.run(n) ; o["FrontendLatency"] = n
        n = ICacheMisses() ; r.run(n) ; o["ICacheMisses"] = n
        n = ITLBmisses() ; r.run(n) ; o["ITLBmisses"] = n
        n = BranchResteers() ; r.run(n) ; o["BranchResteers"] = n
        n = DSBswitches() ; r.run(n) ; o["DSBswitches"] = n
        n = LCP() ; r.run(n) ; o["LCP"] = n
        n = MSswitches() ; r.run(n) ; o["MSswitches"] = n
        n = FrontendBandwidth() ; r.run(n) ; o["FrontendBandwidth"] = n
        n = MITE() ; r.run(n) ; o["MITE"] = n
        n = DSB() ; r.run(n) ; o["DSB"] = n
        n = LSD() ; r.run(n) ; o["LSD"] = n
        n = BadSpeculation() ; r.run(n) ; o["BadSpeculation"] = n
        n = BranchMispredicts() ; r.run(n) ; o["BranchMispredicts"] = n
        n = MachineClears() ; r.run(n) ; o["MachineClears"] = n
        n = Backend_Bound() ; r.run(n) ; o["Backend_Bound"] = n
        n = MemoryBound() ; r.run(n) ; o["MemoryBound"] = n
        n = L1Bound() ; r.run(n) ; o["L1Bound"] = n
        n = DTLBOverhead() ; r.run(n) ; o["DTLBOverhead"] = n
        n = LoadsBlockedbyStoreForwarding() ; r.run(n) ; o["LoadsBlockedbyStoreForwarding"] = n
        n = SplitLoads() ; r.run(n) ; o["SplitLoads"] = n
        n = G4KAliasing() ; r.run(n) ; o["G4KAliasing"] = n
        n = L2Bound() ; r.run(n) ; o["L2Bound"] = n
        n = L3Bound() ; r.run(n) ; o["L3Bound"] = n
        n = ContestedAccesses() ; r.run(n) ; o["ContestedAccesses"] = n
        n = DataSharing() ; r.run(n) ; o["DataSharing"] = n
        n = L3Latency() ; r.run(n) ; o["L3Latency"] = n
        n = DRAMBound() ; r.run(n) ; o["DRAMBound"] = n
        n = MEMBandwidth() ; r.run(n) ; o["MEMBandwidth"] = n
        n = MEMLatency() ; r.run(n) ; o["MEMLatency"] = n
        n = StoresBound() ; r.run(n) ; o["StoresBound"] = n
        n = FalseSharing() ; r.run(n) ; o["FalseSharing"] = n
        n = SplitStores() ; r.run(n) ; o["SplitStores"] = n
        n = DTLBStoreOverhead() ; r.run(n) ; o["DTLBStoreOverhead"] = n
        n = CoreBound() ; r.run(n) ; o["CoreBound"] = n
        n = DividerActive() ; r.run(n) ; o["DividerActive"] = n
        n = PortsUtilization() ; r.run(n) ; o["PortsUtilization"] = n
        n = G0_Ports() ; r.run(n) ; o["G0_Ports"] = n
        n = G1_Port() ; r.run(n) ; o["G1_Port"] = n
        n = G2_Ports() ; r.run(n) ; o["G2_Ports"] = n
        n = G3m_Ports() ; r.run(n) ; o["G3m_Ports"] = n
        n = Retiring() ; r.run(n) ; o["Retiring"] = n
        n = BASE() ; r.run(n) ; o["BASE"] = n
        n = FP_Arith() ; r.run(n) ; o["FP_Arith"] = n
        n = FP_x87() ; r.run(n) ; o["FP_x87"] = n
        n = FP_Scalar() ; r.run(n) ; o["FP_Scalar"] = n
        n = FP_Vector() ; r.run(n) ; o["FP_Vector"] = n
        n = OTHER() ; r.run(n) ; o["OTHER"] = n
        n = MicroSequencer() ; r.run(n) ; o["MicroSequencer"] = n

        # parents
        o["FrontendLatency"].parent = o["FrontendBound"]
        o["ICacheMisses"].parent = o["FrontendLatency"]
        o["ITLBmisses"].parent = o["FrontendLatency"]
        o["BranchResteers"].parent = o["FrontendLatency"]
        o["DSBswitches"].parent = o["FrontendLatency"]
        o["LCP"].parent = o["FrontendLatency"]
        o["MSswitches"].parent = o["FrontendLatency"]
        o["FrontendBandwidth"].parent = o["FrontendBound"]
        o["MITE"].parent = o["FrontendBandwidth"]
        o["DSB"].parent = o["FrontendBandwidth"]
        o["LSD"].parent = o["FrontendBandwidth"]
        o["BranchMispredicts"].parent = o["BadSpeculation"]
        o["MachineClears"].parent = o["BadSpeculation"]
        o["MemoryBound"].parent = o["Backend_Bound"]
        o["L1Bound"].parent = o["MemoryBound"]
        o["DTLBOverhead"].parent = o["L1Bound"]
        o["LoadsBlockedbyStoreForwarding"].parent = o["L1Bound"]
        o["SplitLoads"].parent = o["L1Bound"]
        o["G4KAliasing"].parent = o["L1Bound"]
        o["L2Bound"].parent = o["MemoryBound"]
        o["L3Bound"].parent = o["MemoryBound"]
        o["ContestedAccesses"].parent = o["L3Bound"]
        o["DataSharing"].parent = o["L3Bound"]
        o["L3Latency"].parent = o["L3Bound"]
        o["DRAMBound"].parent = o["MemoryBound"]
        o["MEMBandwidth"].parent = o["DRAMBound"]
        o["MEMLatency"].parent = o["DRAMBound"]
        o["StoresBound"].parent = o["MemoryBound"]
        o["FalseSharing"].parent = o["StoresBound"]
        o["SplitStores"].parent = o["StoresBound"]
        o["DTLBStoreOverhead"].parent = o["StoresBound"]
        o["CoreBound"].parent = o["Backend_Bound"]
        o["DividerActive"].parent = o["CoreBound"]
        o["PortsUtilization"].parent = o["CoreBound"]
        o["G0_Ports"].parent = o["PortsUtilization"]
        o["G1_Port"].parent = o["PortsUtilization"]
        o["G2_Ports"].parent = o["PortsUtilization"]
        o["G3m_Ports"].parent = o["PortsUtilization"]
        o["BASE"].parent = o["Retiring"]
        o["FP_Arith"].parent = o["BASE"]
        o["FP_x87"].parent = o["FP_Arith"]
        o["FP_Scalar"].parent = o["FP_Arith"]
        o["FP_Vector"].parent = o["FP_Arith"]
        o["OTHER"].parent = o["BASE"]
        o["MicroSequencer"].parent = o["Retiring"]

        # references between groups

        o["FrontendBandwidth"].FrontendBound = o["FrontendBound"]
        o["FrontendBandwidth"].FrontendLatency = o["FrontendLatency"]
        o["BranchMispredicts"].BadSpeculation = o["BadSpeculation"]
        o["MachineClears"].BadSpeculation = o["BadSpeculation"]
        o["MachineClears"].BranchMispredicts = o["BranchMispredicts"]
        o["Backend_Bound"].FrontendBound = o["FrontendBound"]
        o["Backend_Bound"].BadSpeculation = o["BadSpeculation"]
        o["Backend_Bound"].Retiring = o["Retiring"]
        o["StoresBound"].MemoryBound = o["MemoryBound"]
        o["CoreBound"].MemoryBound = o["MemoryBound"]
        o["PortsUtilization"].CoreBound = o["CoreBound"]
        o["PortsUtilization"].DividerActive = o["DividerActive"]
        o["BASE"].Retiring = o["Retiring"]
        o["BASE"].MicroSequencer = o["MicroSequencer"]
        o["FP_Arith"].FP_x87 = o["FP_x87"]
        o["FP_Arith"].FP_Scalar = o["FP_Scalar"]
        o["FP_Arith"].FP_Vector = o["FP_Vector"]
        o["OTHER"].BASE = o["BASE"]
        o["OTHER"].FP_Arith = o["FP_Arith"]
