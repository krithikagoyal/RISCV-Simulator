from stageFunctions import State


class HDU:

        code here



    def __init__(self):
        self.E2E=0#data in EtoE data line.
        self.M2E=0
        self.M2M=0
        self.E2D=0
        self.M2D=0
    
    
    def check_data_hazard(self,states):
        forwarding_paths = set()
        # forwarding_paths.add("X->X")
        new_states = []     # updated states
        new_states = [states[0]]
        toDecode = states[1]
        toExecute = states[2]
        toMem = states[3]
        toWB = states[4]
        isHazard = False    # is there a data hazard?
        doStall = False     # do we need to stall in case of data forwarding?
        stallWhere = 3      # stall at the decode stage or execute stage?
                            # 1 = at execute, 2 = at decode, 3 = don't stall
                            # Sorted according to priority

        toDecode_opcode = toDecode.instruction_word & (0x7F)
        toExecute_opcode = toExecute.instruction_word & (0x7F)
        toMem_opcode = toMem.instruction_word & (0x7F)
        toWB_opcode = toWB.instruction_word & (0x7F)

        # M->E and M->M forwarding before E->E forwarding, because E->E forward takes  
        # precedence over the other two, and should have the capacity to overwrite

        
        # if toWB_opcode==3  and toMem_opcode==35:
        # load-toWB and store-toMem instructions
        # state function use these variables.
        # rs1,rs2,rd -global declare

        # register_data=WB_data;
        # RA=operand1
        # RB=operand2
        # final address in memory=memory_address.
        # M->M forwarding
        if (toWB_opcode==3) and (toMem_opcode==35):
            if toWB.rd > 0 and toWB.rd == toMem.rs2:
                toMem.register_data = toWB.register_data
                isHazard = True
                self.M2M=toWB.register_data
                forwarding_paths.add("M->M")


        # M->E forwarding
        if toWB.rd > 0:
            if toWB.rd == toExecute.rs1:
                toExecute.operand1 = toWB.register_data
                self.M2E=toWB.register_data
                isHazard = True
                forwarding_paths.add("M->E")

            if toWB.rd == toExecute.rs2:
                toExecute.operand2 = toWB.register_data
                self.M2E=toWB.register_data
                isHazard = True
                forwarding_paths.add("M->E")
        
        # E->E forwarding
        if toMem.rd > 0:

            # If the producer is a load instruction
            # if toMem_opcode == 3 or toMem_opcode == 55:
            if toMem_opcode == 3:

                # If the consumer is a store instruction
                if toExecute_opcode == 35:

                    # Stall required for address calculation of store instruction
                    if toExecute.rs1 == toMem.rs2:
                        isHazard = True
                        doStall = True
                        stallWhere = min(stallWhere, 1)
                    
                # If the consumer isn't a store instruction, then we need a stall 
                else:
                    isHazard = True
                    doStall = True
                    stallWhere = min(stallWhere, 1)

            # If the producer isn't a load instruction then  E->E data forwarding can be performed
            else:
                if toExecute.rs1 == toMem.rs2:
                    toExecute.operand1 = toMem.register_data
                    self.E2E=toMem.register_data
                    isHazard = True
                    forwarding_paths.add("E->E")

                if toExecute.rs2 == toMem.rs2:
                    toExecute.operand2 = toMem.register_data
                    self.E2E=toMem.register_data
                    isHazard = True
                    forwarding_paths.add("E->E")

        
        new_states = new_states + [toDecode, toExecute, toMem, toWB]
        return [isHazard, doStall, new_states, stallWhere, forwarding_paths]

    
    
    def check_data_hazard_stalling(self,states):
        states=states[1:] #removed the fetch stage instruction
        if len(states)==1:
            return [False,-1]
        elif len(states)>=2:
            exe_state=states[1]
            decode_state=states[0]
            if exe_state.rd!=-1 and decode_state.rs1!=-1:
                if exe_state.rd==decode_state.rs1 :
                    if exe_state.rd!=0:
                        # self.count_data_hazards+=1
                        return [True,2]
                if exe_state.rd==decode_state.rs2:
                    if exe_state.rd!=0:
                        # self.count_data_hazards+=1
                        return [True,2]
            if len(states)>=3:
                mem_state=states[2]
                if mem_state.rd!=-1 and decode_state.rs1!=-1:
                    if mem_state.rd==decode_state.rs1 :
                        if mem_state.rd!=0:
                            # self.count_data_hazards+=1
                            return [True,1]
                    if mem_state.rd==decode_state.rs2:
                        if mem_state.rd!=0:
                            # self.count_data_hazards+=1
                            return [True,1]
        
        return [False,-1]
