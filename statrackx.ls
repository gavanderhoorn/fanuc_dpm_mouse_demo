/PROG  STATRACKX
/ATTR
OWNER   = MNEDITOR;
COMMENT   = "FDPMMD//r0b";
PROG_SIZE = 1050;
CREATE    = DATE 18-01-21  TIME 12:00:00;
MODIFIED  = DATE 18-01-21  TIME 12:00:00;
FILE_NAME = ;
VERSION   = 0;
LINE_COUNT  = 30;
MEMORY_SIZE = 1310;
PROTECT   = READ_WRITE;
TCD:  STACK_SIZE  = 0,
      TASK_PRIORITY = 50,
      TIME_SLICE  = 0,
      BUSY_LAMP_OFF = 0,
      ABORT_REQUEST = 0,
      PAUSE_REQUEST = 0;
DEFAULT_GROUP = 1,*,*,*,*;
CONTROL_CODE  = 00000000 00000000;
/MN
    :  !if your robot needs ;
    :  !a specific toolframe ;
    :  !selected, add it here ;
    :   ;
    :  !Init handshaking: ;
    :  !  TP not ready ;
    :  !  Karel not ready ;
    :  F[1]=(OFF) ;
    :  F[2]=(OFF) ;
    :   ;
    :  !Slowly go to initial ;
    :  !position ;
    :J P[1] 10% FINE    ;
    :   ;
    :  !Start karel program ;
    :  RUN FDPM_MDEMO ;
    :   ;
    :  !Handshake: ;
    :  !  TP is ready ;
    :  F[1]=(ON) ;
    :  !  Karel ready ? ;
    :  WAIT (F[2]=ON)    ;
    :   ;
    :  !Start stat tracking ;
    :  Track DPM[1] ;
    :L P[2] 100mm/sec FINE    ;
    :   ;
    :  !Stop tracking ;
    :  !(will never reach this) ;
    :  Track End ;
/POS
P[1]{
   GP1:
  UF : 1, UT : 1, 
  J1=     1.000 deg,  J2=     1.000 deg,  J3=     1.000 deg,
  J4=     1.000 deg,  J5=   -89.000 deg,  J6=     1.000 deg
};
P[2]{
   GP1:
  UF : 1, UT : 1,   CONFIG : 'N U T, 0, 0, 0',
  X =   385.000  mm,  Y =     0.000  mm,  Z =   285.000  mm,
  W =  -180.000 deg,  P =      .000 deg,  R =     0.000 deg
};
/END
