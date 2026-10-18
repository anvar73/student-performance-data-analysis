
import pandas as pd
import matplotlib.pyplot as plt

# Step 1: Load the student dataset
df = pd.read_csv("student.csv")

# Step 2: Display the dataset
print("\nSTUDENT DATA")
print(df)

# Step 2: Check data quality
print("\nDATA QUALITY CHECK")

print("\nMissing values in each column:")
print(df.isnull().sum())

print("\nNumber of duplicate rows:")
print(df.duplicated().sum())

print("\nDataset dimensions (rows, columns):")
print(df.shape)

# Step 3: Calculate overall performance
print("\nOVERALL PERFORMANCE")
print("Average Math Score:", df["Math_Score"].mean())
print("Average Science Score:", df["Science_Score"].mean())
print("Average Attendance:", df["Attendance"].mean())

# Step 4: Calculate each student's average score
df["Average_Score"] = (
    df["Math_Score"] + df["Science_Score"]
) / 2

print("\nSTUDENT AVERAGE SCORES")
print(df[["Student", "Average_Score"]])


# Step 5: Categorize student performance
def categorize_performance(score):
    if score >= 85:
        return "Excellent"
    elif score >= 70:
        return "Good"
    else:
        return "Needs Improvement"


df["Performance_Category"] = df["Average_Score"].apply(
    categorize_performance
)

print("\nSTUDENT PERFORMANCE CATEGORIES")
print(df[["Student", "Average_Score", "Performance_Category"]])


# Step 5: Find the highest-performing student
top_student = df.loc[df["Average_Score"].idxmax()]

print("\nHIGHEST-PERFORMING STUDENT")
print("Student:", top_student["Student"])
print("Average Score:", top_student["Average_Score"])

# Step 6: Visualize Mathematics and Science scores
x = range(len(df))
width = 0.35

plt.figure(figsize=(8, 5))

plt.bar(
    [i - width / 2 for i in x],
    df["Math_Score"],
    width,
    label="Mathematics"
)

plt.bar(
    [i + width / 2 for i in x],
    df["Science_Score"],
    width,
    label="Science"
)

plt.xlabel("Student")
plt.ylabel("Score")
plt.title("Student Performance: Math vs Science")
plt.xticks(list(x), df["Student"])
plt.legend()
plt.tight_layout()

# Step 7: Save and display the chart
plt.savefig("student_performance.png", dpi=300)
print("\nChart saved as student_performance.png")

plt.show()


# Step 3: Validate score and attendance ranges

print("\nVALIDATION CHECK")

columns_to_check = [
    "Attendance",
    "Math_Score",
    "Science_Score"
]

for column in columns_to_check:
    invalid_rows = df[
        (df[column] < 0) | (df[column] > 100)
    ]

    print(
        f"{column}: "
        f"{len(invalid_rows)} invalid records"
    )
