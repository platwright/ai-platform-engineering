# Failure Labs

Intentional failure scenarios designed to build diagnosis and recovery skills. Every lab in this area deliberately breaks something. Your job is to detect the failure, understand why it happened, and restore normal operation.

## Design Principle

Real platform engineers spend significant time diagnosing failures, not just building features. These labs provide safe practice for the failure modes that appear repeatedly in AI platform operations.

## Available Labs

### Completed

- **oom-lab**: deliberately trigger an out-of-memory container exit and diagnose the failure from logs and metrics. See [platform/docker/oom-lab.compose.yml](../../platform/docker/oom-lab.compose.yml). — covers Module 04

- **provider-timeout**: configure the AI gateway to call a provider that always times out. Observe how each layer handles the failure and implement a fallback recovery path. See [provider-timeout/README.md](provider-timeout/README.md). — covers Modules 08 and 14

- **rag-staleness**: update source documents after ingestion without re-ingesting, then observe the silent quality degradation. Build a staleness detection script. See [rag-staleness/README.md](rag-staleness/README.md). — covers Modules 09, 11, and 14

### Planned

- **gateway-policy-misconfiguration**: apply a rate limit that is too aggressive for the expected traffic pattern. Observe how applications behave when rate-limited and how to diagnose the correct threshold. — covers Module 08
- **agent-tool-escape**: attempt to make the agent call an unauthorized tool using a crafted objective. Verify that the authorization gate blocks the attempt and logs it correctly. — covers Module 10
- **context-window-overflow**: send a request that exceeds the model's context window and observe how different parts of the stack handle the resulting error. — covers Module 02
- **gpu-oom-inference**: overload the KV cache on a model server by sending many long concurrent requests. Observe degradation and practice recovery. — covers Modules 06 and 07
- **rolling-update-regression**: deploy a new application version with a broken prompt template and observe how the rollout affects production responses before rolling back. — covers Modules 11 and 04

## Format

Each failure lab has:

1. **Setup**: commands to create the failure condition
2. **Symptoms**: what you should observe from the outside
3. **Diagnosis**: steps to identify the root cause
4. **Recovery**: steps to restore normal operation
5. **Prevention**: controls that would prevent this failure in production

## Prerequisites

Failure labs build on the relevant module material. Check the lab README for its specific prerequisites before starting.
