#!/usr/bin/env python3

# Copyright (c) 2019, Alchemy Meister
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#     * Redistributions of source code must retain the above copyright notice,
#       this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice,this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * Neither the name of the copyright holder nor the names of its
#       contributors may be used to endorse or promote products derived from
#       this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

"""
Wrapper for dwmapi.dll in ctypes.
"""

# pylint: disable=unused-wildcard-import,wildcard-import
import ctypes
from .defines import *  # NOQA

S_OK = 0

DWMWA_EXTENDED_FRAME_BOUNDS = 9

def dwm_get_window_attribute(h_wnd, dw_attribute, pv_attribute, cb_attribute):
    # DWMAPI DwmGetWindowAttribute(
    #   HWND  hwnd,
    #   DWORD dwAttribute,
    #   PVOID pvAttribute,
    #   DWORD cbAttribute
    # );
    _dwm_get_window_attribute = WINDLL.dwmapi.DwmGetWindowAttribute
    _dwm_get_window_attribute.argtypes = [HWND, DWORD, PVOID, DWORD]
    _dwm_get_window_attribute.restype = ctypes.c_int

    return _dwm_get_window_attribute(
        h_wnd, dw_attribute, pv_attribute, cb_attribute
    )
