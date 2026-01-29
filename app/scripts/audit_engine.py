import os
import sqlite3

import pandas as pd


def run_quality_audit():
    #1. Connect to DB
    script_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(script_dir, "../../ai_engine.db")
    conn = sqlite3.connect(db_path)

    #2. SQL Query to join Tasks and Evaluations
    query = """
    SELECT 
        t.input_text, 
        e.judge_score, 
        e.confidence_score, 
        e.passed,
        e.reasoning
    FROM tasks t
    JOIN evaluations e ON t.id = e.task_id
    """

    #3. Load into DatFrame
    df = pd.read_sql_query(query, conn)
    if df.empty:
        print("No data found.")
        return
    
    #4. Calculate the "Hallucination Gap"
    # A high gap means the model was confident but the judge hated it.
    df['h_gap'] = df['confidence_score'] - df['judge_score']

    print("\n" + "="*40)
    print("       AI ENGINE QUALITY AUDIT")
    print("="*40)
    
    # Summary Metrics
    print(f"Total Interactions:      {len(df)}")
    print(f"Average Judge Score:     {df['judge_score'].mean():.2f}")
    print(f"Average Math Confidence: {df['confidence_score'].mean():.2f}")
    print(f"Overall Pass Rate:       {(df['passed'].mean()*100):.1f}%")
    
    # 4. Identify Confident Hallucinations
    # We flag cases where math confidence is > 0.7 but judge score is < 0.4
    hallucinations = df[(df['confidence_score'] > 0.7) & (df['judge_score'] < 0.4)]
    
    print("\n" + "-"*40)
    print(f"DETECTED HALLUCINATIONS ({len(hallucinations)})")
    print("-"*40)
    
    for i, row in hallucinations.iterrows():
        print(f"Input: {row['input_text'][:60]}...")
        print(f" -> Math Confidence: {row['confidence_score']:.2f}")
        print(f" -> Judge Score:     {row['judge_score']:.2f}")
        print(f" -> Reason:          {row['reasoning']}")
        print("-" * 20)

    conn.close()

if __name__ == "__main__":
    run_quality_audit()