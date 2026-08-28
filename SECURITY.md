# Security policy

## Reporting

Do not open public issues containing customer prompts, evidence, secrets, tenant identifiers or security findings. Report privately to the repository owner.

## Runtime controls

- Use managed identity or workload identity; do not commit keys.
- Keep generative-AI content recording disabled unless explicitly approved.
- Partition traces and evidence by tenant and purpose.
- Require human approval for production changes, compliance claims, financial decisions and customer-facing diligence answers.
- Sign or hash economics receipts and keep policy administration separate from agent execution.
- Treat fetched retail prices as untrusted external input and validate fields before financial use.

