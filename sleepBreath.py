import heartpy as hp
import matplotlib.pyplot as plt
from scipy.signal import butter, lfilter
from scipy.signal import find_peaks
import numpy as np

data1 = hp.get_data('data/MuseData/finalFilteredPPG.csv', column_name='ppg_1')
data2 = hp.get_data('data/MuseData/finalFilteredPPG.csv', column_name='ppg_2')
data3 = hp.get_data('data/MuseData/finalFilteredPPG.csv', column_name='ppg_3')

# data1 = hp.get_data('data/MuseData/outputBreathFinal.csv', column_name='ppg_1')
# data2 = hp.get_data('data/MuseData/outputBreathFinal.csv', column_name='ppg_2')
# data3 = hp.get_data('data/MuseData/outputBreathFinal.csv', column_name='ppg_3')

# data = hp.get_data('data/bidmc_01_Signals.csv', column_name='V')

def fixData(fix):
    fixed = np.asarray(fix)
    mean = np.mean(fixed)
    return np.subtract(fixed, mean)

data_1 = fixData(data1)
data_2 = fixData(data2)
data_3 = fixData(data3)

def butter_bandpass(lowcut, highcut, fs, order=5):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    return b, a


def butter_bandpass_filter(data, lowcut, highcut, fs, order=5):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = lfilter(b, a, data)
    return y

print(len(data1))
# for i in range(6):
# print("order: ", i)
y = butter_bandpass_filter(data_2, .01, .2, 64, order=3)

# getting breath
peaks, _ = find_peaks(y, distance=150)
plt.plot(peaks, y[peaks], "x")
# end breath

yb = butter_bandpass_filter(data_2, 1, 5, 64, order=6)
plt.plot(np.arange(len(data1)), y, label='Filtered signal breath')
plt.plot(np.arange(len(data1)), yb, label='Filtered signal heart')
# plt.plot(np.arange(len(data1)), data_1, label='Noisy signal 1')
plt.plot(np.arange(len(data1)), data_2, label='Noisy signal 2')
# plt.plot(np.arange(len(data1)), data_3, label='Noisy signal 3')
plt.ylabel('some numbers')
plt.legend(loc='upper left')

plt.show()

print("Heart Rate:")
working_data, measures = hp.process(yb, 64)


print(working_data)

hp.plotter(working_data, measures)

