# Documento de Requisitos – MVP do Zél.IA

**Versão:** 1.0
**Data:** 25 de junho de 2025

### 1. Visão Geral do Produto

O Zél.IA é um portal de chatbot centralizado, projetado para que os alunos do Centro Universitário Jorge Amado possam acessar informações básicas de forma direta, rápida e precisa, eliminando a necessidade de buscar em múltiplos documentos e páginas do site.

### 2. Objetivo do MVP

O objetivo principal deste MVP é **validar a viabilidade e aceitação** de um chatbot de IA para responder às dúvidas dos alunos. Especificamente, queremos:

1.  Confirmar que a tecnologia (arquitetura RAG) pode fornecer respostas precisas, utilizando como base de conhecimento um único documento: o **Manual do Aluno**.
2.  Aumentar a confiança do usuário na ferramenta, fornecendo a fonte exata da informação.
3.  Coletar dados de feedback sobre a qualidade das respostas para guiar as futuras iterações do produto.

### 3. Persona do Usuário Principal

* **Nome:** Jorge
* **Papel:** Aluno de graduação (especialmente calouros e alunos dos primeiros semestres).
* **Necessidades:** Precisa de respostas rápidas sobre prazos, regras de frequência, solicitação de documentos e procedimentos acadêmicos.
* **Frustrações:** Acha o site da universidade confuso e considera demorado e difícil encontrar informações específicas nos manuais em PDF.

### 4. Requisitos Funcionais (O que o sistema faz)

* **RF-001: Fazer uma Pergunta**
    * **Como um** aluno, **eu quero** digitar minha pergunta em uma caixa de texto e enviá-la, **para que** eu possa obter uma resposta para minha dúvida.

* **RF-002: Receber uma Resposta**
    * **Como um** aluno, **eu quero** ver a resposta gerada pela I.A. de forma clara na tela, **para que** eu possa entender a informação fornecida.

* **RF-003: Identificar a Fonte da Resposta**
    * **Como um** aluno, **eu quero** ver de qual parte do documento a resposta foi extraída (ex: "Fonte: Manual do Aluno, pág. 12"), **para que** eu possa confiar na informação e consultá-la na fonte original se necessário.

* **RF-004: Fornecer Feedback sobre a Resposta**
    * **Como um** aluno, **eu quero** poder clicar em um botão de "útil" (👍) ou "não útil" (👎) em cada resposta, **para que** eu possa ajudar a equipe a melhorar a precisão da ferramenta.

### 5. Requisitos Não-Funcionais (Como o sistema se comporta)

* **RNF-001: Desempenho:** A resposta do chatbot deve ser exibida em menos de 8 segundos após o envio da pergunta do usuário.
* **RNF-002: Usabilidade:** A interface deve ser limpa, intuitiva e responsiva, funcionando adequadamente em navegadores de desktop e mobile (design "mobile-first").
* **RNF-003: Fonte de Dados:** O sistema, nesta versão MVP, utilizará **apenas e exclusivamente** o documento `Manual_do_Aluno_2025.pdf` como sua base de conhecimento. Nenhuma outra fonte será consultada.
* **RNF-004: Privacidade:** O sistema não deve solicitar nem armazenar nenhuma informação de identificação pessoal do aluno. As interações e o feedback serão coletados de forma anônima.

### 6. Fora do Escopo (O que NÃO faremos agora)

As seguintes funcionalidades são **intencionalmente deixadas de fora do MVP** para garantir o foco e a entrega rápida de valor:

* **Histórico de conversas:** O usuário não poderá ver suas perguntas anteriores.
* **Sistema de login/contas de usuário:** A plataforma será de acesso público e anônimo.
* **Suporte a múltiplos documentos:** A IA responderá apenas com base no Manual do Aluno.
* **Notificações proativas.**
* **Fazer perguntas por voz.**
* **Integração com qualquer outro sistema da universidade.**