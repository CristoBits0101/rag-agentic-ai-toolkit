param(
    [string]$OutputFile = ".git/.codex-commit-message.txt"
)

$ErrorActionPreference = "Stop"

$null = git rev-parse --show-toplevel 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Error "This task must run inside a Git repository."
}

$null = git diff --cached --quiet
if ($LASTEXITCODE -eq 0) {
    Write-Error "No staged changes found. Stage files before generating a commit message."
}

$diffStat = git diff --cached --stat --no-color
$diffBody = git diff --cached --unified=1 --no-color --no-ext-diff

if (-not $diffBody) {
    Write-Error "Unable to read the staged diff."
}

$prompt = @"
Generate one commit message for the staged Git changes.

Rules:
- Return only the commit message.
- Use Conventional Commits.
- Keep the subject line under 72 characters.
- Use imperative mood.
- Add a scope only when it improves clarity.
- Do not use quotes or code fences.

Repository: rag-agentic-ai-toolkit

Staged diff stat:
$diffStat

Staged diff:
$diffBody
"@

$promptFile = [System.IO.Path]::GetTempFileName()
$responseFile = [System.IO.Path]::GetTempFileName()

try {
    Set-Content -Path $promptFile -Value $prompt -NoNewline

    Get-Content -Path $promptFile -Raw | codex exec - --sandbox read-only --output-last-message $responseFile

    if ($LASTEXITCODE -ne 0) {
        exit $LASTEXITCODE
    }

    $message = (Get-Content -Path $responseFile -Raw).Trim()

    if (-not $message) {
        Write-Error "Codex returned an empty commit message."
    }

    $outputDirectory = Split-Path -Parent $OutputFile
    if ($outputDirectory) {
        New-Item -ItemType Directory -Path $outputDirectory -Force | Out-Null
    }

    Set-Content -Path $OutputFile -Value $message -NoNewline

    try {
        Set-Clipboard -Value $message
    } catch {
        Write-Warning "The commit message was generated but could not be copied to the clipboard."
    }

    Write-Output $message
    Write-Output ""
    Write-Output "Saved to $OutputFile"
} finally {
    Remove-Item -Path $promptFile -ErrorAction SilentlyContinue
    Remove-Item -Path $responseFile -ErrorAction SilentlyContinue
}
