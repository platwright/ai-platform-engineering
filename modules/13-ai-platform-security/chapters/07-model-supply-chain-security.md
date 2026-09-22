# Chapter 07 - Model Supply Chain Security

## Why Model Supply Chain Is A Real Risk

Open-weight models are downloaded from public repositories — Hugging Face Hub, GitHub, and similar platforms. The weights are large binary files. Most teams verify them by checking that the download completed without error. That is not a security verification.

Known supply chain risks for model artifacts:

- **Backdoored weights**: a model file modified to exhibit specific behaviors for specific trigger inputs
- **Pickled exploits**: PyTorch's legacy pickle format for serialization is vulnerable to arbitrary code execution on load
- **Provenance spoofing**: a model uploaded as a well-known family member but with altered weights
- **Dependency poisoning**: model loading libraries with malicious dependencies

## Hash Verification

Every model download should be verified against a known-good hash before use:

```bash
# Download and verify
sha256sum llama-3.1-70b-instruct-Q4_K_M.gguf
# Compare to the expected hash published by the model author

# In a script
EXPECTED_HASH="abc123..."
ACTUAL_HASH=$(sha256sum model.bin | awk '{print $1}')
if [ "$ACTUAL_HASH" != "$EXPECTED_HASH" ]; then
  echo "Hash mismatch — model may be compromised"
  exit 1
fi
```

Publish expected hashes in your model registry alongside the download location. The hash must come from a trusted source (the original model author's public keys, your own secured registry) — not from the same location as the download.

## The SafeTensors Format

Hugging Face's SafeTensors format is a safer alternative to PyTorch's pickle-based `.pt` and `.bin` files:

- SafeTensors contains only tensor data, no executable code
- Loading a SafeTensors file cannot execute arbitrary Python code
- Widely supported by major serving frameworks

Prefer SafeTensors over pickle-based formats for any production model deployment. When only a pickle-based format is available, load it in an isolated environment with no network access.

## Trusted Model Registries

Rather than downloading models directly from public hubs in production pipelines, pull from a controlled internal registry:

```
Public Hub (Hugging Face)
        │
        ▼
Internal Review Process
  - hash verification
  - format check (SafeTensors preferred)
  - license review
  - capability evaluation
        │
        ▼
Internal Model Registry (Artifactory, OCI registry, S3)
        │
        ▼
Production Serving Infrastructure
```

This creates a security checkpoint before any model reaches production. It also enables:
- audit trail of which models were reviewed and approved
- license compliance tracking
- reproducible model deployments

## Evaluating Models Before Production Deployment

Beyond format and hash verification, evaluate model behavior before production:

- run your evaluation suite on the new model candidate
- red-team for obvious jailbreaks and harmful output patterns
- verify that the model respects the system prompt structure you use
- check performance against your quality and latency SLOs

A model that passes hash verification but produces systematically harmful outputs is still a supply chain failure — it was not the model you intended to deploy.

## Fine-Tuning Data Provenance

If your organization fine-tunes models, the training data is part of the supply chain:

- track the source and license of every dataset used in fine-tuning
- screen training data for toxic, biased, or malicious content before use
- do not include production user data in fine-tuning datasets without explicit consent and legal review
- version and retain training datasets for audit purposes

A model fine-tuned on poisoned data will exhibit poisoned behavior even if the base weights are legitimate.

## Dependency Security For Model Serving

Model serving libraries (vLLM, TGI, transformers, llama-cpp-python) have their own dependency trees. Apply standard software supply chain practices:

- pin dependency versions in serving container images
- scan dependencies for known CVEs regularly
- use minimal base images to reduce attack surface
- rebuild and redeploy serving containers when security patches are available

The model serving infrastructure is as much a supply chain risk as the model weights themselves.

## Summary Checklist

Before deploying any new model:

- [ ] Downloaded from a trusted source (official model author or your internal registry)
- [ ] Hash verified against a reference published by the model author
- [ ] Format verified (SafeTensors preferred, pickle-based audited)
- [ ] License reviewed for production use
- [ ] Passed your evaluation suite at threshold
- [ ] Tested for obvious harmful output patterns
- [ ] Approved in your model registry with a review record
- [ ] Verified that the serving container dependencies are up to date
