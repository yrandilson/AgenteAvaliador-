import streamlit as st
import ollama

# ─────────────────────────────────────────────────────────────────────────────
# CONFIGURAÇÃO
# Modelo: gemma2:2b  (Google — mais leve e rápido, só 2GB de RAM)
# Para trocar: mude apenas esta linha
# Opções: "gemma2:2b" (mais rápido) | "gemma2:9b" (mais capaz, ~8GB)
# ─────────────────────────────────────────────────────────────────────────────
MODEL = "gemma2:2b"

# ─────────────────────────────────────────────────────────────────────────────
# SYSTEM PROMPT — personalidade e conhecimento do agente
# Este texto é enviado ao modelo antes de qualquer pergunta do usuário
# Define que o agente é especialista no AI Agent Index 2025
# ─────────────────────────────────────────────────────────────────────────────
SYSTEM_PROMPT = """Você é um agente especialista no AI Agent Index 2025 (arXiv:2602.17753),
publicado por pesquisadores do MIT, Stanford, Harvard e Cambridge.

O índice analisou 30 agentes de IA comerciais e acadêmicos usando 6 dimensões:
1. Produto        — o que o agente faz e para quem é destinado
2. Accountability — quem é responsável pelo sistema e sua transparência
3. Arquitetura    — memória, ferramentas, planejamento e multimodalidade
4. Autonomia      — nível de controle humano e mecanismos de supervisão
5. Ecossistema    — integrações, APIs e dados acessados
6. Segurança      — avaliações de risco, red-teaming e impactos sociais

Descoberta principal do índice: a maioria dos desenvolvedores compartilha
muito pouco sobre segurança e impactos sociais dos seus agentes.

Responda sempre em português brasileiro.
Seja claro, direto e estruturado. Máximo 300 palavras por resposta."""

# ─────────────────────────────────────────────────────────────────────────────
# CONFIGURAÇÃO DA PÁGINA STREAMLIT
# Deve ser a primeira chamada st.* do arquivo
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Agente Avaliador de IA",
    page_icon="🤖",
    layout="centered"
)

# ─────────────────────────────────────────────────────────────────────────────
# FUNÇÃO PRINCIPAL — chama o modelo local via Ollama
#
# Parâmetros:
#   prompt (str) — a pergunta ou texto do usuário
#   system (str) — instruções permanentes do agente (usa SYSTEM_PROMPT por padrão)
#
# Retorno:
#   str — texto da resposta gerada pelo modelo
#
# Fluxo interno:
#   1. Monta a lista de mensagens no formato que o Ollama espera
#   2. Envia para o modelo local rodando no servidor
#   3. Extrai e retorna apenas o texto da resposta
#   4. Em caso de erro, retorna mensagem de aviso sem travar o app
# ─────────────────────────────────────────────────────────────────────────────
def chamar_modelo(prompt: str, system: str = SYSTEM_PROMPT) -> str:
    try:
        resposta = ollama.chat(
            model=MODEL,
            messages=[
                {"role": "system", "content": system},  # instruções do agente
                {"role": "user",   "content": prompt}   # pergunta do usuário
            ]
        )
        # resposta["message"]["content"] é onde o Ollama guarda o texto gerado
        return resposta["message"]["content"]

    except Exception as e:
        # Captura qualquer erro (Ollama offline, modelo não instalado, etc.)
        return (
            f"❌ Erro ao conectar ao Ollama: {e}\n\n"
            f"Verifique se o Ollama está rodando com: `ollama serve`\n"
            f"E se o modelo está instalado com: `ollama pull {MODEL}`"
        )


# ─────────────────────────────────────────────────────────────────────────────
# FUNÇÃO COM STREAMING — mostra o texto aparecendo aos poucos, como no terminal
#
# Diferença para chamar_modelo(): em vez de esperar a resposta inteira pronta,
# usa stream=True no Ollama, que entrega o texto em pedaços (chunks) conforme
# o modelo gera. A cada pedaço, atualizamos a área de texto na tela.
#
# Parâmetros:
#   prompt (str)       — a pergunta ou texto do usuário
#   placeholder         — o espaço reservado na tela (st.empty()) onde o texto
#                          vai sendo escrito aos poucos
#   system (str)        — instruções permanentes do agente
#
# Retorno:
#   str — texto completo, depois de terminar de "digitar" na tela
# ─────────────────────────────────────────────────────────────────────────────
def chamar_modelo_streaming(prompt: str, placeholder, system: str = SYSTEM_PROMPT) -> str:
    texto_completo = ""
    try:
        # stream=True faz o Ollama devolver pedacinhos da resposta,
        # um chunk por vez, em vez de tudo de uma vez no final
        stream = ollama.chat(
            model=MODEL,
            messages=[
                {"role": "system", "content": system},
                {"role": "user",   "content": prompt}
            ],
            stream=True
        )

        # Cada "chunk" é um pedaço pequeno do texto sendo gerado
        for chunk in stream:
            pedaco = chunk["message"]["content"]
            texto_completo += pedaco

            # placeholder.markdown() substitui o conteúdo exibido a cada pedaço novo,
            # criando o efeito de "digitando" — o "▌" no final simula um cursor piscando
            placeholder.markdown(texto_completo + "▌")

        # Remove o cursor "▌" no final, deixando o texto limpo
        placeholder.markdown(texto_completo)
        return texto_completo

    except Exception as e:
        erro = (
            f"❌ Erro ao conectar ao Ollama: {e}\n\n"
            f"Verifique se o Ollama está rodando com: `ollama serve`\n"
            f"E se o modelo está instalado com: `ollama pull {MODEL}`"
        )
        placeholder.markdown(erro)
        return erro

# ─────────────────────────────────────────────────────────────────────────────
# INTERFACE — título e abas
# ─────────────────────────────────────────────────────────────────────────────
st.title("🤖 Agente Avaliador de IA")
st.caption(f"Modelo: `{MODEL}` (Google Gemma) via Ollama · AI Agent Index 2025 · arXiv:2602.17753")
st.divider()

# Cria as 3 abas — cada uma é uma funcionalidade do agente
aba1, aba2, aba3 = st.tabs(["📋 Avaliador", "🔍 Buscador", "⚖️ Comparador"])


# ═════════════════════════════════════════════════════════════════════════════
# ABA 1 — AVALIADOR
# Recebe a descrição de um agente e avalia nas 6 dimensões do índice
# ═════════════════════════════════════════════════════════════════════════════
with aba1:
    st.subheader("Avaliar um agente de IA")
    st.caption("Descreva qualquer agente e receba uma avaliação nas 6 dimensões do índice.")

    # Exemplos prontos para facilitar o uso
    # Dicionário: chave = nome exibido no menu, valor = texto que preenche o campo
    exemplos = {
        "Escolha um exemplo...": "",
        "ChatGPT":  "ChatGPT: assistente da OpenAI com busca na web, execução de código, memória de conversas e suporte a imagens.",
        "Gemini":   "Gemini Advanced: assistente do Google integrado ao Gmail, Docs e Drive, com suporte multimodal.",
        "Claude":   "Claude: assistente da Anthropic focado em segurança, com janela de contexto longa e uso de ferramentas.",
        "Copilot":  "Microsoft Copilot: assistente integrado ao Office 365, Teams e Windows, baseado em GPT-4.",
    }

    # Menu suspenso com os exemplos
    # st.selectbox retorna a chave selecionada pelo usuário
    escolha = st.selectbox("Exemplo rápido", list(exemplos.keys()))

    # session_state evita que o campo seja apagado quando a página recarrega
    if "descricao_avaliador" not in st.session_state:
        st.session_state.descricao_avaliador = ""

    # Atualiza o campo só quando o usuário troca a escolha no menu
    if escolha != "Escolha um exemplo...":
        st.session_state.descricao_avaliador = exemplos[escolha]

    # Campo de texto grande — ligado ao session_state via key=
    # O usuário pode editar o texto livremente sem perder o conteúdo
    descricao = st.text_area(
        "Descrição do agente",
        key="descricao_avaliador",
        height=120,
        placeholder="Ex: GPT-4o — modelo da OpenAI com visão, busca na web e execução de código..."
    )

    # Botão principal — só executa o bloco abaixo quando clicado
    if st.button("Avaliar agente ↗", type="primary", key="btn_avaliar"):

        if descricao.strip():  # garante que o campo não está vazio

            # Monta o prompt combinando a instrução com a descrição do usuário
            prompt = (
                f"Avalie este agente de IA nas 6 dimensões do AI Agent Index 2025:\n\n"
                f"{descricao}\n\n"
                f"Estruture a resposta com as 6 dimensões numeradas."
            )

            # st.empty() cria um espaço vazio na tela que pode ser atualizado
            # repetidamente — é nele que o texto vai "aparecer aos poucos"
            placeholder = st.empty()
            placeholder.markdown("▌")  # cursor piscando antes de começar a chegar texto

            # Chama o modelo em modo streaming — o texto vai sendo escrito
            # no placeholder em tempo real, como no terminal
            chamar_modelo_streaming(prompt, placeholder)

            st.success("Avaliação concluída!")

        else:
            st.warning("Digite a descrição do agente antes de avaliar.")


# ═════════════════════════════════════════════════════════════════════════════
# ABA 2 — BUSCADOR
# Responde perguntas sobre agentes de IA com base no AI Agent Index
# ═════════════════════════════════════════════════════════════════════════════
with aba2:
    st.subheader("Perguntas sobre agentes de IA")
    st.caption("Faça perguntas sobre o AI Agent Index, arquitetura de agentes ou segurança em IA.")

    # Lista de sugestões de perguntas
    sugestoes = [
        "Quais os principais riscos de segurança em agentes autônomos?",
        "O que é RAG e como agentes usam recuperação de documentos?",
        "Como funciona memória em agentes de IA modernos?",
        "Por que os desenvolvedores não divulgam informações de segurança?",
        "Qual a diferença entre agente autônomo e assistente tradicional?",
        "O que o AI Agent Index descobriu sobre transparência?",
    ]

    # Botões de sugestão organizados em 2 colunas
    # session_state guarda o valor entre recarregamentos da página —
    # sem isso, o campo "esquece" o texto quando o botão Buscar é clicado
    if "pergunta_buscador" not in st.session_state:
        st.session_state.pergunta_buscador = ""

    st.caption("💡 Clique para preencher:")
    cols = st.columns(2)

    # enumerate(sugestoes) retorna (índice, texto)
    # i % 2 alterna entre coluna 0 e coluna 1
    for i, s in enumerate(sugestoes):
        if cols[i % 2].button(s[:50] + "...", key=f"sug_{i}"):
            st.session_state.pergunta_buscador = s  # salva no session_state, não se perde

    # Campo de texto — ligado diretamente ao session_state via key=
    # Assim o valor digitado OU clicado fica salvo entre os reruns da página
    pergunta = st.text_area(
        "Sua pergunta",
        key="pergunta_buscador",
        height=80,
        placeholder="Ex: Quais são os riscos de segurança em agentes autônomos?"
    )

    if st.button("Buscar resposta ↗", type="primary", key="btn_buscar"):

        if pergunta.strip():
            # Instrui o modelo a responder com base no índice
            prompt = (
                f"Com base no AI Agent Index 2025 e no conhecimento atual sobre agentes de IA, "
                f"responda de forma clara e estruturada:\n\n{pergunta}"
            )

            placeholder = st.empty()
            placeholder.markdown("▌")
            chamar_modelo_streaming(prompt, placeholder)

        else:
            st.warning("Digite sua pergunta.")


# ═════════════════════════════════════════════════════════════════════════════
# ABA 3 — COMPARADOR
# Compara dois agentes lado a lado usando as 6 dimensões do índice
# ═════════════════════════════════════════════════════════════════════════════
with aba3:
    st.subheader("Comparar dois agentes de IA")
    st.caption("Compare dois sistemas lado a lado usando as 6 dimensões do AI Agent Index.")

    # Dois campos lado a lado usando colunas do Streamlit
    col1, col2 = st.columns(2)
    agente_a = col1.text_input("Agente A", placeholder="Ex: ChatGPT")
    agente_b = col2.text_input("Agente B", placeholder="Ex: Claude")

    if st.button("Comparar ↗", type="primary", key="btn_comparar"):

        # Valida que os dois campos estão preenchidos
        if agente_a.strip() and agente_b.strip():
            # O prompt instrui o modelo a comparar os dois agentes
            # nas mesmas 6 dimensões do índice
            prompt = (
                f"Compare '{agente_a}' e '{agente_b}' nas 6 dimensões do AI Agent Index 2025: "
                f"Produto, Accountability, Arquitetura, Autonomia, Ecossistema e Segurança. "
                f"Mostre as diferenças principais de forma clara. "
                f"Use uma estrutura organizada por dimensão."
            )

            placeholder = st.empty()
            placeholder.markdown("▌")
            chamar_modelo_streaming(prompt, placeholder)

        else:
            st.warning("Preencha os dois campos para comparar.")


# ─────────────────────────────────────────────────────────────────────────────
# RODAPÉ
# Informações fixas que aparecem em todas as abas
# ─────────────────────────────────────────────────────────────────────────────
st.divider()
st.caption(f"🖥️ Rodando localmente · Modelo: `{MODEL}` (Google Gemma) via Ollama · AI Agent Index 2025 · arXiv:2602.17753")
