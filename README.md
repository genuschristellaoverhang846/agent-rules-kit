# agent-rules-kit

CLI local para diagnosticar la calidad mínima de archivos de instrucciones para agentes IA en repositorios.

Estado actual: inception local. No hay release, no hay remoto y no hay promesas de producción.

## Propósito

`agent-rules-kit` ayuda a revisar archivos como `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, reglas de Cursor e instrucciones de GitHub Copilot para detectar ausencias, duplicación, contradicciones básicas y riesgos operativos.

## Límites v0.1

- read-only by default; read-only por defecto.
- no network access; sin red.
- no LLM dependency; sin LLM.
- does not execute commands from analyzed repositories; sin ejecutar comandos del repositorio analizado.
- no file modifications unless a future explicit write mode is implemented.
- no security guarantees; it is not a security scanner.
- secret-like findings are always redacted.

## Licencia

MIT.
