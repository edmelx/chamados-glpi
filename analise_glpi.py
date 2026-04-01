import pandas as pd
import matplotlib
matplotlib.use('Agg')  # necessário para rodar sem interface gráfica no servidor
import matplotlib.pyplot as plt
import os

# Cria pasta para salvar os gráficos
os.makedirs('graficos', exist_ok=True)

# ── Carrega o CSV gerado pelo simular_glpi.py ──
df = pd.read_csv('chamados_glpi.csv')

# Converte as colunas de data para o tipo datetime
df['Data_abertura']  = pd.to_datetime(df['Data_abertura'])
df['Data_resolucao'] = pd.to_datetime(df['Data_resolucao'])

# Calcula o tempo de resolução em horas
df['horas_resolucao'] = (
    df['Data_resolucao'] - df['Data_abertura']
).dt.total_seconds() / 3600

# Extrai o mês de abertura para análise temporal
df['mes'] = df['Data_abertura'].dt.to_period('M')

# ── KPI 1: Chamados por status ──
por_status = df.groupby('Status').size().sort_values(ascending=False)
print('=== Chamados por Status ===')
print(por_status)

# ── KPI 2: Taxa de SLA por grupo (%) ──
sla_grupo = (
    df.groupby('Grupo_responsavel')['Dentro_SLA']
    .mean() * 100
).round(1)
print('\n=== Taxa de SLA por Grupo (%) ===')
print(sla_grupo)

# ── KPI 3: Tempo médio de resolução por prioridade ──
tempo_prio = (
    df.groupby('Prioridade')['horas_resolucao']
    .mean()
).round(1).sort_values()
print('\n=== Tempo Médio de Resolução por Prioridade (horas) ===')
print(tempo_prio)

# ── KPI 4: Chamados por mês ──
mensal = df.groupby('mes').size()
print('\n=== Chamados por Mês ===')
print(mensal)

# ════════════════════════════════════════
# GRÁFICOS
# ════════════════════════════════════════

fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle('Dashboard de Chamados GLPI', fontsize=16, fontweight='bold', y=1.01)

# ── Gráfico 1: Chamados por status ──
axes[0, 0].bar(
    por_status.index,
    por_status.values,
    color='#2E7D32'
)
axes[0, 0].set_title('Chamados por Status')
axes[0, 0].set_xlabel('Status')
axes[0, 0].set_ylabel('Quantidade')
axes[0, 0].tick_params(axis='x', rotation=30)

# ── Gráfico 2: Taxa de SLA por grupo ──
cores_sla = ['#2E7D32' if v >= 70 else '#E53935' for v in sla_grupo.values]
axes[0, 1].bar(
    sla_grupo.index,
    sla_grupo.values,
    color=cores_sla  # verde se >= 70%, vermelho se abaixo
)
axes[0, 1].set_title('Taxa de Cumprimento de SLA por Grupo (%)')
axes[0, 1].set_ylabel('%')
axes[0, 1].axhline(70, color='gray', linestyle='--', alpha=0.7, label='Meta 70%')
axes[0, 1].legend()
axes[0, 1].tick_params(axis='x', rotation=15)

# ── Gráfico 3: Tempo médio de resolução por prioridade ──
axes[1, 0].barh(
    tempo_prio.index,
    tempo_prio.values,
    color='#1565C0'
)
axes[1, 0].set_title('Tempo Médio de Resolução por Prioridade (horas)')
axes[1, 0].set_xlabel('Horas')

# ── Gráfico 4: Volume mensal de chamados ──
axes[1, 1].plot(
    mensal.index.astype(str),
    mensal.values,
    color='#2E7D32',
    linewidth=2,
    marker='o'
)
axes[1, 1].set_title('Volume Mensal de Chamados')
axes[1, 1].set_xlabel('Mês')
axes[1, 1].set_ylabel('Quantidade')
axes[1, 1].tick_params(axis='x', rotation=45)
axes[1, 1].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('graficos/dashboard_glpi.png', dpi=150, bbox_inches='tight')
plt.close()

print('\nGráfico salvo em graficos/dashboard_glpi.png')
print('Análise concluída!')