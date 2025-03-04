from flask import Flask, request, render_template
import pandas as pd
import os

app = Flask(__name__)

# Nome del file Excel che conterrà i dati
EXCEL_FILE = "responses.xlsx"

# Inizializza il file Excel se non esiste
if not os.path.exists(EXCEL_FILE):
    df = pd.DataFrame(columns=["Nome", "Email", "Risposta"])
    df.to_excel(EXCEL_FILE, index=False)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        nome = request.form["nome"]
        email = request.form["email"]
        risposta = request.form["risposta"]

        # Carica il file Excel
        df = pd.read_excel(EXCEL_FILE)

        # Evita che lo stesso utente compili due volte (controllo sull'email)
        if email in df["Email"].values:
            return "Hai già compilato il modulo!"

        # Aggiungi la nuova riga
        new_data = pd.DataFrame([[nome, email, risposta]], columns=["Nome", "Email", "Risposta"])
        df = pd.concat([df, new_data], ignore_index=True)

        # Salva il file aggiornato
        df.to_excel(EXCEL_FILE, index=False)

        return "Risposta salvata con successo!"

    return render_template("form.html")

# Endpoint per scaricare il file Excel
@app.route("/download")
def download():
    return f'<a href="{EXCEL_FILE}" download>Clicca qui per scaricare il file Excel</a>'

if __name__ == "__main__":
    app.run(debug=True)
