import pandas as pd
import matplotlib.pyplot as plt

# Φορτώνουμε το αρχείο εργασίας
work = pd.read_excel("WORK.xlsx")

# Παίρνουμε τη στήλη με τις ποσοστιαίες μεταβολές
j = work["PctDiff"].dropna()

# Υπολογίζουμε την πληθυσμιακή τυπική απόκλιση
std_pop = j.std(ddof=0)

# Υπολογίζουμε τον μέσο όρο
mean = j.mean()

# Υπολογίζουμε το κάτω όριο: mean - 2*std
lower = mean - 2 * std_pop

# Υπολογίζουμε το πάνω όριο: mean + 2*std
upper = mean + 2 * std_pop

# Εκτυπώνουμε τα αποτελέσματα
print("Τυπική απόκλιση =", std_pop)
print("Μέσος όρος =", mean)
print("Κάτω όριο =", lower)
print("Πάνω όριο =", upper)

# Υπολογίζουμε πόσες τιμές είναι εκτός διαστήματος (για να δούμε αν είναι ~5%)
outside_count = ((j < lower) | (j > upper)).sum()

# Υπολογίζουμε ποσοστό εκτός
outside_percent = outside_count / len(j) * 100

# Εκτυπώνουμε τον έλεγχο
print("Πλήθος τιμών εκτός διαστήματος =", outside_count)
print("Ποσοστό εκτός διαστήματος (%) =", outside_percent)

# Φτιάχνουμε έναν μικρό πίνακα αποτελεσμάτων
summary = pd.DataFrame({
    "Μέγεθος": ["Μέσος όρος (μ)", "Τυπική απόκλιση (σ)", "Κάτω όριο μ-2σ", "Πάνω όριο μ+2σ", "Ποσοστό εκτός (%)"],
    "Τιμή": [mean, std_pop, lower, upper, outside_percent]
})

# Αποθηκεύουμε τον πίνακα σε νέο sheet στο WORK.xlsx
with pd.ExcelWriter("WORK.xlsx", engine="openpyxl", mode="a", if_sheet_exists="replace") as writer:
    summary.to_excel(writer, sheet_name="Q9_Interval", index=False)

# Αποθηκεύουμε τον πίνακα ως εικόνα
fig, ax = plt.subplots()
ax.axis("off")

summary_display = summary.copy()
summary_display["Τιμή"] = summary_display["Τιμή"].map(lambda v: f"{v:.6f}")

table_obj = ax.table(
    cellText=summary_display.values,
    colLabels=summary_display.columns,
    cellLoc="center",
    loc="center"
)

table_obj.auto_set_font_size(False)
table_obj.set_fontsize(10)
table_obj.scale(1.2, 1.2)

plt.title("Τυπική απόκλιση και διάστημα μ±2σ", pad=12)
plt.savefig("step09_interval_table.png", bbox_inches="tight")
plt.close(fig)

# Φτιάχνουμε έναν άξονα χρόνου για τις τιμές της J (από Week 2 και μετά, γιατί η 1η είναι NaN)
x_time = work.loc[work["PctDiff"].notna(), "Week"]
j_time = work.loc[work["PctDiff"].notna(), "PctDiff"]

# Δημιουργούμε γράφημα
plt.figure()
plt.plot(x_time, j_time, color="tab:blue", label="PctDiff")

# Γραμμή μέσου όρου
plt.axhline(mean, color="tab:green", linewidth=2, label="μ (μέσος)")

# Γραμμή κάτω ορίου
plt.axhline(lower, color="tab:red", linestyle="--", linewidth=2, label="μ - 2σ")

# Γραμμή πάνω ορίου
plt.axhline(upper, color="tab:red", linestyle="--", linewidth=2, label="μ + 2σ")

# Τίτλος και άξονες
plt.title("Ποσοστιαίες μεταβολές και διάστημα μ ± 2σ")
plt.xlabel("Χρόνος (εβδομάδες)")
plt.ylabel("PctDiff (%)")

# Πλέγμα και υπόμνημα
plt.grid(True)
plt.legend()

# Αποθήκευση εικόνας
plt.savefig("step09_interval_plot.png")

# Εμφάνιση
plt.show()