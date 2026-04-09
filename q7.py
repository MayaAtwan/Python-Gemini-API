# CSV Data Insights
from dotenv import load_dotenv
from google import genai
import os
import pandas as pd

load_dotenv()
client=genai.Client(api_key=os.getenv("GENAI_CLIENT_KEY"))
csv_file=input("Enter the CSV file path:").strip()
try:
    df=pd.read_csv(csv_file)
    if df.empty:
        print("No data found")
        exit(0)
    df=df.drop_duplicates().dropna()
    grade_map={'A':4,'B':3,'C':2,'D':1}
    df['grade_num']=df['grade'].map(grade_map)
    df["internet_access"] = df["internet_access"].map({"Yes": 1, "No": 0})
    df["extra_classes"] = df["extra_classes"].map({"Yes": 1, "No": 0})

    # Correlation with overall score
    correlation = df.corr(numeric_only=True)["overall_score"].sort_values(ascending=False)
    correlation_summary = correlation.to_string()

    # Average scores
    avg_scores = df[[
        "study_hours_per_day",
        "attendance_percentage",
        "sleep_hours",
        "overall_score"
    ]].mean().to_string()

    # Top students
    top_students = df.nlargest(5, "overall_score")[[
        "student_id", "overall_score", "grade"
    ]].to_string(index=False)

    # Grade distribution
    grade_dist = df["grade"].value_counts().to_string()

    prompt = f"""
    You are a professional data analyst.
    
    Analyze the student performance dataset and provide clear insights.
    
    Dataset Overview:
    - Rows: {df.shape[0]}
    - Columns: {df.shape[1]}
    
    Average Values:
    {avg_scores}
    
    Grade Distribution:
    {grade_dist}
    
    Top Performing Students:
    {top_students}
    
    Correlation with Overall Score:
    {correlation_summary}
    
    Please provide:
    1. A short overview of the dataset
    2. 4-6 key insights (focus on relationships and trends)
    3. Any surprising patterns
    4. 2 actionable recommendations for improving student performance
    
    Keep the answer structured and concise.
    """
    response = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=prompt
    )

    print("\n--- CSV Data Insights ---\n")
    print(response.text.strip())
except FileNotFoundError:
    print("Error: File not found.")
except Exception as e:
    print(f"An error occurred: {e}")