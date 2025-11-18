# VP Confeitaria Criativa 🧁

Aplicação Django simples para gerenciar precificações de projetos de confeitaria com insumos flexíveis, custos fixos e auditoria de ações.

Conteúdo deste README
- Visão geral das features
- Requisitos e como preparar o ambiente `.env`
- Passos para instalar, migrar e executar localmente (Windows PowerShell)
- Como testar rapidamente as funcionalidades principais
- Notas técnicas e próximos passos

Principais features
- Criar/editar/listar precificações com produtos/insumos armazenados em JSON (campo flexível).
- Formulário com tabela dinâmica para adicionar itens (jQuery).
- Busca por nome do cliente, tema do projeto ou nome da precificação (campo no navbar para usuários autenticados).
- Tabela de custos fixos e pró-labore com cálculos de custo mensal/diário/por hora/por minuto.
- Auditoria (model `History`) registrando create/update/delete para modelos principais.

Requisitos
- Python 3.10+ (ou versão compatível com Django 5.x)
- Virtualenv (você informou que o ambiente chama-se `.env`)

Instalação e execução (Windows PowerShell)

1) Ativar seu ambiente virtual `.env`:

```powershell
.\.env\Scripts\Activate.ps1
```

2) Instalar dependências:

```powershell
pip install -r requirements.txt
```

3) Criar e aplicar migrations:

```powershell
python manage.py makemigrations
python manage.py migrate
```

4) Criar um superuser para acessar o admin (útil para testar autenticação rapidamente):

```powershell
python manage.py createsuperuser
```

5) Rodar o servidor de desenvolvimento:

```powershell
python manage.py runserver
```

6) Acessar no navegador:
- Site: http://127.0.0.1:8000/
- Admin: http://127.0.0.1:8000/admin/

Testes rápidos (fluxos principais)
- Faça login (admin) e verifique se o menu exibe `Precificações`, `Custos` e `Histórico`.
- Criar nova precificação: menu → `Precificações` → `Nova Precificação`. Use a tabela dinâmica para adicionar insumos. Salve.
- Editar precificação: abra o detalhe da precificação e clique em `Editar`. A tabela deve carregar os itens previamente salvos.
- Custos: menu → `Custos` → adicione um custo fixo; verifique os cálculos (mensal/diário/hora/minuto).
- Histórico: menu → `Histórico` → veja as entradas criadas automaticamente (create/update/delete).

Notas técnicas
- O projeto usa `JSONField` para armazenar `produtos` em `Pricing` e `valores` em `FixedCost` para permitir flexibilidade na composição dos projetos.
- Auditoria: implementada via signals (`app/signals.py`) e um middleware thread-local (`app/middleware.py`) para identificar `request.user` nas signals. Isso funciona para operações realizadas via HTTP. Para jobs/background, pode ser necessário fornecer usuário explicitamente.
- Frontend: Bootstrap 5 e jQuery são incluídos via CDN no `templates/base.html` para acelerar o desenvolvimento.

Considerações e próximos passos sugeridos
- Restringir edição de uma precificação apenas ao usuário que a criou (owner-only). Posso implementar isso se desejar.
- Adicionar validação de schema para o JSON de `produtos` (server-side) e mensagens de erro amigáveis.
- Escrever testes unitários para modelos e views (fluxo create→edit→list).

Ajuda / debug rápido
- Se tiver problemas com "Couldn't import Django": verifique se o virtualenv `.env` está ativado e instale dependências (`pip install -r requirements.txt`).
- Se a tabela dinâmica não pré-carregar ao editar: abra o console do navegador (F12) e verifique erros de JavaScript e imprima no template `{{ produtos_json }}` para inspecionar o JSON recebido.

Se preferir, já implemento agora uma das opções acima (tests, validação JSON ou proteção owner-only). Diga qual prefere.

