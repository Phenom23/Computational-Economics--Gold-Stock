import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Φορτώνουμε το WORK αρχείο
work = pd.read_excel("WORK.xlsx")

# Παίρνουμε τα 512 σημεία
N = 512
x = work["Week"].iloc[0:N].to_numpy(dtype=float)
price = work["Price"].iloc[0:N].to_numpy(dtype=float)

# Παίρνουμε την τάση από τη στήλη Trend
trend = work["Trend"].iloc[0:N].to_numpy(dtype=float)

# F = Price - Trend
F = price - trend
work.loc[0:N-1, "F"] = F

# D = x/512 (συχνότητα)
freq = x / N
work.loc[0:N-1, "Freq"] = freq

# G = FFT(price)
G = np.fft.fft(price)
work.loc[0:N-1, "Fourier"] = G

# E = |G|
E = np.abs(G)
work.loc[0:N-1, "Amplitude"] = E

# Γράφημα Amplitude vs Frequency
plt.figure()
plt.plot(freq, E)
plt.title("Fourier")
plt.xlabel("Συχνότητα")
plt.ylabel("Πλάτος")
plt.grid(True)
plt.savefig("step04_fourier_amplitude.png")
plt.show()

# Εύρεση πρώτης ανόδου (βήμα) με for, στο πρώτο μισό
peak_index = None
for k in range(1, (N // 2) - 1):
    if E[k] > E[k - 1]:
        peak_index = k
        break

# Αν για κάποιο λόγο δεν βρεθεί άνοδος, βάζουμε fallback για να μη σκάσει
if peak_index is None:
    peak_index = 1

step = peak_index + 1
print("Βήμα κυκλικότητας =", step)
print("Έλεγχος τιμών: E[k-1], E[k] =", E[peak_index - 1],",", E[peak_index])

# Υπολογισμός εποχικότητας
groups = step
seasonal_pattern = []

for r in range(step):
    values = []
    for j in range(groups):
        idx = r + j * step
        if idx < len(F):
            values.append(F[idx])
    seasonal_pattern.append(sum(values) / len(values))

# Στήλη H: επανάληψη του μοτίβου
H = np.array([seasonal_pattern[t % step] for t in range(len(F))], dtype=float)
work.loc[0:N-1, "Seasonality"] = H

# Γράφημα κυκλικότητας (H)
plt.figure()
plt.plot(x, H)
plt.title("Συνάρτηση Κυκλικότητας / Εποχικότητας")
plt.xlabel("Χρόνος (εβδομάδες)")
plt.ylabel("Εποχικότητα (S)")
plt.grid(True)
plt.savefig("step04_seasonality.png")
plt.show()

# 3ο γράφημα: Εποχικότητα σε βάθος 9 εβδομάδων (όπως στο FINANCE)
# Παίρνουμε τιμές από H69 έως H77 => στη Python είναι index 68 έως 76
# Παίρνουμε τις τιμές H69:H77 από τη σειρά H (Seasonality)
season_9 = H[68:77]  # 68..76 (9 τιμές)

# Φτιάχνουμε άξονα Χ από 1 έως 9 (όπως στο Excel)
weeks_1_to_9 = np.arange(1, 10)

# Δημιουργούμε το γράφημα
plt.figure()
plt.plot(weeks_1_to_9, season_9)
plt.title("Εποχικότητα σε βάθος 9 εβδομάδων")
plt.grid(True)

# Αποθήκευση για παρουσίαση
plt.savefig("step04_seasonality_9weeks.png")
plt.show()

# Αποθήκευση όλων των νέων στηλών στο WORK.xlsx
work.to_excel("WORK.xlsx", index=False)
