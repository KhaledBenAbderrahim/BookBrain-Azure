import azure.functions as func
import psycopg2
import json
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv


load_dotenv()

CORS_HEADERS = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type, Origin'
}

def get_config():
    return {
        "db_host": os.getenv("DB_HOST"),
        "db_name": os.getenv("DB_NAME"),
        "db_user": os.getenv("DB_USER"),
        "db_password": os.getenv("DB_PASSWORD"),
        "db_port": os.getenv("DB_PORT"),
    }

def get_db_connection_string(config):
    return f"postgresql://{config['db_user']}:{config['db_password']}@{config['db_host']}:{config['db_port']}/{config['db_name']}"

def main(req: func.HttpRequest) -> func.HttpResponse:
    # Handle OPTIONS request for CORS preflight
    if req.method == 'OPTIONS':
        return func.HttpResponse(
            status_code=200,
            headers=CORS_HEADERS
        )

    user_id = req.params.get('user_id')
    if not user_id:
        return func.HttpResponse(
            "Please provide a user_id parameter.",
            status_code=400,
            headers=CORS_HEADERS
        )

    config = get_config()
    conn_string = get_db_connection_string(config)

    try:
        conn = psycopg2.connect(conn_string)
        cursor = conn.cursor()

        # 2 Wochen Analyse (in Minuten)
        two_weeks_ago = datetime.now() - timedelta(days=14)
        cursor.execute("""
            SELECT DATE(start_time) as date, 
                   ROUND(SUM(EXTRACT(EPOCH FROM (end_time - start_time))/60)) as minutes_learned
            FROM test_attempt
            WHERE user_id = %s AND start_time >= %s
            GROUP BY DATE(start_time)
            ORDER BY DATE(start_time)
        """, (user_id, two_weeks_ago))
        learning_analysis = [{"date": row[0].strftime("%Y-%m-%d"), "minutes_learned": int(row[1])} for row in cursor.fetchall()]

        # Prüfungen
        cursor.execute("""
            SELECT COUNT(*) as total_tests,
                   SUM(CASE WHEN test_success = true THEN 1 ELSE 0 END) as passed_tests
            FROM test_attempt
            WHERE user_id = %s
        """, (user_id,))
        test_stats = cursor.fetchone()
        total_tests, passed_tests = test_stats
        pass_rate = (passed_tests / total_tests) * 100 if total_tests > 0 else 0

        # Lernfortschritt pro Subject
        cursor.execute("""
            SELECT s.subject, 
                   COUNT(ta.test_id) as total_tests,
                   SUM(CASE WHEN ta.test_success = true THEN 1 ELSE 0 END) as passed_tests
            FROM subject s
            JOIN test t ON s.subject_id = t.subject_id
            JOIN test_attempt ta ON t.test_id = ta.test_id
            WHERE ta.user_id = %s
            GROUP BY s.subject
        """, (user_id,))
        learning_progress = [
            {
                "subject": row[0],
                "total_tests": row[1],
                "passed_tests": row[2],
                "pass_rate": (row[2] / row[1]) * 100 if row[1] > 0 else 0
            }
            for row in cursor.fetchall()
        ]

        result = {
            "learning_analysis": learning_analysis,
            "test_statistics": {
                "total_tests": total_tests,
                "passed_tests": passed_tests,
                "pass_rate": pass_rate
            },
            "learning_progress": learning_progress
        }

        return func.HttpResponse(
            json.dumps(result),
            mimetype="application/json",
            status_code=200,
            headers=CORS_HEADERS
        )

    except Exception as e:
        return func.HttpResponse(
            f"An error occurred: {str(e)}",
            status_code=500,
            headers=CORS_HEADERS
        )
    finally:
        if conn:
            cursor.close()
            conn.close()