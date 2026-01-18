import sqlite3
import random
import shutil
import os

# Define input and output filenames
input_db = 'database/database.db'
output_db = 'database/database_pedidos.db'

# Check if the input file exists
if os.path.exists(input_db):
    # Create a copy to work on
    shutil.copy(input_db, output_db)
    conn = sqlite3.connect(output_db)
    cursor = conn.cursor()

    try:
        # 1. Fetch all registered users
        cursor.execute("SELECT username FROM user")
        users = [row[0] for row in cursor.fetchall()]

        if not users:
            print("Nenhum usuário encontrado na tabela 'user'. Não é possível atualizar requisitantes.")
        else:
            print(f"Usuários encontrados: {len(users)}")

            # 2. Update 'pedidos' table
            # Fetch all pedido IDs to iterate and update individually for randomization
            cursor.execute("SELECT id FROM pedidos")
            pedido_ids = cursor.fetchall()

            if not pedido_ids:
                print("Nenhum pedido encontrado na tabela 'pedidos'.")
            else:
                updates = []
                for (pid,) in pedido_ids:
                    # Random user for requisitante
                    random_user = random.choice(users)
                    # Fixed user for comprador
                    fixed_comprador = "comprador1"
                    
                    updates.append((random_user, fixed_comprador, pid))
                
                # Execute batch update
                cursor.executemany("UPDATE pedidos SET requisitante = ?, comprador = ? WHERE id = ?", updates)
                conn.commit()
                
                print(f"Sucesso! {len(pedido_ids)} pedidos atualizados.")
                
                # 3. Show sample
                print("\nAmostra da tabela 'pedidos' atualizada (ID, Requisitante, Comprador):")
                cursor.execute("SELECT id, requisitante, comprador FROM pedidos LIMIT 5")
                for row in cursor.fetchall():
                    print(row)

    except Exception as e:
        print(f"Erro ao manipular o banco de dados: {e}")
    finally:
        if conn:
            conn.close()
else:
    print(f"Arquivo {input_db} não encontrado.")