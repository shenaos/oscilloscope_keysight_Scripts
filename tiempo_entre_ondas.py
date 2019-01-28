#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 28 16:48:35 2019

@author: labfluidos
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import hilbert


T = 0.01
Ts = T/100
Nc = 20
offset = 1000

t = np.arange(0,Nc*T, Ts)
y1 = np.sin(2*np.pi*(t/T))
y2 = np.exp(-((t-5*T)**2)/0.0001)
y2 = y1*y2
y3 = 0.5*np.exp(-((t-15*T)**2)/0.0001)
y3 = y1*y3
y  = y2 + y3

analytic = hilbert(y)
envelope = np.abs(analytic)


ts1 = np.argmax(envelope[0:offset]) * Ts
ts2 = (offset + np.argmax(envelope[offset:2*offset-1])) * Ts

plt.plot(t, -y,t, envelope)
#plt.plot(t, y)
plt.show()


