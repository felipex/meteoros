import os
from dotenv import load_dotenv
from supabase import create_client, Client
from datetime import datetime

# Carrega variáveis de um arquivo .env
load_dotenv()

# Configurações do Supabase via Variáveis de Ambiente
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
ESTACAO = os.getenv("ESTACAO")

# Verifica se as credenciais foram carregadas
if not SUPABASE_URL or not SUPABASE_KEY:
    print("⚠️ ERRO: Credenciais do Supabase não encontradas no arquivo .env")
    print("Certifique-se de configurar SUPABASE_URL e SUPABASE_KEY.")
    exit(1)

# Inicializa o cliente UMA vez (Escopo Global/Singleton pattern)
try:
    print(SUPABASE_URL)
    print(SUPABASE_KEY)
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
except Exception as e:
    print(f"❌ Erro ao inicializar cliente Supabase: {e}")
    exit(1)

def inserir_dados_estacao(nome_estacao: str = "ESTACAO01", status: bool = True, rms_status: bool = True):
    """
    Insere telemetria de uma estação no Supabase.
    """
    dados = {
        "nome": nome_estacao,
        "timestamp": datetime.now().isoformat(),
        "status": status,
        "rms_status": rms_status
    }

    try:
        # Realiza o insert e captura o resultado
        response = supabase.table("estacoes").insert(dados).execute()
        
        # postgrest-py levanta exceções para erros de rede, 
        # mas verificamos data para confirmar sucesso do insert.
        if response.data:
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ✅ Sucesso: Dado inserido para {nome_estacao}")
            return response.data
            
    except Exception as e:
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ❌ Erro ao inserir no banco: {e}")
        return None

import sys

if __name__ == "__main__":
    # Teste de execução
    print("🚀 Iniciando script de inserção...")
    
    # Se passar um argumento via linha de comando, usa ele como nome da estação
    # Exemplo: python insert_meteo.py ESTACAO_ALPHA
    if len(sys.argv) > 1:
        estacao_alvo = sys.argv[1]
        rms_status = sys.argv[2]
    else:
        estacao_alvo = ESTACAO or "ESTACAO_PADRAO"
        rms_status = True

    inserir_dados_estacao(estacao_alvo, True, rms_status)