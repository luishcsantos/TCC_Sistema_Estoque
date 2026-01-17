import sqlite3
import random
import shutil
import os

# Definir funções para gerar nomes (reutilizando a lógica anterior para consistência)
def generate_random_client():
    first_names = ["Silva", "Santos", "Oliveira", "Souza", "Rodrigues", "Ferreira", "Alves", "Pereira", "Lima", "Gomes", "Costa", "Ribeiro", "Martins", "Carvalho", "Almeida", "Lopes", "Soares", "Fernandes", "Vieira", "Barbosa", "Rocha", "Dias", "Nascimento", "Andrade", "Moreira", "Nunes", "Marques", "Machado", "Mendes", "Freitas"]
    last_names = ["Comércio", "Indústria", "Ltda", "S.A.", "ME", "EPP", "Serviços", "Tecnologia", "Logística", "Transportes", "Consultoria", "Engenharia", "Sistemas", "Modas", "Alimentos", "Automóveis", "Farmácia", "Padaria", "Mercado", "Loja"]
    
    nomes_pessoas = ["Ana", "Bruno", "Carlos", "Daniela", "Eduardo", "Fernanda", "Gabriel", "Helena", "Igor", "Julia", "Lucas", "Mariana", "Nicolas", "Olivia", "Pedro", "Rafaela", "Samuel", "Tatiana", "Vitor", "Yasmin"]
    sobrenomes_pessoas = ["Silva", "Santos", "Oliveira", "Souza", "Pereira", "Lima", "Carvalho", "Ferreira", "Ribeiro", "Almeida"]
    
    if random.random() > 0.3: # 70% pessoa física
        return f"{random.choice(nomes_pessoas)} {random.choice(sobrenomes_pessoas)}"
    else: # 30% empresa
        return f"{random.choice(first_names)} {random.choice(last_names)}"

# Caminho do arquivo
db_path = 'database/database.db'
output_path = 'database/database_final.db'

if not os.path.exists(db_path):
    print(f"Arquivo {db_path} não encontrado.")
else:
    # Copiar o banco
    shutil.copy(db_path, output_path)
    conn = sqlite3.connect(output_path)
    cursor = conn.cursor()

    try:
        # --- 1. REAPLICAR/GARANTIR ATUALIZAÇÃO DE COMPONENTES (Turno anterior 1) ---
        cursor.execute("SELECT id FROM componentes")
        comp_ids = cursor.fetchall()
        if comp_ids:
            comp_updates = []
            for (cid,) in comp_ids:
                q = random.randint(10, 500)
                qm = random.randint(5, 50)
                comp_updates.append((q, qm, cid))
            cursor.executemany("UPDATE componentes SET quant = ?, quant_min = ? WHERE id = ?", comp_updates)
            print(f"Componentes atualizados: {len(comp_ids)}")

        # --- 2. REAPLICAR/GARANTIR ATUALIZAÇÃO DE ORDEM_SERV (Turno anterior 2) ---
        # Buscar usuários 'user' para técnicos
        cursor.execute("SELECT username FROM user WHERE access_level = 'user'")
        tech_users = [row[0] for row in cursor.fetchall()]
        
        cursor.execute("SELECT id FROM ordem_serv")
        os_ids = cursor.fetchall()
        if os_ids and tech_users:
            os_updates = []
            for (oid,) in os_ids:
                cli = generate_random_client()
                tech = random.choice(tech_users)
                os_updates.append((cli, tech, oid))
            cursor.executemany("UPDATE ordem_serv SET cliente = ?, tecnico_responsavel = ? WHERE id = ?", os_updates)
            print(f"OS atualizadas: {len(os_ids)}")
        elif os_ids:
             # Fallback se não houver usuarios 'user', apenas anonimiza cliente
             os_updates = [(generate_random_client(), oid) for (oid,) in os_ids]
             cursor.executemany("UPDATE ordem_serv SET cliente = ? WHERE id = ?", os_updates)
             print(f"OS atualizadas (apenas clientes): {len(os_ids)}")

        # --- 3. NOVA TAREFA: ATUALIZAR TABELA SGP ---
        # "vendedor" -> "vendedor2"
        # "cliente" -> random
        
        cursor.execute("SELECT id FROM sgp")
        sgp_ids = cursor.fetchall()
        
        if not sgp_ids:
            print("Nenhum registro encontrado na tabela SGP.")
        else:
            sgp_updates = []
            for (sid,) in sgp_ids:
                novo_vendedor = "vendedor2"
                novo_cliente = generate_random_client()
                sgp_updates.append((novo_vendedor, novo_cliente, sid))
            
            cursor.executemany("UPDATE sgp SET vendedor = ?, cliente = ? WHERE id = ?", sgp_updates)
            print(f"SGP atualizados: {len(sgp_ids)}")
            
            # Verificar amostra
            cursor.execute("SELECT id, vendedor, cliente FROM sgp LIMIT 5")
            print("Amostra SGP:", cursor.fetchall())

        conn.commit()

    except Exception as e:
        print(f"Erro: {e}")
    finally:
        conn.close()