#! /bin/python
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles

import mysql.connector
import json

# Instanciando o objeto do FastAPI
app = FastAPI()

# Montando a pasta /static para posterior acesso dos arquivos
app.mount("/static", StaticFiles(directory="static"), name="static")

# Caminho da visualização dos dados
@app.get("/")
def index():
    return FileResponse("static/index.html")

# Caminho da API
@app.get('/professores')
def professores():
    q = query("select * from professores")
    professores = jsonificador(q)
    return JSONResponse(content=professores, media_type="application/json")

# Um método para "jsonificar" a query tendo em vista o uso pelo JQuery no HTML
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
        # Conexão ao servidor MySQL/Postgres (estou usando o MySQL)
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
        cursor.close()

# Executando o Uvicorn para abrirmos um servidor web
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("web-service:app", host="localhost", port=8000, reload=True)