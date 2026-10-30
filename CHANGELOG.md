# Changelog

Todas as mudanças relevantes deste projeto são documentadas aqui.

## [0.3] - 2026-10-29

### Corrigido
- **Crash ao abrir no Unity `6000.5.5f1`** (issues #1 e #4). O pacote agora inclui `BepInEx/config/BepInEx.cfg` com o ponto de entrada `Type = MonoBehaviour`: com o padrão (`Application`), o BepInEx iniciava os plugins antes de o motor estar pronto e o jogo fechava ao carregar o XUnity.AutoTranslator ou o plugin de fonte.
- Plugin de fonte: espera um frame antes de acessar o TextMeshPro (não toca mais no TMP de forma síncrona dentro do `Awake`).
- Plugin de fonte compila no Unity `6000.5`: `GetInstanceID()` → `GetHashCode()` e `enableWordWrapping` → `textWrappingMode`.

### Alterado
- O `.zip` passa a incluir as traduções da v0.2 (PR #3), que foi publicada sem pacote `.zip`.

## [0.2] - 2026-10-22

### Corrigido
- **Dados de tabela que estavam traduzidos voltam ao original (102 entradas removidas).** O critério é o próprio jogo: foram extraídos os TextAssets de dados (`players`, `payup`, `movies`, `profiles`, `foods`, `squadrons`…) e o bloco de `Scripts.dll` que preenche as tabelas. Entre os casos: `AS SELECT * FROM`, `CREATE TABLE IF NOT EXISTS`, colunas `date_created`/`time_created`, identificadores (`brochure_1`, `suspect_17432`, `stolen_weapon`…), notas de transação do payup, títulos de filmes/perfis e listas de valores.
- **Nomes e formatos que o jogador digita nas consultas, restaurados dentro das frases:** usuários (`goldtooth`, `fatcat`, `moneyman`, `bobert`, `grinch`), a pista `"member"`/`"donation"` do caso CA$H BOY$, `payup`, `Knights Against Darkness`, `RARE BURNING SWORD`, `Dark Forests`, moeda (`$200`), horas (`8:00`, `6:30`, `10 PM`), datas (`June 30th`) e números (`1000`).
- **Quebras de linha recolocadas em ~200 entradas** (`hints`, `mt`) que tinham virado um bloco só. Só mudam espaços e quebras; o texto continua palavra por palavra igual. A transcrição de áudio do início também recuperou uma frase que tinha sumido.

### Adicionado
- `DatabaseDetective_queryhints_ptbr.txt`: as 100 dicas de consulta do TextAsset `query-hints`, que não tinham tradução. Linhas de SQL, nomes de tabela/coluna e valores ficam idênticos ao original; `=` escapado como `\=`.
- `DatabaseDetective_ui5_ptbr.txt`: textos de interface, do assistente, títulos de mensagens e mensagens de erro do parser (LIMIT/OFFSET/HAVING/GROUP BY…) que não tinham tradução. As entradas que já eram cobertas pelos regex existentes ficaram de fora.
- A dica `8;8;5` ("To find the largest shareholder…"), que era a única sem tradução no `hints`.

## [0.1] - 2026-07-24

Primeira versão pública. Tradução ampla e jogável para PT-BR.

### Adicionado
- Estrutura de mod baseada em **BepInEx 5.4.23.5 + XUnity.AutoTranslator 5.6.1**, validada no Unity `6000.4.3f1` (Mono), em modo **offline** (só dicionários locais, dados de jogo preservados em inglês).
- **~1000+ entradas de tradução** distribuídas em dicionários:
  - Traduzido **à mão**: núcleo/UI, Configurações, tutorial e diálogos do assistente, 39 briefings/reações do chefe, mensagens de erro do parser SQL, notificações, nomes dos 10 casos, navegação do manual, **138 dicas de caso**.
  - Traduzido por **bootstrap automático** (revisável): conteúdo dos ~90 sites fictícios, avaliações e lore.
- **Plugin `DatabaseDetective.PTBR.Font`**:
  - Registra a fonte **Pixelify Sans** (OFL) como *fallback* do TextMeshPro para renderizar acentos em pixel-art.
  - Força **quebra de linha** e **auto-ajuste de tamanho** em textos longos, excluindo campos de entrada (a caixa de consulta SQL fica intacta).

### Corrigido
- Remoção de **255 chaves duplicadas** em que a tradução automática (sem quebras de linha) sobrepunha a tradução à mão (com quebras), causando texto em uma linha só que estourava a tela.
- Desligado o redimensionamento de UI do XUnity.AutoTranslator, que alargava caixas de texto até a largura da tela.

### Limitações conhecidas
- Conteúdo dos sites/lore é tradução automática (rascunho), sujeito a revisão.
- Formulário de prisão ("ARREST WARRANT") ainda em inglês.
- Alguns rótulos apertados podem cortar em telas específicas.
