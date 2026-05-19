# Real AI smoke example for Week 11 Day 3.
# This file is an example only. Confirm your local environment before running it.
# Do not commit a real OPENAI_API_KEY. Set the key in your shell environment instead.

param(
    [switch]$Run,
    [string]$BackendBaseUrl = "http://localhost:8080",
    [string]$SampleImage = "samples/01-simple-card-page.png"
)

$ErrorActionPreference = "Stop"

$RecommendedOpenAiBaseUrl = "https://api.siliconflow.cn/v1"
$RecommendedOpenAiModel = "Qwen/Qwen3-VL-32B-Instruct"
$RecommendedPythonCommand = "D:\environment\python11\python.exe"
$ApiKeyPlaceholder = "<set-your-key-here>"

Write-Host "Real AI smoke example"
Write-Host "Backend base URL: $BackendBaseUrl"
Write-Host "Sample image: $SampleImage"
Write-Host "Recommended OPENAI_BASE_URL: $RecommendedOpenAiBaseUrl"
Write-Host "Recommended OPENAI_MODEL: $RecommendedOpenAiModel"
Write-Host "Recommended IMAGEPAGE_WORKER_PYTHON_COMMAND: $RecommendedPythonCommand"
Write-Host "Current OPENAI_BASE_URL: $env:OPENAI_BASE_URL"
Write-Host "Current OPENAI_MODEL: $env:OPENAI_MODEL"
Write-Host "Current IMAGEPAGE_WORKER_PYTHON_COMMAND: $env:IMAGEPAGE_WORKER_PYTHON_COMMAND"
Write-Host "OPENAI_API_KEY present: $([bool]$env:OPENAI_API_KEY)"
Write-Host ""
Write-Host "Set these variables before starting backend:"
Write-Host "  `$env:OPENAI_BASE_URL = `"$RecommendedOpenAiBaseUrl`""
Write-Host "  `$env:OPENAI_MODEL = `"$RecommendedOpenAiModel`""
Write-Host '  $env:OPENAI_API_KEY = "<set-your-key-here>"'
Write-Host "  `$env:IMAGEPAGE_WORKER_PYTHON_COMMAND = `"$RecommendedPythonCommand`""
Write-Host ""
Write-Host "Then start backend with:"
Write-Host "  cd backend"
Write-Host "  java -jar target/backend-0.0.1-SNAPSHOT.jar --imagepage.worker.timeout-seconds=120"
Write-Host "Do not write the real key into this file."
Write-Host ""

if (-not $Run) {
    Write-Host "Dry example only. Re-run with -Run after confirming the environment."
    exit 0
}

if (-not $env:OPENAI_API_KEY -or $env:OPENAI_API_KEY -eq $ApiKeyPlaceholder) {
    throw "OPENAI_API_KEY is not set. Set it in the shell environment; do not store it in the repository."
}

if ($env:OPENAI_BASE_URL -ne $RecommendedOpenAiBaseUrl) {
    throw "OPENAI_BASE_URL should be $RecommendedOpenAiBaseUrl before running real AI smoke."
}

if ($env:OPENAI_MODEL -ne $RecommendedOpenAiModel) {
    throw "OPENAI_MODEL should be $RecommendedOpenAiModel before running real AI smoke."
}

if ($env:IMAGEPAGE_WORKER_PYTHON_COMMAND -ne $RecommendedPythonCommand) {
    throw "IMAGEPAGE_WORKER_PYTHON_COMMAND should be $RecommendedPythonCommand before running real AI smoke."
}

if (-not (Test-Path -LiteralPath $SampleImage)) {
    throw "Sample image not found: $SampleImage"
}

if (-not (Test-Path -LiteralPath $RecommendedPythonCommand)) {
    throw "Python command not found: $RecommendedPythonCommand"
}

$confirm = Read-Host "This will call the local backend and may trigger a real external model request. Type RUN to continue"
if ($confirm -ne "RUN") {
    Write-Host "Cancelled."
    exit 0
}

Write-Host "Uploading sample image..."
$uploadResponse = Invoke-RestMethod `
    -Method Post `
    -Uri "$BackendBaseUrl/api/image-page/upload" `
    -Form @{ file = Get-Item -LiteralPath $SampleImage }

$jobId = $uploadResponse.data.jobId
if (-not $jobId) {
    $jobId = $uploadResponse.jobId
}
if (-not $jobId) {
    throw "Upload response did not contain jobId."
}

Write-Host "Uploaded. jobId: $jobId"

Write-Host "Generating page..."
$firstGenerate = Invoke-RestMethod `
    -Method Post `
    -Uri "$BackendBaseUrl/api/image-page/jobs/$jobId/generate"

Write-Host "First generate completed."
Write-Host "Inspect response status, sourceType/mode, fallbackUsed, fallbackReason, previewHtml, and artifact files."

Write-Host "Generating page again with the same jobId to check artifact reuse..."
$secondGenerate = Invoke-RestMethod `
    -Method Post `
    -Uri "$BackendBaseUrl/api/image-page/jobs/$jobId/generate"

Write-Host "Second generate completed."
Write-Host "Expected reuse signal: artifact.reused=true in response metadata or metadata.json."
Write-Host "Do not commit backend/storage/, frontend/dist/, private screenshots, or real keys."
