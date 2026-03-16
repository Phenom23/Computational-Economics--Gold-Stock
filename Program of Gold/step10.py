import pandas as pd
import matplotlib.pyplot as plt
import textwrap

# =====================
# STEP 10 – VAR SUMMARY
# =====================

# Διαβάζουμε τα όρια από Step 9
q9 = pd.read_excel("WORK.xlsx", sheet_name="Q9_Interval")

lower = q9.loc[q9["Μέγεθος"] == "Κάτω όριο μ-2σ", "Τιμή"].values[0]
upper = q9.loc[q9["Μέγεθος"] == "Πάνω όριο μ+2σ", "Τιμή"].values[0]

# Συμπέρασμα
conclusion = (
    f"Το VAR βρίσκεται κάτω από το {lower:.2f}% "
    f"και πάνω από το {upper:.2f}%"
)

# =====================
# DATAFRAME (για print & Excel)
# =====================
var_table = pd.DataFrame({
    "Περιγραφή": [
        "Κάτω όριο VAR",
        "Πάνω όριο VAR",
        "Συμπέρασμα"
    ],
    "Τιμή": [
        f"{lower:.2f} %",
        f"{upper:.2f} %",
        conclusion
    ]
})

# =====================
# PRINT 
# =====================
pd.set_option("display.max_colwidth", None)
print(var_table)

# =====================
# Αποθήκευση σε Excel
# =====================
with pd.ExcelWriter("WORK.xlsx", engine="openpyxl", mode="a", if_sheet_exists="replace") as writer:
    var_table.to_excel(writer, sheet_name="Q10_VAR", index=False)

# =====================
# ΕΙΚΟΝΑ (PNG)
# =====================

# Έκδοση πίνακα ΜΟΝΟ για το PNG
var_table_img = var_table.copy()

# Αναδίπλωση κειμένου μόνο στο συμπέρασμα
var_table_img.loc[
    var_table_img["Περιγραφή"] == "Συμπέρασμα", "Τιμή"
] = textwrap.fill(conclusion, width=45)

fig, ax = plt.subplots(figsize=(10, 4))
ax.axis("off")

table = ax.table(
    cellText=var_table_img.values,
    colLabels=var_table_img.columns,
    cellLoc="center",
    colLoc="center",
    loc="center"
)

# Μορφοποίηση
table.auto_set_font_size(False)
table.set_fontsize(12)
table.scale(1.25, 2.0)

plt.title("VAR – Όρια κινδύνου (βάσει μ ± 2σ)", pad=15)

plt.savefig("step10_var_table.png", bbox_inches="tight", dpi=200)
plt.close(fig)
