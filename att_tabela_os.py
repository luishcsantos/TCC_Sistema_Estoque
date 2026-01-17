import sqlite3
import random
import shutil
import os

# Verificar se o arquivo existe
db_path = 'database/database.db'
if not os.path.exists(db_path):
    print(f"Arquivo {db_path} não encontrado.")
else:
    # Criar uma cópia para não alterar o original
    updated_db_path = 'database/database_anonymized.db'
    shutil.copy(db_path, updated_db_path)
    
    conn = sqlite3.connect(updated_db_path)
    cursor = conn.cursor()
    
    try:
        # 1. Verificar níveis de acesso disponíveis na tabela user
        cursor.execute("SELECT DISTINCT access_level FROM user")
        levels = cursor.fetchall()
        print("Níveis de acesso encontrados:", levels)
        
        # 2. Buscar usuários com access_level = 'user'
        target_level = 'user'
        cursor.execute("SELECT username FROM user WHERE access_level = ?", (target_level,))
        tech_users = [row[0] for row in cursor.fetchall()]
        
        if not tech_users:
            print(f"AVISO: Nenhum usuário encontrado com access_level='{target_level}'.")
            # Fallback opcional: buscar todos para mostrar o que existe, caso o usuário tenha se enganado
            cursor.execute("SELECT username, access_level FROM user")
            all_users = cursor.fetchall()
            print("Usuários disponíveis:", all_users)
            # Se não houver users 'user', não podemos atualizar o técnico conforme solicitado.
            # Vou parar ou usar uma lista vazia, o que impediria a atualização desse campo.
        else:
            print(f"Usuários técnicos encontrados ({len(tech_users)}):", tech_users)

        # 3. Listas de nomes para gerar clientes aleatórios
        first_names = ["Silva", "Santos", "Oliveira", "Souza", "Rodrigues", "Ferreira", "Alves", "Pereira", "Lima", "Gomes", "Costa", "Ribeiro", "Martins", "Carvalho", "Almeida", "Lopes", "Soares", "Fernandes", "Vieira", "Barbosa", "Rocha", "Dias", "Nascimento", "Andrade", "Moreira", "Nunes", "Marques", "Machado", "Mendes", "Freitas"]
        last_names = ["Comércio", "Indústria", "Ltda", "S.A.", "ME", "EPP", "Serviços", "Tecnologia", "Logística", "Transportes", "Consultoria", "Engenharia", "Sistemas", "Modas", "Alimentos", "Automóveis", "Farmácia", "Padaria", "Mercado", "Loja"]
        # Misturando nomes de pessoas e empresas para clientes

        nomes_pessoas = ["Ana", "Bruno", "Carlos", "Daniela", "Eduardo", "Fernanda", "Gabriel", "Helena", "Igor", "Julia", "Lucas", "Mariana", "Nicolas", "Olivia", "Pedro", "Rafaela", "Samuel", "Tatiana", "Vitor", "Yasmin"]
        sobrenomes_pessoas = ["Silva", "Santos", "Oliveira", "Souza", "Pereira", "Lima", "Carvalho", "Ferreira", "Ribeiro", "Almeida"]

        # 4. Pegar todas as ordens de serviço
        cursor.execute("SELECT id FROM ordem_serv")
        os_ids = cursor.fetchall()
        
        if not os_ids:
            print("Nenhuma Ordem de Serviço encontrada.")
        else:
            updates = []
            for (os_id,) in os_ids:
                # Gerar nome de cliente aleatório
                if random.random() > 0.3: # 70% pessoa física
                    new_client = f"{random.choice(nomes_pessoas)} {random.choice(sobrenomes_pessoas)}"
                else: # 30% empresa
                    new_client = f"{random.choice(first_names)} {random.choice(last_names)}"
                
                # Selecionar técnico aleatório (se houver)
                new_tech = random.choice(tech_users) if tech_users else None
                
                if new_tech:
                    updates.append((new_client, new_tech, os_id))
                else:
                    # Se não tiver técnico, atualiza só o cliente? O usuário pediu os dois.
                    # Vou tentar atualizar só o cliente se não tiver técnicos, mas avisar.
                    pass 

            if tech_users:
                cursor.executemany("UPDATE ordem_serv SET cliente = ?, tecnico_responsavel = ? WHERE id = ?", updates)
                conn.commit()
                print(f"Sucesso! {len(updates)} Ordens de Serviço atualizadas.")
                
                # Mostrar amostra
                cursor.execute("SELECT id, cliente, tecnico_responsavel FROM ordem_serv LIMIT 5")
                for row in cursor.fetchall():
                    print(row)
            else:
                print("Não foi possível atualizar as OS pois não há técnicos válidos.")

    except Exception as e:
        print(f"Erro: {e}")
    finally:
        conn.close()