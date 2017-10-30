
import numpy as np
import math

# LTE CHANNEL MODELS ##################################################################################################
# AWGN
AWGN = np.array([1/math.sqrt(2)+1j/math.sqrt(2)])
# EPA
EPA = np.zeros(411, dtype=complex)
EPA[0] = 10**((0.0)/(20))/math.sqrt(2) * (1+1j)
EPA[30] = 10**((-1.0)/(20))/math.sqrt(2) * (1+1j)
EPA[70] = 10**((-2.0)/(20))/math.sqrt(2) * (1+1j)
EPA[90] = 10**((-3.0)/(20))/math.sqrt(2) * (1+1j)
EPA[110] = 10**((-8.0)/(20))/math.sqrt(2) * (1+1j)
EPA[190] = 10**((-17.2)/(20))/math.sqrt(2) * (1+1j)
EPA[410] = 10**((-20.8)/(20))/math.sqrt(2) * (1+1j)
# EPA with new sampling rate
EPA_samp = np.array([10**((0.0)/(20))/math.sqrt(2) * (1+1j),
                     10**((-20.8)/(20))/math.sqrt(2) * (1+1j)])

# EVA
EVA = np.zeros(2511, dtype=complex)
EVA[0] = 10**((0)/(20))/math.sqrt(2) * (1+1j)
EVA[30] = 10**((-1.5)/(20))/math.sqrt(2) * (1+1j)
EVA[150] = 10**((-1.4)/(20))/math.sqrt(2) * (1+1j)
EVA[310] = 10**((-3.6)/(20))/math.sqrt(2) * (1+1j)
EVA[370] = 10**((-0.6)/(20))/math.sqrt(2) * (1+1j)
EVA[710] = 10**((-9.1)/(20))/math.sqrt(2) * (1+1j)
EVA[1090] = 10**((-7.0)/(20))/math.sqrt(2) * (1+1j)
EVA[1730] = 10**((-12.0)/(20))/math.sqrt(2) * (1+1j)
EVA[2510] = 10**((-16.9)/(20))/math.sqrt(2) * (1+1j)
# EVA with new sampling rate
EVA_samp = np.array([10**((0.0)/(20))/math.sqrt(2) * (1+1j),
                     10**((-0.6)/(20))/math.sqrt(2) * (1+1j),
                     10**((-7.0)/(20))/math.sqrt(2) * (1+1j),
                     10**((-12.0)/(20))/math.sqrt(2) * (1+1j),
                     10**((-16.9)/(20))/math.sqrt(2) * (1+1j)])

# ETU
ETU = np.zeros(5001, dtype=complex)
ETU[0] = 10**((-1.0)/(20))/math.sqrt(2) * (1+1j)
ETU[50] = 10**((-1.0)/(20))/math.sqrt(2) * (1+1j)
ETU[120] = 10**((-1.0)/(20))/math.sqrt(2) * (1+1j)
ETU[200] = 10**((-0.0)/(20))/math.sqrt(2) * (1+1j)
ETU[230] = 10**((-0.0)/(20))/math.sqrt(2) * (1+1j)
ETU[500] = 10**((-0.0)/(20))/math.sqrt(2) * (1+1j)
ETU[1600] = 10**((-3.0)/(20))/math.sqrt(2) * (1+1j)
ETU[2300] = 10**((-5.0)/(20))/math.sqrt(2) * (1+1j)
ETU[5000] = 10**((-7.0)/(20))/math.sqrt(2) * (1+1j)
# ETU with new sampling rate
ETU_samp = np.array([10**((-1.0)/(20))/math.sqrt(2) * (1+1j),
                     10**((-0.0)/(20))/math.sqrt(2) * (1+1j),
                     0 * (1+1j),
                     10**((-3.0)/(20))/math.sqrt(2) * (1+1j),
                     0 * (1+1j),
                     10**((-5.0)/(20))/math.sqrt(2) * (1+1j),
                     0 * (1+1j),
                     0 * (1+1j),
                     0 * (1+1j),
                     0 * (1+1j),
                     10**((-7.0)/(20))/math.sqrt(2) * (1+1j)])