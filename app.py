#!/usr/bin/env python3
"""
Matomo MCP Chat Interface
Talk to your website analytics in natural language.

Author: GalacticaIA / Ronald Mego
"""

import os
import json
import streamlit as st
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate
from langchain.tools import Tool

# Import MCP tools
from server import (
    get_visits_summary,
    get_top_pages,
    get_referrers,
    get_countries,
    get_devices,
    get_live_visitors,
    get_search_keywords,
    get_weekly_comparison,
    get_site_info,
)

load_dotenv()

# Page config
st.set_page_config(
    page_title="Matomo Analytics Chat",
    page_icon="📊",
    layout="wide",
)

# Custom CSS
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
    }
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(90deg, #7c3aed, #ea580c);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        text-align: center;
        color: #94a3b8;
        margin-bottom: 2rem;
    }
    .stat-card {
        background: rgba(255,255,255,0.05);
        border-radius: 12px;
        padding: 1.5rem;
        border: 1px solid rgba(255,255,255,0.1);
    }
    .stat-value {
        font-size: 2rem;
        font-weight: 700;
        color: #7c3aed;
    }
    .stat-label {
        color: #94a3b8;
        font-size: 0.9rem;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<h1 class="main-header">📊 Matomo Analytics Chat</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Habla con tus analytics en lenguaje natural</p>', unsafe_allow_html=True)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Create tools for LangChain
tools = [
    Tool(
        name="get_visits_summary",
        func=lambda x: json.dumps(get_visits_summary(**json.loads(x)) if x.strip() else get_visits_summary()),
        description="Get visit summary for a site. Input: JSON with 'site' (ronaldmego/galacticaia/becgi) and 'period' (today/yesterday/week/month/year/last 7 days/last 30 days)"
    ),
    Tool(
        name="get_top_pages",
        func=lambda x: json.dumps(get_top_pages(**json.loads(x)) if x.strip() else get_top_pages()),
        description="Get top visited pages. Input: JSON with 'site', 'period', 'limit'"
    ),
    Tool(
        name="get_referrers",
        func=lambda x: json.dumps(get_referrers(**json.loads(x)) if x.strip() else get_referrers()),
        description="Get traffic sources/referrers. Input: JSON with 'site', 'period', 'limit'"
    ),
    Tool(
        name="get_countries",
        func=lambda x: json.dumps(get_countries(**json.loads(x)) if x.strip() else get_countries()),
        description="Get visitor countries. Input: JSON with 'site', 'period', 'limit'"
    ),
    Tool(
        name="get_devices",
        func=lambda x: json.dumps(get_devices(**json.loads(x)) if x.strip() else get_devices()),
        description="Get device breakdown (desktop/mobile/tablet). Input: JSON with 'site', 'period'"
    ),
    Tool(
        name="get_live_visitors",
        func=lambda x: json.dumps(get_live_visitors(**json.loads(x)) if x.strip() else get_live_visitors()),
        description="Get live visitor count in last N minutes. Input: JSON with 'site', 'minutes'"
    ),
    Tool(
        name="get_search_keywords",
        func=lambda x: json.dumps(get_search_keywords(**json.loads(x)) if x.strip() else get_search_keywords()),
        description="Get search keywords that brought visitors. Input: JSON with 'site', 'period', 'limit'"
    ),
    Tool(
        name="get_weekly_comparison",
        func=lambda x: json.dumps(get_weekly_comparison(**json.loads(x)) if x.strip() else get_weekly_comparison()),
        description="Compare this week vs last week. Input: JSON with 'site' (optional)"
    ),
    Tool(
        name="get_site_info",
        func=lambda x: json.dumps(get_site_info()),
        description="Get information about the tracked site. No input needed."
    ),
]


@st.cache_resource
def get_agent():
    """Create the LangChain agent."""
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-pro",
        temperature=0.3,
    )
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", """Eres un asistente de analytics que ayuda a entender el rendimiento de sitios web.
        
Tienes acceso a Matomo Analytics. El sitio principal es ronaldmego.com.

Cuando el usuario pregunte sobre analytics:
1. Usa las herramientas disponibles para obtener datos reales
2. Presenta los datos de forma clara y amigable
3. Ofrece insights cuando sea relevante
4. Responde en español

Para las herramientas, envía los parámetros como JSON. Ejemplo: {{"site": "ronaldmego", "period": "today"}}
Si no se especifica el sitio, usa ronaldmego por defecto.
Si no se especifica el período, usa "today" por defecto."""),
        ("placeholder", "{chat_history}"),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}"),
    ])
    
    agent = create_tool_calling_agent(llm, tools, prompt)
    return AgentExecutor(agent=agent, tools=tools, verbose=True)


# Sidebar with quick stats
with st.sidebar:
    st.markdown("### 🚀 Quick Stats")
    
    try:
        # Get today's stats for ronaldmego.com
        stats = get_visits_summary("ronaldmego", "today")
        
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-value">{stats['unique_visitors']}</div>
            <div class="stat-label">Visitantes únicos hoy</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="stat-card" style="margin-top: 1rem;">
            <div class="stat-value">{stats['pageviews']}</div>
            <div class="stat-label">Pageviews</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="stat-card" style="margin-top: 1rem;">
            <div class="stat-value">{stats['bounce_rate']}</div>
            <div class="stat-label">Bounce Rate</div>
        </div>
        """, unsafe_allow_html=True)
        
    except Exception as e:
        st.error(f"Error loading stats: {e}")
    
    st.markdown("---")
    st.markdown("### 💡 Ejemplos")
    st.markdown("""
    - "¿Cómo va mi sitio hoy?"
    - "¿Cuántas visitas tuve esta semana?"
    - "¿De qué países vienen las visitas?"
    - "¿Cuáles son las páginas más vistas?"
    - "¿Hay alguien en el sitio ahora?"
    """)

# Chat interface
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Pregunta sobre tus analytics..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Get agent response
    with st.chat_message("assistant"):
        with st.spinner("Consultando Matomo..."):
            try:
                agent = get_agent()
                response = agent.invoke({
                    "input": prompt,
                    "chat_history": [],
                })
                answer = response["output"]
                st.markdown(answer)
                st.session_state.messages.append({"role": "assistant", "content": answer})
            except Exception as e:
                error_msg = f"Error: {str(e)}"
                st.error(error_msg)
                st.session_state.messages.append({"role": "assistant", "content": error_msg})
