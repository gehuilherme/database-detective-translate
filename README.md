# Database Detective — Tradução PT-BR (Português do Brasil)

Mod de tradução **não-oficial** para o jogo **[Database Detective](https://store.steampowered.com/)** (HsuCorp), levando a interface, os diálogos, os erros de SQL, as mensagens, as dicas e o conteúdo dos sites fictícios para **Português do Brasil**.

> ⚠️ **Versão 0.3** — tradução ampla e jogável. O núcleo do jogo (história, tutorial, erros de SQL, UI, dicas) foi traduzido **à mão**; o conteúdo mais extenso dos sites/lore usa uma **tradução automática revisável** (veja [Limitações](#limitações-conhecidas)).

Não afiliado à HsuCorp. Feito por fãs, para fãs.

---

## Como funciona

O jogo é feito em **Unity 6 (Mono)** e não tem sistema de idiomas. A tradução é aplicada em **tempo de execução**, sem alterar nenhum arquivo do jogo, usando três peças:

1. **[BepInEx](https://github.com/BepInEx/BepInEx)** — carregador de mods para Unity.
2. **[XUnity.AutoTranslator](https://github.com/bbepis/XUnity.AutoTranslator)** — intercepta o texto do TextMeshPro e o substitui pelas traduções dos dicionários em `BepInEx/Translation/pt/Text/`. Configurado em **modo offline** (`Endpoint=` vazio): só o que está nos dicionários é traduzido, então **os dados consultáveis das tabelas (nomes, valores, palavras-chave SQL) permanecem em inglês** e os enigmas de SQL continuam funcionando.
3. **Plugin próprio** (`DatabaseDetective.PTBR.Font`) — resolve dois problemas de localização:
   - A fonte pixel do jogo não tem glifos acentuados. O plugin registra a **Pixelify Sans** (fonte pixel com acentos, licença OFL) como *fallback* do TextMeshPro, então `á ã ç é õ ú` aparecem em pixel-art, combinando com o estilo.
   - O português é mais longo que o inglês. O plugin força **quebra de linha** e **auto-ajuste de tamanho** em textos longos (sem tocar na caixa de consulta SQL).

---

## Requisitos

- **Database Detective** instalado (testado no Unity `6000.4.3f1` e `6000.5.5f1`, build Steam `25775427`).
- Windows 64-bit.

---

## Instalação (fácil)

1. Baixe o `.zip` da versão mais recente em **[Releases](../../releases)**.
2. Abra a pasta do jogo:
   - Steam → clique com o botão direito em **Database Detective** → **Gerenciar** → **Ver arquivos locais**.
3. **Extraia o conteúdo do `.zip` dentro da pasta do jogo** (onde está o `copOS.exe`), mantendo a estrutura de pastas. Aceite substituir, se perguntar.
4. Abra o jogo normalmente. Pronto — está em português.

### O jogo fecha/crasha ao abrir?

A partir do Unity `6000.5.5f1` o BepInEx precisa carregar os plugins mais tarde. O `.zip` (v0.3+) já traz o `BepInEx/config/BepInEx.cfg` certo; se você instalou uma versão antiga, extraia o `.zip` novo por cima **aceitando substituir**, ou edite `BepInEx/config/BepInEx.cfg` à mão:

```ini
[Preloader.Entrypoint]
Assembly = UnityEngine.CoreModule.dll
Type = MonoBehaviour
Method = .cctor
```

(O padrão do BepInEx é `Type = Application`, que inicia os plugins antes de o motor estar pronto e derruba o jogo. Diagnóstico de @Duarrt na issue #1.)

### Desinstalar

Apague (ou renomeie) o arquivo **`winhttp.dll`** na pasta do jogo. Isso desativa o mod sem remover nada do jogo. Para remover por completo, apague também a pasta `BepInEx`, o `doorstop_config.ini` e o `.doorstop_version`.

---

## O que está traduzido

- ✅ Interface, menus, **Configurações**, barra de tarefas, ícones do desktop
- ✅ Tutorial e diálogos do assistente (o "moleman")
- ✅ Briefings e reações do chefe em todos os casos
- ✅ **Mensagens de erro do parser SQL** (grande valor didático)
- ✅ Depoimentos, pistas e **dicas de cada caso**
- ✅ Notificações, confirmações e validações
- ✅ Nomes dos 10 casos e navegação do manual
- ✅ Conteúdo dos ~90 sites fictícios, avaliações e lore *(tradução automática — em revisão)*
- 🚫 **Dados de jogabilidade mantidos em inglês de propósito** (nomes de pessoas, comidas, materiais, memorandos de transações, nomes de tabelas/colunas, palavras-chave SQL) — para não quebrar as consultas que você digita.

## Limitações conhecidas

- O conteúdo dos sites/lore é **tradução automática** (rascunho) e pode ter trechos imperfeitos.
- O **formulário de prisão** ("ARREST WARRANT") ainda está em inglês (texto em rich-text que será tratado numa próxima versão).
- Alguns rótulos apertados podem cortar/vazar em telas específicas — reporte via *Issues*.

---

## Estrutura do repositório

```
translations/   → dicionários de tradução (formato XUnity.AutoTranslator)
config/          → AutoTranslatorConfig.ini (configuração usada)
src/plugin/      → código-fonte do plugin de fonte/layout (C#)
tools/           → scripts Python usados para extrair e montar as traduções
```

## Compilar o plugin (opcional)

Requer **.NET SDK** e o jogo com BepInEx já instalado.

```bash
cd src/plugin
dotnet build -c Release -p:GameDir="C:\Program Files (x86)\Steam\steamapps\common\Database Detective"
```

O `DatabaseDetective.PTBR.Font.dll` gerado vai para `BepInEx/plugins/DatabaseDetective-PTBR/` (junto com `PixelifySans.ttf`).

---

## Contribuindo com a tradução

Os dicionários são arquivos de texto simples no formato `original=tradução`, um por linha. Para melhorar uma frase, edite o arquivo correspondente em `translations/` e copie para `BepInEx/Translation/pt/Text/` no seu jogo (com `ReloadTranslationsOnFileChange=True`, dá para recarregar com **ALT+R** sem reiniciar). PRs são bem-vindos.

---

## Créditos e licenças

Veja **[NOTICE.md](NOTICE.md)**. Resumidamente:

- Código e traduções deste repositório: **MIT** (veja [LICENSE](LICENSE)).
- BepInEx — LGPL-2.1 · XUnity.AutoTranslator (bbepis) · **Pixelify Sans** — SIL Open Font License 1.1.
- *Database Detective* é propriedade da **HsuCorp**. Este é um projeto de fã, não-oficial; nenhum arquivo do jogo é redistribuído.
