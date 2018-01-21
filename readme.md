# Fanuc DPM Mouse Demo

## Overview

This is a simple demo that shows how to use Fanuc *Dynamic Path Modification*
in Modal mode with Stationary Tracking inputting offsets via system variables
to control the end-effector in 3D (XYZ) with mouse inputs from a remote
system.

![example](https://user-images.githubusercontent.com/4550046/35197068-e7acf79c-feda-11e7-834a-964029e318e5.gif)


## NOTICE

**This is just a demo** and solely meant to show one possible way to interface
with DPM over a TCP socket. It has only been tested running in Roboguide, and
the code as-is is absolutely **not** intended to be suitable for any kind of
production use (it lacks proper error handling and recovery, for instance).

Always adhere to safety regulations and make sure you, other people, your
robot and your workcell are safe. Refer to the safety instructions found in
all Fanuc manuals for information on safety when working with Fanuc robots
and controllers.


## tl;dr

Copy Karel and TP programs to a controller with DPM, check flags used,
configure DPM schedule 1, channels 1, 2 and 3 for stationary tracking with
path offset set to maximum and `SYSVAR` input type. Update *KAREL Vars* of
`FDPM_MDEMO` to match TP and Python program. Check that positions configured
in TP program work for the used robot.
Start TP program, start `fdpm_mdemo.py` on PC, use mouse to control EEF.

See *Requirements* section for info on required options and runtimes.


## Requirements

The following is needed for this demo to work:

 - R-30iB controller (`V8.xx` and up), with:
   - `R739` - Dyn Path Modifier
   - `R648` - User Socket Msg (`R636` is not enough unfortunately)
 - Roboguide
 - Python 2 with PyGame installed (`pip install pygame`)

The Python part should work under Linux and OSX as well, as long as PyGame is
installed. This hasn't been tested though. Python 3 has also not been tested.

Karel (`R632`) is probably not needed, as long as `$KAREL_ENB` is set to `1`.


## Build

### Command line

If `ktrans.exe` is not installed in the default location (ie:
`C:\Program Files (x86)\Fanuc\WinOLPC\bin`),
open `build.cmd` and update the `KTRANS_BIN` variable. If `ktrans.exe` is on
the Windows `PATH`, simply setting it to `ktrans.exe` should also work.

If you need to build for a runtime software version other than `V8.30`,
change `CORE_VERSION` as well.

Now run `build.cmd` in a command shell. Three p-code files should have been
produced.

### Roboguide

Add the three Karel programs and the single TP program to your Roboguide
workcell and build them.


## Installation

Roboguide should have automatically uploaded the Karel programs to the virtual
controller. Loading the TP program should copy it as well.

If `build.cmd` was used, add the `.pc` and `.ls` files to the project and
load them onto the virtual controller. Alternatively an FTP client could be
used.


## Configuration

### DPM

This demo uses Modal DPM with Stationary Tracking and `SYSVAR` channels and
assumes that the first DPM schedule has been set up for that.

Global DPM configuration used for this demo:

```
DPM function:              ENABLED
Instruction type:          MODAL
Offset BEF/AFT filter:     AFTER
Orientation CTRL:          DISABLED
Delay time (inline DPM):   5 ITP
Motion group mask:         [1,*,*,*,*,*,*,*]
```

Schedule 1, channel 1, 2 and 3 configuration:

```
DPM type:               MODAL
Offset ref. frame:      UTOOL
Offset accumulate:      FALSE
Stationary track:       YES
Stationary track sych:  DI[1]
Channel enabled:        TRUE
On-The-Fly Input:       DI[0]
Max offset/path:        100.00 mm
Max offset/ITP:         50.00 mm
Min offset/ITP:         0.00 mm
Channel input type:     SYSVAR
Offset value:           0.00 mm
```

Make sure the schedule is also `ENABLED`.

Note that `Stationary track sych` *must be set to a DI index*, or DPM
Stationary tracking will not work (`Stationary track sych` is used as
a termination condition: if `DI[1]` is `ON`, tracking will terminate).
For this demo, it's set to `DI[1]`, but make sure to set this to an
unconnected and unused DI.

Refer to the Fanuc *Dynamic Path Modification User's Guide* (`MARUBDPMO02141E`)
for more information on how to setup DPM.

### Host Comm

Setup a *Server Tag* to use the `SM` protocol and make sure to set
`Startup State` to `START`. Use the `[ACTION]` menu to start the Tag
immediately, or restart the controller.

Note the Tag index.

### FDPM_MDEMO

Open the *KAREL Vars* for `FDPM_MDEMO`, switch to the `cfg_` field, open the
structure and enter the following values:

```
F_TP_READY   : 1
F_KRL_READY  : 2
S_TCP_PORT   : 11010
S_TAG_NR     : <SERVER_TAG>
UM_CLEAR     : TRUE
```

Where `SERVER_TAG` is the index of the Server Tag configured earlier.

Note: make sure the values for `F_TP_READY` and `F_KRL_READY` correspond to
the values used in `STATRACKX` (see below).

### STATRACKX

Three things need configuration here: initial pose, DPM starting position and
the flags used for handshaking with `FDPM_MDEMO`.

#### DPM starting position

This is the pose that `STATRACKX` starts stationary tracking from. This pose
can be anything, but is recommended to be in a neutral position for the used
robot. For an LR Mate 200iD, the author used the Cartesian pose that results
from having all joint angles at 0, except `J5` which was at `90` degrees.

This pose is stored as `P[2]` in `STATRACKX`.

#### Initial position

As DPM does not permit stationary tracking to be started with moves that
would result in *zero motion*, this pose should have a slight offset from
the starting position that was configured in the previous section. The
author used `P[2]`, but in `JOINT` representation, and offset each angle
by `1` degree.

This pose is stored as `P[1]` in `STATRACKX`.

#### Flags

Two flags are used by `STATRACKX` to communicate with `FDPM_MDEMO`. By default
these are flags 1 and 2. Make sure these are free to use.

If other flags should be used, update them in `STATRACKX` and be sure to
update `FDPM_MDEMO`'s configuration to match.


## Running the demo

To run the demo, start the `STATRACKX` TP program using the teach pendant. If
all goes well, the teach pendant should show:

```
12345 I FDMD init done
12345 I FDMD wait TP
12345 I FDMD TP is ready
12345 I FDMD wait client
```

On the PC, start `fdpm_mdemo.py` in a command session. A black window should
appear, and the console should show:

```
Connected, move mouse to control EEF.
Left mouse button : X-Y
Right mouse button: Z
```

The teach pendant should now show:

```
...
12345 I FDMD connected
12345 I FDMD ready for mouse input
```

On the PC, click inside the black window and drag the mouse while holding
down the mouse button . A left click will control EEF translation in the
X and Y directions. A right click controls EEF translation in Z.
