
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# Page configuration
st.set_page_config(
    page_title="Student Performance Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Student Performance Analytics Dashboard")
st.write(
    "Analyze student attendance, subject scores, "
    "and overall academic performance."
)

# Load the dataset
DATA_FILE = Path(__file__).parent / "student.csv"

@st.cache_data
def load_data(file_path):
    return pd.read_csv(file_path)

try:
    df = load_data(DATA_FILE)

    required_columns = [
        "Student",
        "Attendance",
        "Math_Score",
        "Science_Score"
    ]

    missing_columns = [
        column for column in required_columns
        if column not in df.columns
    ]

    if missing_columns:
        st.error(
            f"Missing required columns: {missing_columns}"
        )
        st.stop()

    # Validate numeric columns
    numeric_columns = [
        "Attendance",
        "Math_Score",
        "Science_Score"
    ]

    for column in numeric_columns:
        df[column] = pd.to_numeric(
            df[column], errors="coerce"
        )

    # Data quality summary
    st.subheader("Data Quality Summary")

    missing_values = int(df.isnull().sum().sum())
    duplicate_rows = int(df.duplicated().sum())

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Records", len(df))
    col2.metric("Missing Cells", missing_values)
    col3.metric("Duplicate Rows", duplicate_rows)

    # Identify invalid ranges
    invalid_mask = pd.Series(False, index=df.index)

    for column in numeric_columns:
        invalid_mask |= (
            (df[column] < 0) | (df[column] > 100)
        )

    invalid_records = int(invalid_mask.sum())

    if missing_values or duplicate_rows or invalid_records:
        st.warning(
            "Please review the data quality issues "
            "before interpreting the results."
        )

    # Exclude incomplete or invalid records from analysis
    valid_df = df.dropna(
        subset=required_columns
    ).copy()

    valid_mask = pd.Series(True, index=valid_df.index)

    for column in numeric_columns:
        valid_mask &= (
            (valid_df[column] >= 0)
            & (valid_df[column] <= 100)
        )

    valid_df = valid_df.loc[valid_mask].copy()

    if valid_df.empty:
        st.error("No valid records are available for analysis.")
        st.stop()

    # Calculate performance
    valid_df["Average_Score"] = (
        valid_df["Math_Score"]
        + valid_df["Science_Score"]
    ) / 2

    def categorize_performance(score):
        if score >= 85:
            return "Excellent"
        elif score >= 70:
            return "Good"
        return "Needs Improvement"

    valid_df["Performance_Category"] = (
        valid_df["Average_Score"]
        .apply(categorize_performance)
    )

    # Dashboard metrics
    st.subheader("Performance Overview")

    metric1, metric2, metric3, metric4 = st.columns(4)

    metric1.metric("Students Analyzed", len(valid_df))
    metric2.metric(
        "Average Math Score",
        f"{valid_df['Math_Score'].mean():.2f}"
    )
    metric3.metric(
        "Average Science Score",
        f"{valid_df['Science_Score'].mean():.2f}"
    )
    metric4.metric(
        "Average Attendance",
        f"{valid_df['Attendance'].mean():.2f}%"
    )

    # Student filter
    st.subheader("Explore Student Records")

    selected_categories = st.multiselect(
        "Filter by performance category",
        options=[
            "Excellent",
            "Good",
            "Needs Improvement"
        ],
        default=[
            "Excellent",
            "Good",
            "Needs Improvement"
        ]
    )

    filtered_df = valid_df[
        valid_df["Performance_Category"].isin(
            selected_categories
        )
    ]

    display_columns = [
        "Student",
        "Attendance",
        "Math_Score",
        "Science_Score",
        "Average_Score",
        "Performance_Category"
    ]

    st.dataframe(
        filtered_df[display_columns],
        use_container_width=True,
        hide_index=True
    )

    # Subject comparison chart
    st.subheader("Mathematics vs Science")

    chart_df = filtered_df.set_index("Student")[
        ["Math_Score", "Science_Score"]
    ]

    st.bar_chart(chart_df)

    # Category distribution
    st.subheader("Performance Category Distribution")

    category_counts = (
        filtered_df["Performance_Category"]
        .value_counts()
        .reindex(
            ["Excellent", "Good", "Needs Improvement"],
            fill_value=0
        )
    )

    st.bar_chart(category_counts)

    # Download report
    st.subheader("Export Analysis")

    csv_data = valid_df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="Download Student Analysis CSV",
        data=csv_data,
        file_name="student_performance_report.csv",
        mime="text/csv"
    )

    # Highest-performing student
    top_student = valid_df.loc[
        valid_df["Average_Score"].idxmax()
    ]

    st.subheader("Highest-Performing Student")

    st.success(
        f"Student {top_student['Student']} — "
        f"Average Score: {top_student['Average_Score']:.2f}"
    )

except FileNotFoundError:
    st.error(
        "student.csv was not found. "
        "Keep it in the same folder as dashboard.py."
    )
except pd.errors.EmptyDataError:
    st.error("student.csv is empty.")
except Exception as error:
    st.error(f"Unable to load the dashboard: {error}")
