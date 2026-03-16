import pandas as pd
import numpy as np


# -------------------------------
# Φορτώνουμε τα δεδομένα
# -------------------------------
work = pd.read_excel("WORK.xlsx")

# Χρόνος (Week)
x = work["Week"].to_numpy(dtype=float)

# Σειρές που μας ενδιαφέρουν
y_price = work["Price"].to_numpy(dtype=float)
y_stoch = work["Stochastic"].to_numpy(dtype=float)

# -------------------------------
# Συνάρτηση υπολογισμού R^2 από γραμμική τάση
# -------------------------------
def trend_r2(x, y):
    mask = ~np.isnan(x) & ~np.isnan(y)
    x2 = x[mask]
    y2 = y[mask]

    x_mean = x2.mean()
    y_mean = y2.mean()
    sxx = ((x2 - x_mean) ** 2).sum()
    sxy = ((x2 - x_mean) * (y2 - y_mean)).sum()
    a = sxy / sxx
    b = y_mean - a * x_mean

    y_hat = a * x2 + b
    sse = ((y2 - y_hat) ** 2).sum()
    sst = ((y2 - y_mean) ** 2).sum()
    r2 = 1 - sse / sst

    return a, b, r2

# -------------------------------
# Υπολογισμοί R^2 και R
# -------------------------------
a_price, b_price, r2_price = trend_r2(x, y_price)
a_stoch, b_stoch, r2_stoch = trend_r2(x, y_stoch)

R_price = np.sqrt(r2_price)
R_stoch = np.sqrt(r2_stoch)

# -------------------------------
# Συνάρτηση παραγωγής πορίσματος με R
# -------------------------------
def r2_conclusion(series_name, r2, R):
    print(f"Χρονοσειρά {series_name}:")
    print(f"R² = {r2:.4f}, R = {R:.4f}")

    if r2 > 0.85:
        print("Συμπέρασμα: Υπάρχει σίγουρη ευθεία,")
        print("τα σημεία ακολουθούν πολύ πιστά την ευθεία,")
        print("γεγονός που υποδηλώνει πολύ καλή αυτοσυσχέτιση.")
    elif r2 > 0.7:
        print("Συμπέρασμα: Υπάρχει ευθεία,")
        print("τα σημεία ακολουθούν αρκετά πιστά την ευθεία,")
        print("γεγονός που υποδηλώνει καλή αυτοσυσχέτιση.")
    elif r2 > 0.4:
        print("Συμπέρασμα: Υπάρχει μάλλον ευθεία,")
        print("τα σημεία ακολουθούν σχετικά πιστά την ευθεία,")
        print("γεγονός που υποδηλώνει μέτρια αυτοσυσχέτιση.")
    else:
        print("Συμπέρασμα: Δεν υπάρχει ευθεία,")
        print("τα σημεία δεν ακολουθούν την ευθεία,")
        print("γεγονός που υποδηλώνει καθόλου αυτοσυσχέτιση.")

    print("-" * 50)

# -------------------------------
# Εκτύπωση πορισμάτων
# -------------------------------
print("\nΑΠΟΤΕΛΕΣΜΑΤΑ ΑΝΑΛΥΣΗΣ R² και R\n")
r2_conclusion("Price", r2_price, R_price)
r2_conclusion("Stochastic", r2_stoch, R_stoch)

