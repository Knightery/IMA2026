---
description: Run all tasks automatically without user approval
---

// turbo-all

## Rules

- **NEVER print large outputs to stdout.** Always write results directly to files (CSV, markdown, text, etc.) and then use `view_file` to read them. This avoids truncation issues.
- When running Python scripts, save all outputs to files rather than relying on `print()`.
- Use `view_file` to inspect results after writing them.

## Steps

1. Read and understand the user's request
2. Execute all necessary commands and file operations
3. Complete the task end-to-end
