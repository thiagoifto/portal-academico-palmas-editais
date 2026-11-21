# Repositório de dados de Editais — IFTO Campus Palmas

## Situação identificada
Na `main` consultada em 21/11/2026, este repositório contém somente este README. A branch `previa` também existe. Não há, neste snapshot da `main`, arquivo JSON de produção, validador ou workflow de publicação.

**Este repositório não deve ser tratado como fonte de produção ativa até que a GEAE aprove formalmente o contrato, a origem dos dados, o fluxo de prévia/publicação e a integração com o Portal.**

## Fluxo atualmente documentado no Portal
A curadoria de Editais permanece descrita no repositório principal:
- [Procedimento de curadoria](https://github.com/thiagoifto/portal-academico-palmas/blob/main/admin/editais/README.md)
- [Conferência GEAE](https://github.com/thiagoifto/portal-academico-palmas/blob/main/admin/editais/conferencia-geae.md)
- Implementação de curadoria: `scripts/editais-curadoria.py`.
- Fonte de publicação indicada pelo procedimento atual: `data/editais.json` no repositório Portal.

O fluxo descrito é: fonte oficial → candidatos com origem/data → conferência documental → decisão GEAE → publicação controlada → PR → prévia → merge autorizado.

## Regras para evolução
- Não transferir dados do Portal para este repositório sem decisão e plano de migração.
- Não criar arquivo de produção, contrato ou workflow por suposição.
- Manter dados de candidatos e documentos pessoais fora do Git; publicar somente informações institucionais públicas autorizadas.
- Não incluir credenciais, tokens, propriedades Apps Script ou segredos.
- Preservar regras de proteção da branch default: PR obrigatório, histórico linear, resolução de threads e Squash; o ruleset atualmente exige zero aprovações.
- Quando houver decisão de ativação, registrar contrato, schema, validador, origem, papéis, aprovação, reversão e pipeline antes de publicar.

## Relação com o Portal
Este repositório é separado do código do Portal, mas a separação física não implica que ele já seja a fonte de dados em produção. A fonte efetiva deve ser confirmada no build e na documentação operacional vigente.
