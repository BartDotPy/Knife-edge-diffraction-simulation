import settings
import pygame
import math

def calculate_diffraction(tx,rx, obs, freq):
    #wave length
    wave_l = settings.c / freq

    #distances
    d1 = abs(obs.x - tx.x)
    d2 = abs(rx.x - obs.x)
    d_total = d1 + d2

    s1_and_s2 = math.sqrt((abs(rx.h - tx.h))**2 + d_total**2)


    diff_h1 = abs(obs.h - tx.h)
    r1 = math.sqrt(diff_h1**2 + d1**2)

    diff_h2 = abs(rx.h - obs.h)
    r2 = math.sqrt(diff_h2**2 + d2**2)

    #heron's formula to get h
    half_of_perimeter = (r1+r2+s1_and_s2)/2
    area = math.sqrt(half_of_perimeter*(half_of_perimeter-r1)*(half_of_perimeter-r2)*(half_of_perimeter-s1_and_s2))
    #area = (a*h)/2
    h_magnitude = (area * 2)/s1_and_s2

    
    

    #need to check, that obstacle is higher than our LOS line
    slope = (rx.h - tx.h) / d_total
    los_height_at_obs = tx.h + slope * d1

    if obs.h > los_height_at_obs:
        h = h_magnitude
    else:
        h = -h_magnitude

    try:
        # Używamy s_los jako s1+s2
        v = h*math.sqrt(2/wave_l * (s1_and_s2/(r1*r2)))
    except (ValueError, ZeroDivisionError):
        v = 0

    diffraction_loss = 0
    if v > -0.7:
        diffraction_loss = 6.9 + 20 * math.log10(math.sqrt((v-0.1)**2+1) + v - 0.1)
    
    if diffraction_loss < 0: diffraction_loss = 0

    return diffraction_loss, v, h, los_height_at_obs

