from scipy.io.wavfile import read, write
from scipy.fftpack import fft, fftfreq, ifft
from scipy.signal import butter, resample, filtfilt
import matplotlib.pyplot as mplt
import numpy as np

'''
Integrantes:
    - Cristhofer Parada
    - Jose toro
Profesor:
    - Alejandro Catalan Monsalve
Ayudante:
    - Miguel Salinas Gonzalez

'''


'''
Input: String x Variable x Variable x String x String
Output: Void
Description: Allows to plot as spectrogram using the input given
'''

def graph_spectrogram(title, x, y, label_x, label_y):
    mplt.figure(title)
    mplt.specgram(x, Fs=y)
    mplt.title(title)
    mplt.xlabel(label_x)
    mplt.ylabel(label_y)
    mplt.show()


'''
Input: String x String x Varible x Variable x String x String
Output: Void
Description: Allows to plot as spectrogram using the input given
'''
def graph(title, color, x, y, label_x, label_y):
    mplt.figure(title)
    mplt.plot(x, y, color)
    mplt.title(title)
    mplt.xlabel(label_x)
    mplt.ylabel(label_y)
    mplt.show()


'''
Input: list x list
Output: list
Description: adds each element of signal1 with it's corresponding elements of signal2
'''


def sum_signals(signal1, signal2):
    new_signal = np.zeros(len(signal2))
    for i in range(0, len(signal2)):
        new_signal[i] = signal1[i] + signal2[i]
    return new_signal


'''
Input: String
Output: list
Description: Read a file and save it
'''


def read_file(name):
    frequency, signal = read(name)
    try:
        r = signal[0][1]
        r = []
        for i in range(0, len(signal)):
            r.append(signal[i][0])
        return [frequency, r]
    except "Single channel audio":
        return [frequency, signal]


# 1 crear los audios "jose toro.wav" y "cristhofer_parada.wav"
# 2 Lea las señales de audio generadas y determine a qué corresponde cada uno de los parámetros retornados.

readA = read_file("cristhofer_parada.wav")  # signalA for cristhofer
readB = read_file("jose_toro.wav")  # signalB for jose

frequencyA = readA[0]
signalA = readA[1]
frequencyB = readB[0]
signalB = readB[1]

'''
The audio signals generated by the read function are two,
1. the sampling rate,
2. Array of ints, representing the signal.
'''
# 3 Grafique las señales de audio en el tiempo
time_str = "Tiempo [s]"
amplitude_str = "Amplitud [dB]"
frequency_str = "Frecuencia [Hz]"
# the amplitude and the duration are calculated.
amplitudeA = len(signalA)
durationA = amplitudeA / frequencyA  # d = A/f
timeA = np.linspace(0, durationA, amplitudeA)
graph("Audio 1: Cristhofer Parada", "red", timeA, signalA, time_str, amplitude_str)

# the same steps are repeated for the next .wav file
amplitudeB = len(signalB)
durationB = amplitudeB / frequencyB  # d = A/f
timeB = np.linspace(0, durationB, amplitudeB)
graph("Audio 1: Jose Toro", "blue", timeB, signalB, time_str, amplitude_str)

# 4 Calcule la transformada de Fourier de las señales de audio:

# fft and fftfreq from scipy library are used to calculate fourier derivative, and it's frequency
# for both signals
fourierA = fft(signalA)
frequencyFourierA = fftfreq(amplitudeA)

fourierB = fft(signalB)
frequencyFourierB = fftfreq(amplitudeB)

# a. Grafique la señal en el dominio de la frecuencia.

str1 = "Transformada de fourier para el audio 1: Cristhofer Parada"
graph(str1, "red", frequencyFourierA, abs(fourierA), frequency_str, amplitude_str)
str2 = "Transformada de fourier para el audio 2: Jose Toro"
graph(str2, "blue", frequencyFourierB, abs(fourierB), frequency_str, amplitude_str)

# b. Al resultado del punto 4, calcule la transformada de Fourier inversa.
inverseFourierA = ifft(fourierA).real
inverseFourierB = ifft(fourierB).real

# c. Compare con la señal leída en el punto 1.
str1 = "Transformada inversa de fourier para el audio 1: Cristhofer Parada"
str2 = "Transformada inversa de fourier para el audio 2: Jose Toro"
graph(str1, "red", frequencyFourierA, inverseFourierA, time_str, amplitude_str)
graph(str2, "blue", frequencyFourierB, inverseFourierB, time_str, amplitude_str)

# 5 Calcule y grafique el espectrograma de cada una de las señales. El espectrograma
# permite visualizar información en el dominio de la frecuencia y del tiempo a la vez.
str1 = "Espectrograma de audio 1: Cristhofer Parada"
str2 = "Espectrograma de audio 2: Jose Toro"
graph_spectrogram(str1, signalA, frequencyA, time_str, frequency_str)
graph_spectrogram(str2, signalB, frequencyB, time_str, frequency_str)

# 7 señal ruido rosa
pink_frequency, pink_signal = read("Ruido Rosa.wav")
# a. repetir 3, 4 y 5 con la señal ruidosa

# since both signals need the same frequency, a re-sampling is needed
total_of_samplings = round(len(pink_signal) * float(frequencyA) / pink_frequency)
resampled_pink_signal = resample(pink_signal, total_of_samplings)

# Now the frequency of the pink audio is equal to cristhofer's audio.
pink_frequency = frequencyA
# it's amplitude is calculated
pink_amplitude = len(resampled_pink_signal)
# its duration is calculated
pink_duration = pink_amplitude / pink_frequency
# the axis of time is calculated
pink_time = np.linspace(0, pink_duration, pink_amplitude)

# pink_signal is added to cristhofer's signal in order to make it noisy
noisy_signalA = sum_signals(resampled_pink_signal, signalA)

# it's amplitude, duration and time is calculated
noisy_signalA_amplitude = len(noisy_signalA)
noisy_signalA_duration = noisy_signalA_amplitude / frequencyA
noisy_signalA_time = np.linspace(0, noisy_signalA_duration, noisy_signalA_amplitude)
# the pink signal is plotted
str3 = "Grafico de audio de la señal ruido rosa"
graph(str3, "pink", pink_time, resampled_pink_signal, time_str, amplitude_str)

# fourier derivative is calculated of the pink signal
fourier_pink_signal = fft(resampled_pink_signal)
# also it's frequency
frequency_pink_signal = fftfreq(pink_amplitude)
# the fourier pink signal is plotted
str3 = "Transformada de fourier ruido rosa"
graph(str3, "pink", frequency_pink_signal, abs(fourier_pink_signal), frequency_str, amplitude_str)

# inverse fourier
inverse_fourier_pink = ifft(fourier_pink_signal).real
# is plotted
str3 = "Transformada de fourier inversa ruido rosa"
graph(str3, "pink", pink_time, inverse_fourier_pink, time_str, amplitude_str)

# espectograma
str3 = "Espectrograma de ruido rosa"
graph_spectrogram(str3, resampled_pink_signal, pink_frequency + 1, time_str, frequency_str)

# signal a+ signal pink

write("CristhoferParadaRuidoRosa.wav", frequencyA, noisy_signalA.astype(np.int16))
str3 = "Grafico de la señal 1 + ruido rosa"
graph(str3, "cyan", noisy_signalA_time, noisy_signalA, time_str, amplitude_str)
# fourier a+pink
fourier_pink_plus_signalA = fft(noisy_signalA)
# freq a+pink
frequency_pink_plus_signalA = fftfreq(noisy_signalA_amplitude)
# plotting fourier a+pink
str3 = "Transformada de fourier de la señal 1 + ruido rosa"
graph(str3, "brown", frequency_pink_plus_signalA, abs(fourier_pink_plus_signalA), frequency_str, amplitude_str)

# inverse
inverse_fourier_pink_plus_a = ifft(fourier_pink_plus_signalA).real
# plotting
str3 = "Transformada de fourier inversa de la señal 1 + ruido rosa"
graph(str3, "brown", noisy_signalA_time, inverse_fourier_pink_plus_a, time_str, amplitude_str)

# spectro
str3 = "Espectrograma de la señal 1 + ruido rosa"
graph_spectrogram(str3, noisy_signalA, 6, time_str, frequency_str)

# 8 A continuación se tratará de filtrar el ruido de la señal ruidosa, para ello:
# a. Diseñe un filtro FIR o IIR para eliminar el ruido de la señal de audio.
# Determine el tipo de filtro (pasa bajos, pasa altos, o pasa banda) y determine
# las frecuencias de corte para este de acuerdo a su análisis en el punto 7
# b. Pruebe distintos parámetros al momento de aplicar el filtro y explique por qué
# eligió esos parámetros y cómo afectan el resultado.
# c. Obtenga la transformada de Fourier, el espectrograma de la señal filtrada y
# analice sus resultados.


aux = 0.5 * frequencyA

cut1 = 500
n_cut1 = cut1 / aux
cut1_2 = 4900
n_cut1_2 = cut1_2 / aux
b, a = butter(8, [n_cut1, n_cut1_2], btype='bandpass')

cut2 = 5000
n_cut2 = cut2 / aux
b2, a2 = butter(8, n_cut2, btype='lowpass')

cut3 = 8000
n_cut3 = cut3 / aux
b3, a3 = butter(8, n_cut3, btype='highpass')

filtered_audio1 = filtfilt(b, a, noisy_signalA)
filtered_audio2 = filtfilt(b2, a2, noisy_signalA)
filtered_audio3 = filtfilt(b3, a3, noisy_signalA)

write("AudioFiltrado1.wav", frequencyA, filtered_audio1.astype(np.int16))
write("AudioFiltrado2.wav", frequencyA, filtered_audio2.astype(np.int16))
write("AudioFiltrado3.wav", frequencyA, filtered_audio3.astype(np.int16))

#  the third filtered audio is used to calculate and plot is fourier and spectogram

# its amplitude is caculated
amplitude_filtered3 = len(filtered_audio3)
# Fourier is calculated
fourier_filtered3 = fft(filtered_audio3)
# its duration is calculated
duration_filtered3 = amplitude_filtered3 / frequencyA
# its time is calculated
time_filtered3 = np.linspace(0, duration_filtered3, amplitude_filtered3)
# also its frequency
frequency_filtered3 = fftfreq(amplitude_filtered3)

# fourier transform is plotted
str3 = "Transformada de fourier para el audio filtrado"
graph(str3, "green", frequency_filtered3, abs(fourier_filtered3), frequency_str, amplitude_str)
# spectogram is plotted
str3 = "Espectrograma de audio filtrado"
graph_spectrogram(str3, filtered_audio3, 6, time_str, frequency_str)
