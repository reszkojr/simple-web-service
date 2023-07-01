# simple-web-service
A simple web service made with FastAPI and Jim Carrey.

![Screenshot_20230701_123758](https://github.com/reszkojr/simple-web-service/assets/67809084/9e915ee7-57c5-4b62-9047-c28aa19fc8d3)

### Python modules:

```bash
python3 -m pip install fastapi uvicorn psycopg2 jinja2 python-multipart sqlalchemy mysql-connector-python
```

### SQL commands:
```sql
CREATE TABLE professores (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    cpf VARCHAR(11) UNIQUE NOT NULL,
    materia VARCHAR(50) NOT NULL,
    incredibilidade INT(100) UNSIGNED NOT NULL,
    sexo CHAR(1) NOT NULL
);
```

```sql
INSERT INTO professores (nome, cpf, materia, incredibilidade, sexo) VALUES
      ('Eduardo Tieppo', '12345678901', 'Dev. Web', '10000', 'M'),
      ('Loretta Rosolem', '23456789012', 'AEE', '100', 'F'),
      ('Bárbara Elisa', '34567890123', 'Português', '100', 'F'),
      ('Alessandra Zavala', '45678901234', 'Matemática', '80', 'F'),
      ('Felipe Comitre', '56789012345', 'Geografia', '100', 'M'),
      ('Marlon Vaz', '67890123456', 'Alguma coisa ae, não sei', '70', 'M');
```

### HTML code:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Professores</title>

    <!-- Famoso Jim Carrey -->
    <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
    <style>
        body {
            background-color: #1E293B;
            font-family: Arial;
        }

        #professores {
            display: grid;
            grid-template-columns: 1fr 1fr 1fr;
            column-gap: 15px;
            row-gap: 15px;
        }

        .professor {
            color: #82b2ff;
            padding: 10px;
            border: 1px;
            background-color: #243247;
            border-radius: 8px;
        }

        .nome {
            font-weight: bold;
        }

        .attr {
            color: lightgray;
        }
    </style>
</head>
<body>
    <div id="professores"></div>
    <script>
        // Código AJAX responsável por requisitar os dados da API
        $.ajax({
            url: "/professores",
            method: "GET",
            dataType: "json",
            success: function(data) { // Criando as devidas div's caso a requisição tenha sucesso
                var container = $("#professores");
                data.forEach(function(professor) {
                    var professorEl = $("<div>").addClass("professor");
                        var nomeEl = $("<div>").addClass("nome").text("Nome: " + professor.nome);
                        var cpfEl = $("<div>").addClass("attr").text("CPF: " + professor.cpf);
                        var incredibilidadeEl = $("<div>").addClass("attr").text("Incrivibilidade: " + professor.incredibilidade + "%");
                        var materiaEl = $("<div>").addClass("attr").text("Matéria: " + professor.materia);
                        var sexoEl = $("<div>").addClass("attr").text("Sexo: " + professor.sexo);    
                            
                        professorEl.append(nomeEl, cpfEl, incredibilidadeEl, materiaEl, sexoEl);
                        container.append(professorEl);
                    })
            },
            error: function() { // Caso não, erronamente, algo de errado certamente não está certo.
                console.log("Exception: a serious cagada has happened.")
            }
        })
    </script>
</body>
</html>
```

### Python (FastAPI) code:

```python
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
```
