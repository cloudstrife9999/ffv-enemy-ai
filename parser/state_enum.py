from enum import Enum


class StateEnum(Enum):
    '''
    Initial state: START
    Final state: TER2
    Error sink state: ERROR
    '''
    START = "Start"
    C1 = "Read non-default condition first byte"
    C2 = "Read non-default condition second byte"
    C3 = "Read non-default condition third byte"
    C4 = "Read non-default condition fourth byte"
    SEP1 = "Read separator byte after C4 state"
    SA = "Read simple action byte"
    CA1 = "Read complex action first byte"
    CA2 = "Read complex action second byte"
    CA3 = "Read complex action third byte"
    CA4 = "Read complex action fourth byte"
    SEP2 = "Read separator byte after SA/CA4 state"
    DC1 = "Read default condition first byte"
    DC2 = "Read default condition second byte"
    DC3 = "Read default condition third byte"
    DC4 = "Read default condition fourth byte"
    SEP3 = "Read separator byte after DC4 state"
    SDA = "Read simple default action byte"
    CDA1 = "Read complex default action first byte"
    CDA2 = "Read complex default action second byte"
    CDA3 = "Read complex default action third byte"
    CDA4 = "Read complex default action fourth byte"
    TER1 = "Read active AI terminator byte"
    RC1 = "Read reactive condition first byte"
    RC2 = "Read reactive condition second byte"
    RC3 = "Read reactive condition third byte"
    RC4 = "Read reactive condition fourth byte"
    SEP4 = "Read separator byte after RC4 state"
    RSA = "Read reactive simple action byte"
    RCA1 = "Read reactive complex action first byte"
    RCA2 = "Read reactive complex action second byte"
    RCA3 = "Read reactive complex action third byte"
    RCA4 = "Read reactive complex action fourth byte"
    SEP5 = "Read separator byte after RSA/RCA4 state"
    TER2 = "Read reactive AI terminator byte"
    ERROR = "Error state"
