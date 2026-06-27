# 🤖 Agente Avaliador de IA

**Trabalho Final — Tópicos em Sistemas de Informação (Agentes)**  
Universidade Federal do Ceará — UFC Quixadá · Sistemas de Informação · 2026

---

## Sobre o projeto

Sistema de agente de IA baseado nas **6 dimensões do [AI Agent Index 2025](https://arxiv.org/abs/2602.17753)** (MIT · Stanford · Harvard · Cambridge · arXiv:2602.17753), que analisou 30 agentes de IA implantados comercialmente em 2025.

O agente possui 3 funcionalidades:

| Funcionalidade | Descrição |
|---|---|
| 📋 **Avaliador** | Recebe a descrição de qualquer agente de IA e avalia nas 6 dimensões do índice |
| 🔍 **Buscador** | Responde perguntas sobre agentes de IA com base no AI Agent Index |
| ⚖️ **Comparador** | Compara dois agentes lado a lado pelas mesmas 6 dimensões |

---

## As 6 dimensões do AI Agent Index

1. **Produto** — o que o agente faz e para quem é destinado
2. **Accountability** — quem é responsável pelo sistema e sua transparência
3. **Arquitetura** — memória, ferramentas, planejamento e multimodalidade
4. **Autonomia** — nível de controle humano e mecanismos de supervisão
5. **Ecossistema** — integrações, APIs e dados acessados
6. **Segurança** — avaliações de risco, red-teaming e impactos sociais

---

## Stack tecnológico

- **Python 3.x** — linguagem principal
- **Streamlit** — interface web
- **Ollama** — execução local do modelo de linguagem
- **Gemma 2:2b** (Google) — modelo de IA leve (1.6GB), 100% local, sem custo de API

---

## Como executar

### Pré-requisitos

1. Instalar Python: [python.org/downloads](https://www.python.org/downloads/)  
   ⚠️ Marcar **"Add Python to PATH"** durante a instalação

2. Instalar Ollama: [ollama.com/download](https://ollama.com/download)

3. Baixar o modelo Gemma (no terminal):
```bash
ollama pull gemma2:2b
```

4. Instalar dependências Python:
```bash
pip install -r requirements.txt
```

### Executar

```bash
# Iniciar o Ollama (se não iniciar automaticamente)
ollama serve

# Em outro terminal, rodar o sistema
streamlit run app.py
```

O Streamlit abre automaticamente no navegador padrão.

---

## Estrutura do projeto

```
agente-ai-index/
├── app.py            ← código principal (comentado linha a linha)
├── requirements.txt  ← dependências Python
├── .gitignore        ← arquivos ignorados pelo git
└── README.md         ← este arquivo
```

---

## Referência principal

> STAUFER, L. et al. **The 2025 AI Agent Index**: Documenting Technical and Safety Features of Deployed Agentic AI Systems. MIT, Stanford, Harvard, Cambridge. arXiv:2602.17753, 2026.  
> 📄 PDF: https://arxiv.org/pdf/2602.17753  
> 🌐 Site: https://aiagentindex.mit.edu  
> 📊 Dataset: https://zenodo.org/records/19592546

---

## Autor

**Iran** — github.com/yrandilson  
UFC Quixadá · Sistemas de Informação
