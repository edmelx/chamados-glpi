# chamados-glpi

https://lookerstudio.google.com/s/vtgUp23L8nI

# Dashboard de Chamados GLPI

Dashboard analítico de chamados de suporte técnico construído com Python e Looker Studio.

## Descrição

Projeto que simula um ambiente real de helpdesk no formato GLPI — sistema de chamados mais usado em empresas brasileiras de TI. Os dados foram gerados com Python e visualizados em um dashboard interativo no Looker Studio.

## Como funciona

### 1. Geração dos dados — `simular_glpi.py`
Script Python que usa a biblioteca `faker` para gerar 400 chamados fictícios, mas realistas, com os seguintes campos:
- ID, Título, Categoria, Tipo, Status, Prioridade
- Grupo responsável, Técnico, Solicitante
- Data de abertura e resolução
- Indicador de cumprimento de SLA (1 = dentro do prazo, 0 = fora)

As prioridades seguem SLAs reais de mercado:
| Prioridade | SLA |
|---|---|
| Muito alta | 2 horas |
| Alta | 8 horas |
| Média | 24 horas |
| Baixa | 72 horas |
| Muito baixa | 120 horas |

### 2. Análise dos dados — `analise_glpi.py`
Script que lê o CSV gerado e produz:
- KPIs no terminal (chamados por status, SLA por grupo, tempo médio de resolução)
- Gráfico PNG salvo em `graficos/dashboard_glpi.png` com 4 painéis

### 3. Dashboard no Looker Studio
O CSV foi conectado ao Looker Studio como fonte de dados. O dashboard conta com 5 painéis:
- **Scorecard** — total de chamados
- **Pizza** — distribuição por status (Novo, Em processamento, Pendente, Resolvido, Fechado)
- **Barras** — volume por categoria (Incidente, Requisição, Problema, Mudança)
- **Barras** — taxa de cumprimento de SLA por grupo (N1, N2, N3)
- **Barras** — distribuição por prioridade

## Stack
- Python 3.x
- Pandas
- Matplotlib
- Faker
- Looker Studio (Google)

## Instalação
```bash
pip install faker pandas matplotlib
```

## Execução
```bash
# 1. Gerar os dados simulados
python simular_glpi.py

# 2. Gerar análise e gráficos
python analise_glpi.py
```

## Estrutura do projeto
```
chamados-glpi/
├── simular_glpi.py        # gerador de dados fictícios
├── analise_glpi.py        # análise e geração de gráficos
├── requirements.txt       # dependências do projeto
├── chamados_glpi.csv      # dados gerados
├── graficos/
│   └── dashboard_glpi.png # gráfico gerado pelo script
└── README.md
```

## Contexto

GLPI é amplamente utilizado em empresas brasileiras para gestão de chamados de TI, infraestrutura e helpdesk. Este projeto demonstra a capacidade de modelar, gerar e analisar dados no formato de um sistema real, aplicando KPIs usados por times de operações e suporte técnico.
