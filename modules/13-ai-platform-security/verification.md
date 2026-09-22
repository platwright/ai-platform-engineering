# Module 13 Verification

## Check 1 - Threat Modeling Understanding

Without looking at the chapter, apply STRIDE to one component of the AI platform. Pick any one: RAG platform, agent platform, or model serving. Write one threat per STRIDE letter.

## Check 2 - Secrets Audit

Confirm your secrets audit from the lab is complete:

- [ ] You identified all files containing API key references in the sample stack
- [ ] You confirmed which files are gitignored
- [ ] You can explain what would happen if a real key was committed
- [ ] You can describe the correct production approach for this secret

## Check 3 - Prompt Injection

Confirm you can explain:

- [ ] The difference between direct and indirect prompt injection
- [ ] Why there is no complete defense against prompt injection
- [ ] At least two controls that reduce injection risk
- [ ] Why input validation alone is insufficient

## Check 4 - Approval Gate

Verify the approval gate behavior from the lab:

- [ ] Destructive action was blocked without approval token
- [ ] Destructive action succeeded with approval token
- [ ] Run artifact captured both outcomes correctly
- [ ] You can explain what would need to change to make the approval token more secure (expiry, scoping, single-use)

## Check 5 - RAG Tenant Isolation

Confirm you understand where isolation is enforced:

- [ ] You located the tenant filtering code in Project 03
- [ ] You can explain whether filtering is enforced at the storage layer or the application layer
- [ ] You can describe what would happen if the tenant filter had a bug
- [ ] You can explain what "authorization at retrieval time" means

## Check 6 - Supply Chain

Without looking at the chapter, answer:

1. Why is downloading an open-weight model and running `sha256sum` against the downloaded file not sufficient supply chain verification on its own?
2. What format should production deployments prefer over PyTorch `.bin` files and why?
3. What is the relationship between fine-tuning data and model behavior?

## Check 7 - Audit Logging

Design a minimal audit log entry for a successful agent tool call. Without looking at the chapter, write the JSON structure and explain what each field enables during an investigation.

## Check 8 - OWASP LLM Alignment

Match each OWASP LLM Top 10 item to one control from this module:

- [ ] LLM01 Prompt Injection → 
- [ ] LLM02 Sensitive Information Disclosure →
- [ ] LLM03 Supply Chain →
- [ ] LLM06 Excessive Agency →
- [ ] LLM08 Vector and Embedding Weaknesses →
