# DevTools CLI Repair Playbook

## Command Ladder

Use the official CLI bundled with WeChat DevTools.

### Step 1: Confirm CLI Availability

Run:

```powershell
& '<cli-path>' --help
```

What it proves:

- DevTools is installed
- the official CLI is callable
- supported subcommands can be inspected before acting

### Step 2: Check Relevant Help

Typical commands:

```powershell
& '<cli-path>' open --help
& '<cli-path>' preview --help
& '<cli-path>' auto --help
```

### Step 3: Establish IDE Connectivity And The Live Port

Typical open command:

```powershell
& '<cli-path>' open --project '<project-root>' --port 9000
```

Collect:

- command exit code
- stdout and stderr
- the port reported by the CLI itself

If the command reports a running HTTP service address, treat the reported port as the live source of truth for the current session.

### Step 4: Use `preview` As The Primary Compile Check

Typical preview command:

```powershell
& '<cli-path>' preview --project '<project-root>' --port '<live-port>' --qr-format base64 --qr-output '<qr-output>' --info-output '<info-output>'
```

What it proves when it works:

- the repo survives the preview compile path
- exact invalid-file errors can be surfaced when the repo is wrong
- preview artifacts can be generated for automation

### Step 5: Treat `engine build` As Secondary Diagnostics

Do not use `engine build` as the primary compile check for a standard miniapp repo. Prefer it only when `preview` does not answer the question.

## Live Port Discovery

Prefer these sources in order:

1. explicit CLI success output from `open` or `preview`
2. local DevTools settings that record the current listener
3. `.cli`-style cache files as hints only

If cached files disagree with the live CLI message, trust the live CLI message.

## Timeout Handling

If `open` or `preview` times out:

1. check whether DevTools and its helper processes are running
2. inspect the latest launch logs
3. if the log is empty and GUI is open, treat the remaining failure as potentially GUI-only

## Auto-Fix Decision Table

Before changing files, classify the failure into one of four buckets:

1. repo-scoped preview or compile failure
2. host, login, AppID, or DevTools session blocker
3. GUI-only runtime issue after a route opens
4. local service dependency outside preview scope

### Preview Exposes A Repo Syntax Or Compile Error

Action:

- patch the repo only if the change is local and semantics-preserving
- prefer exact, minimal fixes
- re-run the same `preview` command

### Preview Exposes TypeScript Recognition Or Config Drift

Action:

- patch `project.config.json`, `tsconfig.json`, or `app.json`
- rerun `open` if the active session is stale
- rerun `preview`

### CLI Exposes A Repo Structure Error

Action:

- patch the repo automatically if the fix is clearly repo-scoped
- explain the exact file changes
- rerun the smallest validating command

### CLI Starts DevTools But Does Not Surface The Problem

Action:

- say the CLI path was exhausted
- ask for the exact screenshot or GUI evidence that still blocks diagnosis

### Preview Is Green But The Page Still Fails At Runtime

Action:

- stop the CLI-only loop
- classify the remaining blocker as GUI-only runtime evidence
- hand off to `miniapp-devtools-gui-check` or the repo's service-debug path

### Route Fails Because A Local Service Is Unavailable

Action:

- do not misclassify the issue as a preview compile failure
- keep the CLI result as "compile path healthy"
- ask for the service contract, local backend status, or GUI/runtime evidence that shows the failing request

## Success Criteria

Claim preview success only when all of these are true:

1. CLI output indicates preview success
2. the command exits successfully
3. requested preview artifacts exist
4. the generated info file can be read when requested
