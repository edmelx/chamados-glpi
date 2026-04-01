import pandas as pd
import random
from faker import Faker
from datetime import datetime, timedelta

# Inicializa o gerador de dados fictícios em português brasileiro
fake = Faker('pt_BR')

# ── Listas de opções para os campos ──
categorias  = ['Incidente', 'Requisicao', 'Problema', 'Mudanca']
tipos       = ['Hardware', 'Software', 'Rede', 'Impressora', 'Acesso']
status_list = ['Novo', 'Em processamento', 'Pendente', 'Resolvido', 'Fechado']
prioridades = ['Muito baixa', 'Baixa', 'Media', 'Alta', 'Muito alta']
grupos      = ['N1 - Suporte', 'N2 - Infraestrutura', 'N3 - Desenvolvimento']

# SLA em horas por prioridade (tempo máximo para resolver)
sla_horas = {
    'Muito alta': 2,
    'Alta':       8,
    'Media':      24,
    'Baixa':      72,
    'Muito baixa':120,
}

registros = []

for i in range(1, 401):  # gera 400 chamados
    # Data de abertura aleatória nos últimos 12 meses
    abertura = fake.date_time_between(start_date='-12M', end_date='now')

    # Prioridade aleatória
    prio = random.choice(prioridades)

    # Tempo de resolução — entre 50% e 250% do SLA (alguns dentro, outros fora)
    horas = sla_horas[prio] * random.uniform(0.5, 2.5)
    fechamento = abertura + timedelta(hours=horas)

    # Verifica se foi resolvido dentro do SLA
    dentro_sla = 1 if horas <= sla_horas[prio] else 0

    registros.append({
        'ID':                i,
        'Titulo':            fake.sentence(nb_words=6),
        'Categoria':         random.choice(categorias),
        'Tipo':              random.choice(tipos),
        'Status':            random.choice(status_list),
        'Prioridade':        prio,
        'Grupo_responsavel': random.choice(grupos),
        'Tecnico':           fake.name(),
        'Solicitante':       fake.name(),
        'Data_abertura':     abertura.strftime('%Y-%m-%d %H:%M'),
        'Data_resolucao':    fechamento.strftime('%Y-%m-%d %H:%M'),
        'Dentro_SLA':        dentro_sla,
    })

# Salva o CSV gerado
df = pd.DataFrame(registros)
df.to_csv('chamados_glpi.csv', index=False)

print(f'CSV gerado com {len(df)} chamados!')
print(df.head())