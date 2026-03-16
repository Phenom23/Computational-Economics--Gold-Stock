import pandas as pd
import matplotlib.pyplot as plt

# Φορτώνουμε το WORK αρχείο
work = pd.read_excel("WORK.xlsx")

# Παίρνουμε τη χρονοσειρά των πρώτων διαφορών
diff_series = work["FirstDiff"]

# Χωρίζουμε σε δύο ίσα μέρη (255 και 255)
first_half = diff_series.iloc[1:256]
second_half = diff_series.iloc[256:511]

# Υπολογίζουμε μέσους όρους
mean_1 = first_half.mean()
mean_2 = second_half.mean()

# Υπολογίζουμε τυπικές αποκλίσεις
std_1 = first_half.std()
std_2 = second_half.std()

# Ποσοστιαίες διαφορές
mean_diff_percent = abs(mean_1 - mean_2) / abs(mean_1) * 100 if mean_1 != 0 else float("inf")
std_diff_percent = abs(std_1 - std_2) / abs(std_1) * 100 if std_1 != 0 else float("inf")

# Συμπέρασμα
if mean_diff_percent > 15 and std_diff_percent > 3:
    conclusion = "Η χρονοσειρά ΔΕΝ είναι στάσιμη."
else:
    conclusion = "Η χρονοσειρά μπορεί να θεωρηθεί στάσιμη."

# Εκτυπώνουμε αποτελέσματα
print("Μέσος όρος 1ου μέρους:", mean_1)
print("Μέσος όρος 2ου μέρους:", mean_2)
print("Ποσοστιαία διαφορά μέσων όρων (%):", mean_diff_percent)

print("Τυπική απόκλιση 1ου μέρους:", std_1)
print("Τυπική απόκλιση 2ου μέρους:", std_2)
print("Ποσοστιαία διαφορά τυπικών αποκλίσεων (%):", std_diff_percent)

print("Συμπέρασμα:", conclusion)

# Πίνακας ως εικόνα
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

plt.title("Στατιστικά Πρώτων Διαφορών (2 μέρη)", pad=12)
plt.savefig("step07_table.png", bbox_inches="tight")
plt.close(fig)

# Γράφημα split
plt.figure()
plt.plot(first_half.index + 1, first_half, label="1ο μέρος")
plt.plot(second_half.index + 1, second_half, label="2ο μέρος")
plt.title("Πρώτες Διαφορές χωρισμένες σε 2 ίσα μέρη")
plt.xlabel("Χρόνος (εβδομάδες)")
plt.ylabel("Πρώτες Διαφορές")
plt.legend()
plt.grid(True)
plt.savefig("step07_split.png")
plt.show()
