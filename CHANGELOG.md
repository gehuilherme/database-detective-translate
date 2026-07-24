# Changelog

Todas as mudanças relevantes deste projeto são documentadas aqui.

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
