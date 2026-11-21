# Repositório de dados de Editais — IFTO Campus Palmas

## Situação identificada em 21/11/2026
- A branch `main` contém somente este README; ainda não é fonte de dados de produção.
- A branch `previa` contém uma implementação candidata R4.16-E2: `editais.json` (contrato `editais.v1`), `verificar-conteudo.py` e workflow `.github/workflows/validar.yml`.
- A prévia contém 18 registros e usa validador automático em push/PR. Isso comprova preparação técnica, não aprovação para produção nem integração efetiva ao Portal.

**Não promover a prévia nem tratar este repositório como fonte oficial de produção sem decisão expressa da GEAE e homologação da integração.**

## Fluxo atualmente documentado no Portal
A curadoria também permanece implementada/documentada no repositório principal:
- [Procedimento de curadoria](https://github.com/thiagoifto/portal-academico-palmas/blob/main/admin/editais/README.md)
- [Conferência GEAE](https://github.com/thiagoifto/portal-academico-palmas/blob/main/admin/editais/conferencia-geae.md)
- Implementação: `scripts/editais-curadoria.py`.
- Arquivo atualmente consumido pelo Portal: `data/editais.json`.

A comparação de inventário feita em 21/11/2026 encontrou 18 IDs na prévia deste repositório e 18 IDs no arquivo do Portal, com o mesmo conjunto de IDs. As datas de geração e hashes são diferentes; igualdade de IDs não comprova igualdade integral de conteúdo. É necessária comparação campo a campo e validação das fontes antes de qualquer promoção.

## Regras para evolução
- Não transferir nem promover dados sem decisão e plano de migração aprovados.
- Não criar arquivo de produção, contrato ou workflow por suposição.
- Manter dados de candidatos e documentos pessoais fora do Git; publicar somente informações institucionais públicas autorizadas.
- Não incluir credenciais, tokens, propriedades Apps Script ou segredos.
- Preservar ruleset da branch default: PR obrigatório, histórico linear, resolução de threads e Squash; atualmente zero aprovações obrigatórias.
- Qualquer ativação deve registrar contrato, schema, validador, origem, papéis, aprovação, reversão, pipeline e testes de integração.

## Relação com o Portal
A separação física dos repositórios não torna automaticamente este repositório a fonte usada em produção. O Portal ainda possui `data/editais.json` e sua própria curadoria. A futura adoção desta branch `previa` depende de decisão formal, reconciliação de conteúdo e mudança controlada do build/integração.
