import sqlite3
import random
import shutil
import os

# Verificar se o arquivo existe
if os.path.exists('database/database.db'):
    # Criar uma cópia para não alterar o original caso algo dê errado, ou para fornecer um novo arquivo
    shutil.copy('database/database.db', 'database/database_updated.db')
    
    conn = sqlite3.connect('database/database_updated.db')
    cursor = conn.cursor()
    
    try:
        # Verificar se a tabela existe
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='componentes';")
        if not cursor.fetchone():
            print("Tabela 'componentes' não encontrada.")
        else:
            # Pegar todos os IDs
            cursor.execute("SELECT id FROM componentes")
            ids = cursor.fetchall()
            
            if not ids:
                print("Nenhum componente encontrado para atualizar.")
            else:
                # Gerar dados aleatórios e atualizar
                # quant entre 10 e 500
                # quant_min entre 5 e 50
                updates = []
                for (row_id,) in ids:
                    quant = random.randint(10, 500)
                    quant_min = random.randint(5, 50)
                    updates.append((quant, quant_min, row_id))
                
                cursor.executemany("UPDATE componentes SET quant = ?, quant_min = ? WHERE id = ?", updates)
                conn.commit()
                
                print(f"Sucesso! {len(ids)} itens atualizados.")
                print("Amostra dos dados atualizados (ID, Descrição, Quant, Quant_Min):")
                
                # Mostrar amostra, tentando pegar a descrição se existir a coluna descr
                try:
                    cursor.execute("SELECT id, descr, quant, quant_min FROM componentes LIMIT 5")
                except sqlite3.OperationalError:
                    # Caso descr não exista (improvável dado o contexto anterior, mas seguro)
                    cursor.execute("SELECT id, quant, quant_min FROM componentes LIMIT 5")
                    
                for row in cursor.fetchall():
                    print(row)

    except Exception as e:
        print(f"Ocorreu um erro: {e}")
    finally:
        conn.close()
else:
    print("Arquivo database.db não encontrado.")