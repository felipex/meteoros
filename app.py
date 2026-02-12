import os
from flask import Flask, render_template, jsonify
from dotenv import load_dotenv
from supabase import create_client, Client

# Carrega variáveis de ambiente
load_dotenv()

app = Flask(__name__)

# Configurações do Supabase
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("⚠️ SUPABASE_URL e SUPABASE_KEY devem estar no arquivo .env")

# Inicializa o cliente Supabase
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

@app.route("/")
def index():
    try:
        # Busca os últimos 50 registros da tabela 'estacoes'
        # Ordenado por timestamp decrescente
        response = supabase.table("estacoes").select("*").order("timestamp", desc=True).limit(50).execute()
        
        dados = response.data if response.data else []
        
        # Calcula alguns stats simples para o dashboard
        total_leituras = len(dados)
        estacoes_ativas = len(set([d['nome'] for d in dados if d.get('status') is True]))
        
        return render_template(
            "index.html", 
            dados=dados, 
            total=total_leituras, 
            ativas=estacoes_ativas,
            supabase_url=SUPABASE_URL,
            supabase_key=SUPABASE_KEY
        )
    except Exception as e:
        print(f"❌ Erro ao buscar dados: {e}")
        return render_template("index.html", error=str(e), dados=[])

# API para atualização dinâmica (caso queira usar HTMX ou poling no futuro)
@app.route("/api/data")
def get_data():
    response = supabase.table("estacoes").select("*").order("timestamp", desc=True).limit(20).execute()
    return jsonify(response.data)

if __name__ == "__main__":
    app.run(debug=True)
