# Security Policy

## Scope

This repository currently contains:

- reusable Codex skills
- documentation and playbooks
- lightweight host-side tooling for WeChat Mini Program workflows
- one optional beta GUI harness under `tools/wechat-gui-check`

## Reporting

For low-risk bugs or documentation mistakes, open a normal GitHub issue.

For anything that may expose credentials, compromise a local machine, or enable unsafe host-side automation behavior, do not post exploit details in a public issue. Until a dedicated private reporting channel exists, open only a minimal public issue that asks for a private contact path and omits sensitive reproduction details.

## Known Dependency Note

Most of the current dependency audit surface is isolated to the optional `tools/wechat-gui-check` beta package, which still inherits a small number of moderate findings through `miniprogram-automator` and its transitive `jimp` / `file-type` chain.

This repository already reduces the direct dependency surface on its own side, but it does not fully remove those upstream package risks yet. Keep the public security note phrased in terms of a small remaining upstream moderate surface rather than a hardcoded count, because GitHub alerts and local `npm audit` summaries may not age in lockstep.
