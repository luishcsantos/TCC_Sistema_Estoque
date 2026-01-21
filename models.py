from peewee import *
from werkzeug.security import generate_password_hash, check_password_hash
import os
from datetime import date

# Caminho para o banco de dados
db_path = "database/database.db"

# Cria o banco de dados, caso não exista
if not os.path.exists("database"):
    os.makedirs("database")

db = SqliteDatabase(db_path, timeout=30)


class BaseModel(Model):
    class Meta:
        database = db


class User(BaseModel):
    username = CharField(unique=True)
    password_hash = CharField()
    access_level = CharField()

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @property
    def access_level_description(self):
        if self.access_level == "admin":
            return "Administrador"
        elif self.access_level == "comprador":
            return "Comprador"
        elif self.access_level == "almoxarifado":
            return "Almoxarifado"
        elif self.access_level in ("vendedor_serv","vendedor_repos"):
            return "Vendedor"
        elif self.access_level == "RH":
            return "RH"
        elif self.access_level == "Comprador_gerencia":
            return "Comprador/Gerência"
        elif self.access_level == "Diretoria":
            return "Diretoria"
        else:
            return "Usuário"


class Componentes(BaseModel):
    id = PrimaryKeyField()
    descr = CharField(unique=True)
    categ = CharField()
    encaps = CharField()
    quant = IntegerField()
    quant_min = IntegerField()
    local = CharField()
    cod_ant = CharField()
    obs = CharField()

    class Meta:
     database = db
     table_name = "componentes"


class Categoria(Model):
    id_categ = AutoField()
    categ = CharField(unique=True)
    
    class Meta:
        database = db
        table_name = 'categoria'

class Encapsulamento(Model):
    id_pack = AutoField()
    pack = CharField(unique=True)
    
    class Meta:
        database = db
        table_name = 'encapsulamento'


class Pedidos(BaseModel):
    id = PrimaryKeyField()
    data = DateTimeField()
    componentes = CharField()
    link_componentes = CharField()
    fornecedor = CharField()
    quant = IntegerField()
    urgente = BooleanField()
    requisitante = CharField()
    motivo = CharField(null=True, default="")
    comprado = BooleanField()
    comprador = CharField()
    data_compra = DateTimeField(null=True, default=None)
    data_chegada = DateTimeField(null=True, default=None)
    status = BooleanField()
    obs = CharField(null=True, default="")

    class Meta:
        database = db
        table_name = "pedidos"


class Sgp(BaseModel):
    id = PrimaryKeyField()
    data = DateField(null=True)
    vendedor = CharField(null=True)
    descricao = TextField(null=True)
    numero_pedido = CharField(null=True)
    cliente = CharField()
    previsao_entrega = DateField(null=True)
    observacao1 = TextField(null=True)
    almox_ciente = BooleanField(default=False)
    data_separacao = DateField(null=True)
    observacao2 = TextField(null=True)
    forma_entrega = CharField(null=True)
    finalizado_em = DateField(null=True)
    nota_fiscal = CharField(null=True)

    class Meta:
        database = db
        table_name = "sgp"


class OrdemServ(BaseModel):
    id = PrimaryKeyField()
    data_abertura = DateField(default=date.today)
    status = CharField()
    n_os = FloatField(unique=True)
    cliente = CharField()
    equipamento = TextField()
    tecnico_responsavel = CharField()
    valor_servico = FloatField(null=True)
    data_aprovacao = DateField(null=True)
    tempo_conserto = FloatField(null=True)
    data_entrega = DateField(null=True)
    dias_atraso = IntegerField(null=True)
    observacoes = TextField(null=True)

    class Meta:
        database = db
        table_name = "ordem_serv"
        

# Função para criar todas as tabelas do banco de dados
def create_database_and_tables():
    try:
        # Conecta ao banco de dados
        db.connect()

        # Cria todas as tabelas se elas não existirem
        db.create_tables([User, Componentes, Categoria, Encapsulamento, Pedidos, Sgp, OrdemServ], safe=True)
        print("✅ Banco de dados e todas as tabelas criados com sucesso!")
    except Exception as e:
        print(f"❌ Erro ao criar banco de dados e tabelas: {e}")
    finally:
        # Fecha a conexão com o banco de dados
        if not db.is_closed():
            db.close()

create_database_and_tables()