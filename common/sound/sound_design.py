"""
Equation of wave: 
v = f * λ
velocity (m/s) equals the product of frequency (Hz) and wave length(m)

posição na onda:
y = A sin(teta * t - k * x + Φ)
position y equals to product of amplitude and sin of the product of ω and time minus the product of angular wave number and horizontal position plus the phase.

A frequência é o tempo que a onda demora para fazer uma crista e um vale
O tamanho da onda no eixo X é a distância de uma crista a outra
O tamanho da onda no eixo y é a amplitude
"""

# import sys
# import wave
# import math
# import struct
# import random
# import argparse
# from itertools import *

# def sine_wave(frequency, framerate, amplitude):
#     if amplitude > 1.0: amplitude = 1.0
#     if amplitude < 0.0: amplitude = 0.0
#     y = amplitude * math.sin(frequency*(i/framerate) for i in count(0))


# import numpy as np
# from numpy import pi
# import matplotlib.pyplot as plt
# import matplotlib.animation as animation

# plt.style.use('dark_background')

# fig = plt.figure()
# fig.set_dpi(100)
# ax1 = fig.add_subplot(1,1,1)

# #Wave speed
# c = 1

# #x axis
# x0 = np.linspace(-pi,pi,10000)

# #Initial time
# t0 = 0

# #Time increment
# dt = 0.05

# #Wave equation solution
# def u(x,t):
#     return 0.5*(np.sin(x+c*t) + np.sin(x-c*t))

# a = []

# for i in range(500):
#     value = u(x0,t0)
#     t0 = t0 + dt
#     a.append(value)

# k = 0
# def animate(i):
#     global k
#     x = a[k]
#     k += 1
#     ax1.clear()
#     plt.plot(x0,x,color='cyan')
#     plt.grid(True)
#     plt.ylim([-2,2])
#     plt.xlim([-pi,pi])
    
# anim = animation.FuncAnimation(fig,animate,frames=60,interval=20)
# plt.show()

# https://zach.se/generate-audio-with-python/