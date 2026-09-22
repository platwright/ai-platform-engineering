# Chapter 07 - Disaster Recovery for AI Platforms

## What "Disaster" Means For AI Platforms

For a web application, disaster recovery typically means restoring compute and data from backup after a major failure. For an AI platform, disaster recovery covers the same infrastructure concerns plus AI-specific artifacts that must also be recoverable:

| Artifact | DR Concern |
|---|---|
| Prompt registry | Must be versioned and recoverable to any prior state |
| RAG indexes | Must be re-creatable from source documents |
| Vector database state | Must be backed up or reconstructable |
| Model weights | Must be available from a trusted registry |
| Eval datasets | Must be version-controlled and restorable |
| Platform configuration | Must be managed as infrastructure-as-code |

## RTO and RPO for AI Artifacts

RTO (Recovery Time Objective) and RPO (Recovery Point Objective) apply to each AI artifact type:

| Artifact | RPO Target | RTO Target | Recovery Method |
|---|---|---|---|
| System prompts | 0 (git-versioned) | < 5 min | Pull from git |
| RAG index | 24 hours | < 2 hours | Re-ingest from source docs |
| Vector DB data | 24 hours | < 4 hours | Restore from backup |
| Model weights | N/A (not data) | < 1 hour | Pull from model registry |
| Gateway config | 0 (git-versioned) | < 10 min | Re-apply from git |
| Eval datasets | 0 (git-versioned) | < 5 min | Pull from git |

## RAG Index Recovery

RAG indexes are the AI-specific artifact most likely to need disaster recovery procedures. The recovery sequence:

1. **Identify the extent of loss**: which tenants are affected, what was the last successful ingest timestamp
2. **Verify source documents are intact**: the vector index can be reconstructed if the source documents exist
3. **Re-ingest from source**: run the ingestion pipeline against the source document store
4. **Validate recovery**: run a set of known queries and confirm expected results
5. **Monitor freshness signal**: verify `rag_index_last_updated_timestamp` updates correctly

The key insight: the RAG index is derived data. If source documents are preserved, the index can always be reconstructed. The source documents are the primary artifact to protect.

## Prompt and Config Recovery

Prompts and configuration managed in git recover automatically:

```bash
# Restore last known good prompt version
git checkout <last-good-commit> -- prompts/rag-grounding/v1.4.0.yaml

# Re-apply gateway configuration
kubectl apply -k platform/kubernetes/ai-gateway
```

This is why treating prompts as code in version control is both a quality practice (Module 11) and a reliability practice.

## Vector Database Backup

Vector databases typically support snapshot-based backup:

```bash
# Chroma (file-based) - copy the persistence directory
cp -r /chroma/data /backup/chroma-$(date +%Y%m%d)

# Qdrant - use snapshot API
curl -X POST http://qdrant:6333/collections/{collection}/snapshots

# Pinecone / managed providers - use platform backup features
```

Set up automated daily snapshots with retention for at least 7 days.

## Stateless Design Reduces DR Complexity

The most reliable AI platform is one where the minimum amount of state needs DR protection:

- **Stateless serving**: model servers load weights from the registry on startup, no local state
- **Derived indexes**: RAG indexes reconstructable from source, not a primary data store
- **External secrets**: credentials in a vault, not baked into images or config maps
- **Config as code**: all platform configuration in git, applied by CI/CD

A platform designed with these principles recovers faster because fewer artifacts require backup and restoration procedures.

## DR Testing

DR procedures that are not regularly tested will fail when needed:

| Test | Frequency | What To Validate |
|---|---|---|
| RAG index re-ingest | Monthly | Ingest from scratch produces correct query results |
| Gateway config restore | Quarterly | Re-apply config from git, verify routing works |
| Model weight reload | Per model update | Pull from registry and serve correctly |
| Prompt rollback | Per release | Revert prompt version, confirm behavior change |

Run these tests in a staging environment, not production. Document the RTO observed versus the RTO target.

## Platform Runbook: Full Stack Recovery

For a complete platform recovery from scratch:

```
1. Provision infrastructure (Kubernetes cluster, GPU nodes)
   → Use terraform/IaC: 30-60 minutes

2. Deploy platform services from git
   → kubectl apply -k platform/kubernetes/: 10-15 minutes

3. Load model weights from registry
   → Automated by serving pod startup: 5-20 minutes depending on model size

4. Apply secrets from vault
   → External Secrets Operator syncs on startup: 2-5 minutes

5. Re-ingest RAG indexes for each tenant
   → Run ingestion pipeline per tenant: 5-30 minutes per tenant

6. Validate with smoke tests
   → Run eval/run_eval.py --mode smoke: 5-10 minutes

Total estimated RTO: 1-3 hours depending on infrastructure provisioning speed
```

Document this runbook and test it at least once per quarter.
