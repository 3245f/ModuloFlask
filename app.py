from flask import Flask, request, render_template, send_file, abort
import pandas as pd
import os




'''def format_risposta_aperta(domanda, risposta):
    return f"{domanda}: {risposta}" if risposta else ""'''

'''"Linguaggi": linguaggi,
            "C++": format_dettagli("C++", request.form.get("cplus_tempo", ""), request.form.get("cplus_luogo", ""), request.form.get("cplus_progetto", "")),
            "Java": format_dettagli("Java", request.form.get("java_tempo", ""), request.form.get("java_luogo", ""), request.form.get("java_progetto", "")),
            "Python": format_dettagli("Python", request.form.get("python_tempo", ""), request.form.get("python_luogo", ""), request.form.get("python_progetto", "")),
            "JavaScript": format_dettagli("JavaScript", request.form.get("javascript_tempo", ""), request.form.get("javascript_luogo", ""), request.form.get("javascript_progetto", "")),
            "PLC": plc,
            "Sistemi Operativi": sistemi_operativi,
            "Siemens": format_dettagli("Siemens", request.form.get("siemens_tempo", ""), request.form.get("siemens_luogo", ""), request.form.get("siemens_progetto", "")),
            "Allen-Bradley": format_dettagli("Allen-Bradley", request.form.get("allen_tempo", ""), request.form.get("allen_luogo", ""), request.form.get("allen_progetto", "")),
            "Omron": format_dettagli("Omron", request.form.get("omron_tempo", ""), request.form.get("omron_luogo", ""), request.form.get("omron_progetto", "")),
'''


app = Flask(__name__)

EXCEL_FILE = "responses.xlsx"

if not os.path.exists(EXCEL_FILE):


    df = pd.DataFrame(columns=[
        "Nome", "Email"])

    df.to_excel(EXCEL_FILE, index=False)



def format_dettagli(tecnologia, tempo, luogo, progetto):
    return f"Mesi: {tempo} | Esperienza: {luogo} | Progetto: {progetto}" if (tempo or luogo or progetto) else ""

############################ NEW  ########################################
# Funzione per aggiungere le informazioni in ordine logico
def aggiungi_sezione(nome_sezione, scelte, dettagli_dict,data):
    """Aggiunge la colonna con le scelte e i dettagli di una specifica area al dizionario dei dati"""
    data[f"Aree progetti {nome_sezione}"] = ", ".join(scelte)
    
    # Aggiunge ogni dettaglio subito dopo la relativa sezione
    for area in dettagli_dict:
        data[area] = "\n\n".join(dettagli_dict[area]) if dettagli_dict[area] else ""

###########################  END NEW  #####################################

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        nome = request.form.get("nome", "")
        email = request.form.get("email", "")
        istruzione = request.form.get("istruzione", "")
        studi = request.form.get("studi", "")
        certificati = request.form.get("certificati", "")
        sede = request.form.get("sede", "")
        esperienza = request.form.get("esperienza", "")
        esperienza_alten = request.form.get("esperienza_alten", "")
        clienti_railway= request.form.getlist("clienti")  
        clienti_str = ", ".join(clienti_railway) if clienti_railway else "" 
        area_railway= request.form.getlist("area_railway")  
        area_str = ", ".join(area_railway) if area_railway else "" 
        normative = request.form.get("normative", "")
        metodologia= request.form.getlist("metodologia")  
        metodologia_str = ", ".join(metodologia) if metodologia else "" 
        sistemi_operativi = request.form.get("SistemiOperativi", "")
        altro= request.form.getlist("altro")  
        altro_str = ", ".join(altro) if altro else "" 
        hobby= request.form.getlist("hobby")  
        hobby_str = ", ".join(hobby) if hobby else "" 


# Progetti SVILUPPO
        progetti_sviluppo_si_no = request.form.get('progetti_sw_hw_auto', 'No')  
        scelte_progetti_sviluppo = request.form.getlist('sviluppo')  
        dettagli = {area: "" for area in ["Applicativi", "Firmware", "Web", "Mobile", "SCADA", "PLC"]}
        #print(request.form) 
        for area in dettagli.keys():
            if area not in scelte_progetti_sviluppo:  
                continue  

            linguaggi = request.form.getlist(f'linguaggi_{area.lower()}[]')
            tool = request.form.getlist(f'tool_{area.lower()}[]')
            ambito = request.form.getlist(f'Ambito_{area.lower()}[]')
            descrizione = request.form.getlist(f'descrizione_{area.lower()}[]')
            print(f"{area} -> Linguaggi: {linguaggi}, Tool: {tool}, Ambito: {ambito}, Descrizione: {descrizione}")
            esperienze = []
            for i in range(max(len(linguaggi), len(tool), len(ambito), len(descrizione))):
                l = linguaggi[i] if i < len(linguaggi) else ""
                t = tool[i] if i < len(tool) else ""
                a = ambito[i] if i < len(ambito) else ""
                d = descrizione[i] if i < len(descrizione) else ""
                esperienze.append(f"{l} | {t} | {a} | {d}")
            dettagli[area] =esperienze
        print("dettagli sviluppo",dettagli)
        linguaggi = ", ".join(request.form.getlist("linguaggi")) if request.form.getlist("linguaggi") else "Nessuno"
        plc = ", ".join(request.form.getlist("plc")) if request.form.getlist("plc") else "Nessuno"
      
# Progetti V&V
        scelte_progetti_vv = request.form.getlist('v&v')  
        dettagli_vv = {area: "" for area in ["functional_testing", "test_and_commisioning", "unit", "analisi_statica", "analisi_dinamica", "automatic_test", "piani_schematici", "procedure", "cablaggi", "FAT", "SAT", "doc"]}
        for area in dettagli_vv.keys():
            if area not in scelte_progetti_vv:  
                continue  

            tecnologie = request.form.getlist(f'tecnologie_{area}[]')
            ambito = request.form.getlist(f'azienda_{area}[]')
            descrizione = request.form.getlist(f'descrizione_{area}[]')
            print(f"{area} -> Tecnologie: {tecnologie}, Ambito: {ambito}, Descrizione: {descrizione}")
            esperienze = []
            for i in range(max(len(tecnologie), len(ambito), len(descrizione))):
                t = tecnologie[i] if i < len(tecnologie) else ""
                a = ambito[i] if i < len(ambito) else ""
                d = descrizione[i] if i < len(descrizione) else ""
                esperienze.append(f" {t} | {a} | {d}")
            dettagli_vv[area] =esperienze
        print(dettagli_vv)
        tecnologie = ", ".join(request.form.getlist("tecnologie")) if request.form.getlist("tecnologie") else "Nessuno"

# Progetti System
        scelte_progetti_system = request.form.getlist('system')  
        dettagli_system = {area: "" for area in ["requirement management", "requirement_engineering", "system_engineering", "project_engineering"]}
        for area in dettagli_system.keys():
            if area not in scelte_progetti_system:  
                continue  

            #tecnologie = request.form.getlist(f'tecnologie_{area.lower()}[]')
            tecnologie = request.form.getlist(f'tecnologie_{area}[]')
            ambito = request.form.getlist(f'azienda_{area}[]')
            descrizione = request.form.getlist(f'descrizione_{area}[]')
            print(f"{area} -> Tecnologie: {tecnologie}, Ambito: {ambito}, Descrizione: {descrizione}")
            esperienze = []
            for i in range(max(len(tecnologie), len(ambito), len(descrizione))):
                t = tecnologie[i] if i < len(tecnologie) else ""
                a = ambito[i] if i < len(ambito) else ""
                d = descrizione[i] if i < len(descrizione) else ""
                esperienze.append(f"{t} | {a} | {d}")
            dettagli_system[area] =esperienze
        print(dettagli_system)
        tecnologie = ", ".join(request.form.getlist("tecnologie")) if request.form.getlist("tecnologie") else "Nessuno"

# Progetti Safety
        scelte_progetti_safety = request.form.getlist('safety')  
        dettagli_safety = {area: "" for area in ["RAMS", "hazard_analysis", "verification_report", "fire_safety", "reg_402"]}
        print(request.form) 
        for area in dettagli_safety.keys():
            if area not in scelte_progetti_safety: 
                continue  

            tecnologie = request.form.getlist(f'tecnologie_{area}[]')
            ambito = request.form.getlist(f'azienda_{area}[]')
            descrizione = request.form.getlist(f'descrizione_{area}[]')
            print(f"{area} -> Tecnologie: {tecnologie}, Ambito: {ambito}, Descrizione: {descrizione}")
            esperienze = []
            for i in range(max(len(tecnologie), len(ambito), len(descrizione))):
                t = tecnologie[i] if i < len(tecnologie) else ""
                a = ambito[i] if i < len(ambito) else ""
                d = descrizione[i] if i < len(descrizione) else ""
                esperienze.append(f"{t} | {a} | {d}")
            dettagli_safety[area] =esperienze
        print(dettagli_safety)
        tecnologie = ", ".join(request.form.getlist("tecnologie")) if request.form.getlist("tecnologie") else "Nessuno"

# Progetti Segnalamento      
        scelte_progetti_segnalamento = request.form.getlist('segnalamento')  
        dettagli_seg = {area: "" for area in ["piani_schematici_segnalamento", "cfg_impianti", "layout_apparecchiature", "architettura_rete", "computo_metrico"]}
        for area in dettagli_seg.keys():
            if area not in scelte_progetti_segnalamento:  
                continue  

            tecnologie = request.form.getlist(f'tecnologie_{area}[]')
            ambito = request.form.getlist(f'azienda_{area}[]')
            descrizione = request.form.getlist(f'descrizione_{area}[]')
            print(f"{area} -> Tecnologie: {tecnologie}, Ambito: {ambito}, Descrizione: {descrizione}")
            esperienze = []
            for i in range(max(len(tecnologie),len(ambito), len(descrizione))):
                t = tecnologie[i] if i < len(tecnologie) else ""
                a = ambito[i] if i < len(ambito) else ""
                d = descrizione[i] if i < len(descrizione) else ""
                esperienze.append(f"{t} | {a} | {d}")
            dettagli_seg[area] = esperienze
        print(dettagli_seg)
        tecnologie = ", ".join(request.form.getlist("tecnologie")) if request.form.getlist("tecnologie") else "Nessuno"


# Dati da salvare nel file excel
        data = {
            "Nome": nome,
            "Email": email,
            "Istruzione": istruzione,
            "Certificazioni": certificati,
            "Sede Alten": sede,
            "Esperienza (anni)": esperienza,
            "Esperienza Alten (anni)": esperienza_alten,
            "Clienti Railway":  clienti_str, 
            "Area Railway": area_str, 
            "Normative": normative, 
            "Metodologie lavoro": metodologia_str,
            "Sistemi Operativi": sistemi_operativi,
            "Info aggiuntive": altro_str,
            "Hobby": hobby_str,
            "Progetti Sviluppo": progetti_sviluppo_si_no,
           # "Aree progetti Sviluppo": ", ".join(scelte_progetti_sviluppo),
           # "Aree progetti V&V": ", ".join(scelte_progetti_vv),
           # "Aree progetti Safety": ", ".join(scelte_progetti_safety),
            #"Aree progetti System": ", ".join(scelte_progetti_system),
            #"Aree progetti Segnalamento": ", ".join(scelte_progetti_segnalamento),
        }




        '''memorizza i dettagli delle varie sezioni non nell'ordine desiderato
        #sviluppo
        for area in dettagli:
            data[area] = "\n\n".join(dettagli[area]) if dettagli[area] else ""
        #V&V
        for area in dettagli_vv:
            data[area] = "\n\n".join(dettagli_vv[area]) if dettagli_vv[area] else ""
        #safety
        for area in dettagli_safety: 
              data[area] = "\n\n".join(dettagli_safety[area]) if dettagli_safety[area] else ""       
        #system
        for area in dettagli_system:
            data[area] = "\n\n".join(dettagli_system[area]) if dettagli_system[area] else ""
        #segnalamento
        for area in dettagli_seg:
            data[area] = "\n\n".join(dettagli_seg[area]) if dettagli_seg[area] else "" '''''''''


#########################################  NEW  #####################################################

        # Aggiunta delle varie sezioni in ordine
        aggiungi_sezione("Sviluppo", scelte_progetti_sviluppo, dettagli,data)
        aggiungi_sezione("V&V", scelte_progetti_vv, dettagli_vv,data)
        aggiungi_sezione("Safety", scelte_progetti_safety, dettagli_safety,data)
        aggiungi_sezione("System", scelte_progetti_system, dettagli_system,data)
        aggiungi_sezione("Segnalamento", scelte_progetti_segnalamento, dettagli_seg,data)

#########################################  END NEW  #################################################

        
        df = pd.read_excel(EXCEL_FILE)
        df = pd.concat([df, pd.DataFrame([data])], ignore_index=True)
        df.to_excel(EXCEL_FILE, index=False)
        return "Risposta salvata con successo!"
    
    return render_template("form.html")

@app.route("/download")
def download():
    if not os.path.exists(EXCEL_FILE):
        return abort(404, description="File not found")
    return send_file(EXCEL_FILE, as_attachment=True, download_name="responses.xlsx")

if __name__ == "__main__":
    app.run(debug=True)
