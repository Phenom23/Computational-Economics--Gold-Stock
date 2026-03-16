import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Φορτώνουμε το WORK αρχείο
work = pd.read_excel("WORK.xlsx")

# Παίρνουμε την αρχική χρονοσειρά Price
price = work["Price"]

# Παίρνουμε τις τελευταίες 32 παρατηρήσεις
segment = price.iloc[480:512].to_numpy(dtype=float)

# Ορίζουμε τα n (32, 16, 8, 4, 2)
n_values = [32, 16, 8, 4, 2]

# Θα κρατήσουμε τα αποτελέσματα: log(n) και μέσο log(R/S)
log_n_list = []
mean_log_rs_list = []

# κρατάμε λεπτομέρειες για κάθε ομάδα
details_rows = []

# Για κάθε μέγεθος ομάδας n
for n in n_values:
    # Υπολογίζουμε πόσες ομάδες χωράνε στα 32 σημεία
    num_groups = len(segment) // n

    # Λίστα με log(R/S) για όλες τις ομάδες αυτού του n
    log_rs_groups = []

    # Σπάμε το segment σε num_groups κομμάτια των n σημείων
    for g in range(num_groups):
        # Παίρνουμε την ομάδα g: n τιμές
        group_data = segment[g * n:(g + 1) * n]

        # Βήμα 2: μέσος όρος μ της ομάδας
        mu = group_data.mean()

        # Βήμα 2: αποκλίσεις X = value - μ
        X = group_data - mu

        # Βήμα 2: αθροιστικές αποκλίσεις Y = cumulative sum των X
        Y = np.cumsum(X)

        # Βήμα 3: εύρος R = max(Y) - min(Y)
        R = Y.max() - Y.min()

        # Βήμα 4: S = sqrt( average(X^2) )
        S = np.sqrt(np.mean(X ** 2))

        # Βήμα 5: R/S (προσοχή αν S=0 για να μη διαιρέσουμε με 0)
        if S == 0:
            rs = np.nan
            log_rs = np.nan
        else:
            rs = R / S
            # Βήμα 5: LOG(R/S)
            log_rs = np.log10(rs)

        # Αποθηκεύουμε το log(R/S) της ομάδας
        log_rs_groups.append(log_rs)

        # Αποθηκεύουμε λεπτομέρειες
        details_rows.append({
            "n": n,
            "group": g + 1,
            "mu": mu,
            "R": R,
            "S": S,
            "R/S": rs,
            "log10(R/S)": log_rs
        })

    # Βήμα 7: μέσος όρος log(R/S) για αυτό το n
    mean_log_rs = np.nanmean(log_rs_groups)

    # Βήμα 6: log(n) (Excel LOG = log10)
    log_n = np.log10(n)

    # Αποθηκεύουμε για το γράφημα
    log_n_list.append(log_n)
    mean_log_rs_list.append(mean_log_rs)

# Μετατρέπουμε σε numpy arrays
log_n_arr = np.array(log_n_list, dtype=float)
mean_log_rs_arr = np.array(mean_log_rs_list, dtype=float)

# Βήμα 8: y = a*x + b πάνω στα (log(n), mean log(R/S))
# Το a είναι ο δείκτης Hurst
a, b = np.polyfit(log_n_arr, mean_log_rs_arr, 1)

# Υπολογίζουμε R^2 
y_hat = a * log_n_arr + b
ss_res = np.sum((mean_log_rs_arr - y_hat) ** 2)
ss_tot = np.sum((mean_log_rs_arr - mean_log_rs_arr.mean()) ** 2)
r2 = 1 - ss_res / ss_tot

# Εκτυπώνουμε τον Hurst
print("Hurst (H) =", a)
print("Intercept (b) =", b)
print("R^2 =", r2)

# Αποθήκευση πίνακα αποτελεσμάτων σε νέο sheet στο WORK.xlsx
summary = pd.DataFrame({
    "n": n_values,
    "log10(n)": log_n_arr,
    "mean_log10(R/S)": mean_log_rs_arr
})

hurst_info = pd.DataFrame({
    "Μέγεθος": ["Hurst (H)", "Intercept (b)", "R^2"],
    "Τιμή": [a, b, r2]
})

details = pd.DataFrame(details_rows)

# Γράφουμε σε ξεχωριστά sheets για να μην μπερδεύονται οι στήλες του WORK
with pd.ExcelWriter("WORK.xlsx", engine="openpyxl", mode="a", if_sheet_exists="replace") as writer:
    summary.to_excel(writer, sheet_name="Q11_Summary", index=False)
    hurst_info.to_excel(writer, sheet_name="Q11_Hurst", index=False)
    details.to_excel(writer, sheet_name="Q11_Details", index=False)

# Γράφημα log(n) vs mean log(R/S) + trendline
plt.figure()

# Σημεία
plt.scatter(log_n_arr, mean_log_rs_arr, label="Μέσο log10(R/S)")

# Γραμμή προσαρμογής
x_line = np.linspace(log_n_arr.min(), log_n_arr.max(), 100)
y_line = a * x_line + b
plt.plot(x_line, y_line, label=f"Trendline: y={a:.3f}x+{b:.3f}")

plt.title("Εκτίμηση Hurst με μέθοδο R/S")
plt.xlabel("log10(n)")
plt.ylabel("mean log10(R/S)")
plt.grid(True)
plt.legend()

# Αποθήκευση εικόνας
plt.savefig("step11_hurst_plot.png")

plt.show()
