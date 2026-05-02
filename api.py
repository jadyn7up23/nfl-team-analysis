from fastapi import FastAPI
import psycopg2

app = FastAPI()

def get_connection():
    return psycopg2.connect(
        host="localhost",
        database="nfl_stats",
        user="postgres",
        password="your_password_here",
        port="5432"
    )

@app.get("/")
def home():
    return {"message": "NFL Stats API is running"}

@app.get("/items")
def get_items():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT t.team_name, s.year, s.wins, s.losses, o.points, o.total_yards, o.turnovers
        FROM offensive_stats o
        JOIN seasons s ON o.season_id = s.season_id
        JOIN teams t ON s.team_id = t.team_id
        LIMIT 50;
    """)

    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    return [
        {
            "team_name": row[0],
            "year": row[1],
            "wins": row[2],
            "losses": row[3],
            "points": row[4],
            "total_yards": row[5],
            "turnovers": row[6]
        }
        for row in rows
    ]

@app.get("/items/{team_name}")
def get_team(team_name: str):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT t.team_name, s.year, s.wins, s.losses, o.points, o.total_yards, o.turnovers
        FROM offensive_stats o
        JOIN seasons s ON o.season_id = s.season_id
        JOIN teams t ON s.team_id = t.team_id
        WHERE LOWER(t.team_name) LIKE LOWER(%s)
        ORDER BY s.year;
    """, (f"%{team_name}%",))

    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    return [
        {
            "team_name": row[0],
            "year": row[1],
            "wins": row[2],
            "losses": row[3],
            "points": row[4],
            "total_yards": row[5],
            "turnovers": row[6]
        }
        for row in rows
    ]

@app.post("/items")
def add_item(team_name: str, year: int, wins: int, losses: int):
    return {
        "message": "POST endpoint working",
        "team_name": team_name,
        "year": year,
        "wins": wins,
        "losses": losses
    }
