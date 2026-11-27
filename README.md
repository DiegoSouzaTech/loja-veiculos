# Recife Motors — Showroom Automotivo Digital (White-Label)

Aplicação web responsiva desenvolvida em **Django** e **Tailwind CSS** para gestão de estoque automotivo e conversão direta de leads via WhatsApp. Projetada com arquitetura **White-Label** para fácil adaptação de marca, paleta de cores e domínio para diferentes lojas de veículos.

## Principais Funcionalidades

- **Vitrine Showroom Dark (Mobile-First):**
  - Carrossel horizontal magnético (`snap-x`) na página inicial para navegação fluida em smartphones.
  - Catálogo completo com cards horizontais compactos no mobile, busca por modelo e filtro por marca.
  - Ficha técnica detalhada separando **Ano de Fabricação** e **Ano do Modelo**, galeria interativa de fotos e formatação monetária brasileira (`R$`).
- **Conversão Direta no WhatsApp:**
  - Formulário de interesse na página do veículo (financiamento, troca ou compra à vista) que registra o lead no banco de dados e redireciona para o WhatsApp com mensagem pré-preenchida.
  - Página dedicada para avaliação de veículo usado na troca.
  - Botão flutuante responsivo para atendimento imediato.
- **Painel Administrativo (`/gestao/`):**
  - Gerenciamento completo de veículos, upload de múltiplas fotos com definição de capa, marcas e acompanhamento de leads capturados.
- **Identidade Visual White-Label:**
  - Variáveis centralizadas em `static/css/theme.css` e dados institucionais configuráveis via `.env`.

## Stack Tecnológica

- **Backend:** Python 3.13, Django 5.2
- **Frontend:** Django Templates, Tailwind CSS, CSS Custom Properties (`theme.css`)
- **Banco de Dados:** SQLite (desenvolvimento) / PostgreSQL (produção)
- **Configuração:** `python-dotenv`

## Como Executar Localmente

1. **Clone o repositório e acesse a pasta:**
   ```powershell
   git clone [https://github.com/DiegoSouzaTech/loja-veiculos.git](https://github.com/DiegoSouzaTech/loja-veiculos.git)
   cd loja-veiculos
   ```
