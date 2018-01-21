#!/usr/bin/env python

# Copyright (c) 2018, G.A. vd. Hoorn
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


#
# NOTICE: THIS IS A DEMO, AND NOT MEANT FOR ANY KIND OF PRODUCTION USE.
#         THIS PROGRAM LACKS ANY AND ALL ERROR CHECKING AND HANDLING.
#         USAGE OTHER THAN WITH ROBOGUIDE IS COMPLETELY UNTESTED.
#         THE AUTHOR DENIES ANY RESPONSIBILITY FOR DAMAGE DONE TO
#         ROBOTS, CONTROLLERS, OTHER EQUIPMENT OR PEOPLE THAT IS THE
#         RESULT OF IGNORING THE PREVIOUS WARNING.
#         REFER ALSO TO THE APACHE 2.0 LICENSE INCLUDED WITH THIS SOFTWARE.
#


import pygame
import struct
import socket
import time


controller_ip = '127.0.0.1'
tcp_port = 11010

# makes motions a bit more intuitive if looking at robot 'from the side'
mirror_y = True


# nothing to change below this line


IDX_X=0
IDX_Y=1

MOUSE_LEFT = 1
MOUSE_RIGHT = 3

M_NONE = 0
M_Z = 1
M_XY = 2


running = True
m_dir = M_NONE
mult_y = -1 if not mirror_y else 1


# open socket to controller
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((controller_ip, tcp_port))

print ("Connected, move mouse to control EEF.")
print ("Left mouse button : X-Y")
print ("Right mouse button: Z")

screen = pygame.display.set_mode((320, 240))

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            m_dir = M_NONE
            running = 0
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == MOUSE_LEFT:
                m_dir = M_XY
                pygame.event.set_grab(True)
                print ("EEF: grabbed X-Y")
            elif event.button == MOUSE_RIGHT:
                m_dir = M_Z
                pygame.event.set_grab(True)
                print ("EEF: grabbed Z")
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button in [MOUSE_LEFT, MOUSE_RIGHT]:
                m_dir = M_NONE
                pygame.event.set_grab(False)
                print ("EEF: released")
        elif event.type == pygame.MOUSEMOTION:
            if pygame.event.get_grab():
                if m_dir == M_XY:
                    data = struct.pack('<3f', event.rel[IDX_X], mult_y * event.rel[IDX_Y], 0.0)
                    s.send(data)
                elif m_dir == M_Z:
                    data = struct.pack('<3f', 0.0, 0.0, event.rel[IDX_Y])
                    s.send(data)

    time.sleep(0.01)

    screen.fill((0, 0, 0))
    pygame.display.flip()

print ("Disconnecting ..")
