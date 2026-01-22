import os
import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np


def get_lenguages_used(repos: dict) -> dict:
    try:
        languages = {}
        for repo in repos:
            lang = repo.get("lenguage")
            if lang:
                languages[lang] = languages.get(lang, 0) + 1

        return languages
    
    except Exception as error:
        raise Exception(f"Erro {str(error)}")
    
def get_weekly_activity(events: dict) -> dict:
    try:

        df = pd.DataFrame(events)

        if df.empty: 
            return {}
        
        df["created_at"] = pd.to_datetime(df["created_at"])
        df["date"] = df["created_at"].dt.date
        df['day_of_week'] = str(df['created_at'].dt.day_name())
        df['hour'] = str(df['created_at'].dt.hour)

        daily_activity = df.groupby('date').size()

        event_types = df.groupby('type').size()

        return {
            'daily_activity': daily_activity,
            'event_types': event_types,
            'total_events': len(df)
        }
    
    except Exception as error:
        raise Exception(f"Erro {str(error)}")
    
def create_visualizations(data, languages):
    try:
        # Configuração do estilo
        plt.style.use('seaborn-v0_8-darkgrid')
        sns.set_palette("husl")

        # 1. Gráfico de Linguagens
        fig1, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

        # Pizza das linguagens
        if languages:
            labels = list(languages.keys())
            sizes = list(languages.values())
            ax1.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
            ax1.set_title('Linguagens Utilizadas', fontsize=14, fontweight='bold')
            ax1.axis('equal')

        # 2. Atividade Semanal (se houver dados)
        if 'daily_activity' in data and not data['daily_activity'].empty:
            days = data['daily_activity'].index[-7:]  # Últimos 7 dias
            values = data['daily_activity'].values[-7:]
            
            ax2.bar(range(len(days)), values, color='#2ea44f')
            ax2.set_title('Atividade Diária (Últimos 7 Dias)', fontsize=14, fontweight='bold')
            ax2.set_xlabel('Dias')
            ax2.set_ylabel('Eventos')
            ax2.set_xticks(range(len(days)))
            ax2.set_xticklabels([d.strftime('%d/%m') for d in days])

        plt.tight_layout()
        plt.savefig('charts/github_analytics.png', dpi=300, bbox_inches='tight')
        plt.close()

        if 'event_types' in data and not data['event_types'].empty:
            fig2, ax3 = plt.subplots(figsize=(10, 6))
            data['event_types'].plot(kind='bar', ax=ax3, color='#0366d6')
            ax3.set_title('Tipos de Atividade', fontsize=14, fontweight='bold')
            ax3.set_xlabel('Tipo de Evento')
            ax3.set_ylabel('Quantidade')
            plt.xticks(rotation=45)
            plt.tight_layout()
            plt.savefig('charts/activity_types.png', dpi=300, bbox_inches='tight')
            plt.close()
    except Exception as error:
        raise Exception(f"Erro {str(error)}")

def generate_linkedin_post(data, languages):
    """Gera o texto para o post no LinkedIn"""
    
    total_repos = len(data.get('repos', []))
    total_events = data.get('total_events', 0)
    
    # Encontra linguagem principal
    main_language = max(languages, key=languages.get) if languages else 'N/A'
    
    post = f"""🚀 Meu Relatório Semanal de Atividade no GitHub!

📊 **Resumo da Semana:**
• {total_events} eventos de desenvolvimento
• {total_repos} repositórios ativos
• Linguagem principal: {main_language}

💻 **Distribuição por Linguagem:**
"""
    
    for lang, count in sorted(languages.items(), key=lambda x: x[1], reverse=True):
        percentage = (count / total_repos) * 100 if total_repos > 0 else 0
        post += f"• {lang}: {count} repos ({percentage:.1f}%)\n"
    
    post += f"""
📈 **Insights:**
- Mantive consistência nos commits diários
- Trabalhei em {len(languages)} tecnologias diferentes
- Foco em qualidade do código e documentação

🔧 **Próximos Objetivos:**
1. Aumentar contribuições em projetos open-source
2. Explorar novas tecnologias na stack
3. Melhorar cobertura de testes

#GitHub #Desenvolvimento #Programação #Analytics #Tech 
#Python #DataScience #DevOps #OpenSource #CarreiraTech

👉 Veja os gráficos completos abaixo! ⬇️
"""
    
    return post

def convert_for_json(obj):
    """Converte objetos para formato serializável em JSON"""
    from datetime import date, datetime
    
    # Se for dict, converte chaves
    if isinstance(obj, dict):
        new_dict = {}
        for key, value in obj.items():
            # Converte chave para string se necessário
            if isinstance(key, (date, datetime)):
                new_key = key.isoformat()
            elif not isinstance(key, (str, int, float, bool, type(None))):
                new_key = str(key)
            else:
                new_key = key
            
            # Converte valor recursivamente
            new_dict[new_key] = convert_for_json(value)
        return new_dict
    
    # Se for lista, converte cada item
    elif isinstance(obj, list):
        return [convert_for_json(item) for item in obj]
    
    # Se for pandas Series/DataFrame
    elif isinstance(obj, pd.Series):
        # Converte Series para dict primeiro, depois processa
        return convert_for_json(obj.to_dict())
    elif isinstance(obj, pd.DataFrame):
        return convert_for_json(obj.to_dict('records'))
    
    # Se for date/datetime
    elif isinstance(obj, (date, datetime)):
        return obj.isoformat()
    
    # Se for numpy
    elif isinstance(obj, np.ndarray):
        return convert_for_json(obj.tolist())
    elif isinstance(obj, (np.integer, np.floating)):
        return obj.item()
    
    # Se for NaN
    elif pd.isna(obj):
        return None
    
    # Outros tipos (strings, números, booleanos, None)
    else:
        return obj

def save_data(data, filename='github_analysis.json'):
    """Salva os dados analisados em um arquivo JSON"""
    
    try:
        # Converte todos os dados
        serializable_data = convert_for_json(data)
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(serializable_data, f, ensure_ascii=False, indent=2)
        
        print(f"Dados salvos em {filename}")
        
    except Exception as error:
        print(f"Erro ao salvar dados: {error}")