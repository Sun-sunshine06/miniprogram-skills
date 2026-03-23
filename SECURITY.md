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

The default repository install no longer carries `miniprogram-automator` or its transitive `jimp` / `file-type` chain as a locked dependency of `tools/wechat-gui-check`.

If contributors or users opt into live GUI automation, they still need a local `miniprogram-automator` install at runtime, and that separately installed runtime may continue to inherit upstream audit findings. Treat that runtime dependency as a host-side prerequisite rather than a guaranteed-clean dependency managed by this repository, and keep the public note phrased in terms of a small remaining upstream moderate surface rather than a hardcoded count.
