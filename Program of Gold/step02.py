import pandas as pd
import matplotlib.pyplot as plt

# Φορτώνουμε το WORK αρχείο
work = pd.read_excel("WORK.xlsx")

# Παίρνουμε τη στήλη Price
price = work["Price"]

# Χωρίζουμε σε 2 ίσα μέρη (256 & 256)
first_half = price.iloc[0:256]
second_half = price.iloc[256:512]

# Υπολογισμοί
mean_1 = first_half.mean()
mean_2 = second_half.mean()
std_1 = first_half.std()
std_2 = second_half.std()

mean_diff_percent = abs(mean_1 - mean_2) / mean_1 * 100
std_diff_percent = abs(std_1 - std_2) / std_1 * 100

# Συμπέρασμα
if mean_diff_percent > 15 and std_diff_percent > 3:
    conclusion = "Η χρονοσειρά ΔΕΝ είναι στάσιμη."
else:
    conclusion = "Η χρονοσειρά μπορεί να θεωρηθεί στάσιμη."

print("Μέσος όρος 1ου μέρους:", mean_1)
print("Μέσος όρος 2ου μέρους:", mean_2)
print("Τυπική απόκλιση 1ου μέρους:", std_1)
print("Τυπική απόκλιση 2ου μέρους:", std_2)
print("Διαφορά μέσων (%):", mean_diff_percent)
print("Διαφορά τυπικών (%):", std_diff_percent)
print("Συμπέρασμα:", conclusion)

# Πίνακας αποτελεσμάτων
results_table = pd.DataFrame({
    "Μέρος": ["1ο μέρος", "2ο μέρος"],
    "Μέσος Όρος": [mean_1, mean_2],
    "Τυπική Απόκλιση": [std_1, std_2]
})


# Αποθήκευση πίνακα ως εικόνα
fig, ax = plt.subplots()
ax.axis("off")

display_table = results_table.copy()
display_table["Μέσος Όρος"] = display_table["Μέσος Όρος"].map(lambda v: f"{v:.4f}")
display_table["Τυπική Απόκλιση"] = display_table["Τυπική Απόκλιση"].map(lambda v: f"{v:.4f}")

table_obj = ax.table(
    cellText=display_table.values,
    colLabels=display_table.columns,
    cellLoc="center",
    loc="center"
)

table_obj.auto_set_font_size(False)
table_obj.set_fontsize(10)
table_obj.scale(1.2, 1.2)

plt.title("Σύγκριση στατιστικών στα δύο μέρη", pad=12)
plt.savefig("step02_table.png", bbox_inches="tight")
plt.close(fig)

# Γράφημα split
plt.figure()
plt.plot(first_half.index + 1, first_half, label="1ο μέρος")
plt.plot(second_half.index + 1, second_half, label="2ο μέρος")
plt.title("Χρονοσειρά χωρισμένη σε 2 ίσα μέρη")
plt.xlabel("Χρόνος (εβδομάδες)")
plt.ylabel("Τιμή Χρυσού")
plt.legend()
plt.grid(True)
plt.savefig("step02_stationarity_split.png")
plt.show()
