#!/usr/bin/env python3
"""Conferência do repositório de dados dos Editais (somente leitura; sem dependências externas).

Recusa: arquivos fora da lista permitida; editais.json ilegível, fora do contrato editais.v1 ou com campos não previstos;
sinais de dados pessoais (CPF, e-mail, telefone, matrícula) em qualquer texto; endereços fora dos domínios do IFTO;
conteúdo fictício quando --producao. A validação completa do contrato continua sendo a do Portal (scripts/validar-editais.py).

Uso: python3 verificar-conteudo.py [DIRETORIO] [--producao]
Saída: 0 se estiver tudo certo (ou se ainda não houver editais.json); 1 com a lista de problemas.
"""
import json, re, sys
from pathlib import Path

PERMITIDOS = {"README.md", "editais.json", "verificar-conteudo.py", ".github/workflows/validar.yml"}
TOPO = {"versao", "gerado_em", "origem", "aviso", "categorias", "editais"}
EDITAL = {"id", "numero", "titulo", "categorias", "nivel", "publico", "publicado_em", "link_edital", "link_inscricao", "pagina_oficial",
          "cronograma", "documentos", "palavras_chave", "substitui_previsao", "aprovacao", "observacao_publica", "oportunidade_estudantil",
          "abrangencia", "vigencia"}
HOSTS = ("https://www.ifto.edu.br/", "https://ifto.edu.br/", "https://portal.ifto.edu.br/", "https://suap.ifto.edu.br/")
CPF = re.compile(r"\b\d{3}\.?\d{3}\.?\d{3}-?\d{2}\b")
EMAIL = re.compile(r"[\w.+-]+@[\w-]+(\.[\w-]+)+")
TELEFONE = re.compile(r"(\(\d{2}\)\s?|\b\d{2}\s)9?\d{4}[-\s]?\d{4}\b")
MATRICULA = re.compile(r"\b\d{12,}\b")
FICTICIO = re.compile(r"\bteste\b|\[teste\]|fict[ií]ci", re.I)


def textos(valor, caminho=""):
    """Todos os textos do JSON, com o caminho de cada um."""
    if isinstance(valor, dict):
        for k, v in valor.items():
            yield from textos(v, f"{caminho}.{k}" if caminho else k)
    elif isinstance(valor, list):
        for i, v in enumerate(valor):
            yield from textos(v, f"{caminho}[{i}]")
    elif isinstance(valor, str):
        yield caminho, valor


def verificar(raiz, producao=False):
    raiz = Path(raiz)
    erros = []
    for p in sorted(raiz.rglob("*")):
        rel = p.relative_to(raiz).as_posix()
        if rel == ".git" or rel.startswith(".git/") or p.is_dir():
            continue
        if rel not in PERMITIDOS:
            erros.append(f"arquivo não permitido neste repositório: {rel}")
    arquivo = raiz / "editais.json"
    if not arquivo.is_file():
        return erros  # repositório recém-criado: ainda sem dados
    if arquivo.stat().st_size > 1024 * 1024:
        return erros + ["editais.json maior que 1 MB"]
    try:
        dados = json.loads(arquivo.read_text(encoding="utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as ex:
        return erros + [f"editais.json ilegível: {ex}"]
    if not isinstance(dados, dict) or dados.get("versao") != "editais.v1" or not isinstance(dados.get("editais"), list):
        return erros + ["editais.json fora do contrato editais.v1"]
    extras = sorted(set(dados) - TOPO)
    if extras:
        erros.append(f"campos de topo não previstos: {extras}")
    for i, e in enumerate(dados["editais"]):
        if not isinstance(e, dict):
            erros.append(f"editais[{i}] não é um objeto")
            continue
        extras = sorted(set(e) - EDITAL)
        if extras:
            erros.append(f"edital {e.get('id', i)}: campos não previstos {extras}")
    for caminho, t in textos(dados):
        chave = caminho.rsplit(".", 1)[-1]
        if chave in ("link_edital", "link_inscricao", "pagina_oficial", "url"):
            if not t.startswith(HOSTS):
                erros.append(f"{caminho}: endereço fora dos domínios oficiais do IFTO")
            continue  # endereços oficiais podem conter números longos
        for nome, padrao in (("CPF", CPF), ("e-mail", EMAIL), ("telefone", TELEFONE), ("número longo (matrícula/documento)", MATRICULA)):
            if padrao.search(t):
                erros.append(f"{caminho}: parece conter dado pessoal ({nome})")
    if producao:  # mesmos campos conferidos pelo validador do Portal (rótulos como "Teste de nivelamento" são legítimos)
        for e in dados["editais"]:
            if isinstance(e, dict) and FICTICIO.search(" ".join(str(e.get(k, "")) for k in ("id", "titulo", "numero", "observacao_publica"))):
                erros.append(f"edital {e.get('id', '?')}: conteúdo fictício ou de teste não pode ir para a main")
    return erros


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    problemas = verificar(args[0] if args else ".", "--producao" in sys.argv)
    if problemas:
        print("REPROVADO:")
        for p in problemas:
            print("  - " + p)
        sys.exit(1)
    print("OK: repositório de editais dentro das regras.")
