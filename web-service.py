#! /bin/python
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles

import mysql.connector
import json

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def index():
    return FileResponse("static/index.html")

@app.get('/professores')
def professores():
    print("tsasdfasftes")
    q = query("select * from professores")
    professores = jsonificador(q)
    return JSONResponse(content=professores, media_type="application/json")

def jsonificador(string: str):
    json = []
    for i in string:
        professor = {
            "nome": i[1],
            "cpf": i[2],
            "materia": i[3],
            "incredibilidade": i[4],
            "sexo": i[5],
        }
        json.append(professor)
    return json

def query(q: str):
    connection = None
    cursor = None
    try:
        # Conexão ao servidor MySQL/Postgres (estou usando o MySQL aqui)
        connection = mysql.connector.connect(
            host="localhost",
            user="webservice",
            password="mysql",
            database="webservice"
        )

        cursor = connection.cursor()

        # Executando a query e já retornando sua saída
        cursor.execute(q)
        return cursor.fetchall()
    
    except mysql.connector.Error as e:
        # Caso Deus não nos permita realizar uma conexão, lançamos um 500.
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        # Código anti-cagada
        connection.close()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("web-service:app", host="localhost", port=8000, reload=True)