import pandas as pd
import matplotlib.pyplot as plt

# Φορτώνουμε WORK
work = pd.read_excel("WORK.xlsx")

# Παίρνουμε τη σειρά MA20
ma20 = work["MA20"]

# Πετάμε τα NaN (πριν συμπληρωθούν 20 τιμές δεν υπάρχει MA20)
ma20_clean = ma20.dropna().reset_index(drop=True)

# Υπολογίζουμε τις πρώτες διαφορές του MA20
ma20_diff = ma20_clean.diff()

# Πετάμε το πρώτο NaN (η πρώτη διαφορά δεν ορίζεται)
ma20_diff = ma20_diff.dropna().reset_index(drop=True)

# Αποθηκεύουμε τη νέα στήλη στο WORK (θα έχει NaN στις αρχές, γιατί ευθυγραμμίζεται με το αρχικό μήκος)
work["MA20_FirstDiff"] = pd.NA
start_row = work["MA20"].first_valid_index()  # πρώτη θέση που υπάρχει MA20
# Οι διαφορές ξεκινούν μία γραμμή μετά από το start_row
work.loc[start_row + 1:start_row + len(ma20_diff), "MA20_FirstDiff"] = ma20_diff.values

# Αποθηκεύουμε WORK
work.to_excel("WORK.xlsx", index=False)

# Χωρισμός σε 2 ίσα κομμάτια των 246 τιμών
first_half = ma20_diff.iloc[0:246]
second_half = ma20_diff.iloc[246:492]

# Υπολογισμοί
mean_1 = first_half.mean()
mean_2 = second_half.mean()

std_1 = first_half.std()
std_2 = second_half.std()

mean_diff_percent = abs(mean_1 - mean_2) / abs(mean_1) * 100 if mean_1 != 0 else float("inf")
std_diff_percent = abs(std_1 - std_2) / abs(std_1) * 100 if std_1 != 0 else float("inf")

# Συμπέρασμα
if mean_diff_percent > 15 and std_diff_percent > 3:
    conclusion = "Συμπέρασμα: Η χρονοσειρά ΔΕΝ είναι στάσιμη."
else:
    conclusion = "Συμπέρασμα: Η χρονοσειρά μπορεί να θεωρηθεί στάσιμη."

# Εκτυπώνουμε αποτελέσματα
print("Μέσος όρος 1ου μέρους:", mean_1)
print("Μέσος όρος 2ου μέρους:", mean_2)
print("Ποσοστιαία διαφορά μέσων όρων (%):", mean_diff_percent)

print("Τυπική απόκλιση 1ου μέρους:", std_1)
print("Τυπική απόκλιση 2ου μέρους:", std_2)
print("Ποσοστιαία διαφορά τυπικών αποκλίσεων (%):", std_diff_percent)

print(conclusion)

# Πίνακας
results_table = pd.DataFrame({
    "Μέρος": ["1ο μέρος", "2ο μέρος"],
    "Μέσος Όρος": [mean_1, mean_2],
    "Τυπική Απόκλιση": [std_1, std_2]
})

fig, ax = plt.subplots()
ax.axis("off")

display_table = results_table.copy()
display_table["Μέσος Όρος"] = display_table["Μέσος Όρος"].map(lambda v: f"{v:.6f}")
display_table["Τυπική Απόκλιση"] = display_table["Τυπική Απόκλιση"].map(lambda v: f"{v:.6f}")

table_obj = ax.table(
    cellText=display_table.values,
    colLabels=display_table.columns,
    cellLoc="center",
    loc="center"
)

table_obj.auto_set_font_size(False)
table_obj.set_fontsize(10)
table_obj.scale(1.2, 1.2)

plt.title("Στατιστικά πρώτων διαφορών του MA(20)", pad=12)
plt.savefig("step16_table.png", bbox_inches="tight")
plt.close(fig)

# Γράφημα της χρονοσειράς διαφορών
plt.figure()
plt.plot(ma20_diff)
plt.title("Πρώτες διαφορές του MA(20)")
plt.xlabel("Παρατήρηση")
plt.ylabel("ΔMA20")
plt.grid(True)
plt.savefig("step16_ma20_firstdiff.png")
plt.show()
