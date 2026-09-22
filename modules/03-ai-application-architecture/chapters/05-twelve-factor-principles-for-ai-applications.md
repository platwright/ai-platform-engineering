# Chapter 3.5 - Twelve-Factor Principles for AI Applications

## Why Revisit Twelve-Factor

The classic twelve-factor principles still provide useful discipline for cloud-native applications. AI systems do not replace those principles. They expand the set of artifacts and runtime controls that need the same discipline.

## Still Useful Core Ideas

The following still matter directly:

- one codebase per application
- explicit dependencies
- config separated from code
- backing services treated as attached resources
- clear build, release, and run stages
- stateless processes where possible
- fast startup and shutdown behavior
- environment parity
- logs as event streams

## AI-Specific Translation

For AI applications, extend those principles to include:

- prompts as managed artifacts
- model selection as configuration, not hidden code
- evaluation datasets and checks as part of release quality
- retrieval configuration as a runtime concern
- tool permissions and policy as explicit configuration

## Practical Adaptation Examples

### Config

Traditional config might include database URLs and credentials.

AI config also includes:

- model alias
- prompt file path
- generation defaults
- provider credentials
- limits and fallback policy

### Backing Services

Traditional backing services might include a database and cache.

AI applications may also attach to:

- vector stores
- model providers
- evaluation services
- tracing backends

### Build, Release, Run

You should know exactly which combination of code, prompt assets, and config entered a release. If you cannot answer that, debugging regressions becomes guesswork.

## Platform Takeaway

Twelve-factor discipline is still a strong baseline. The important change is that AI-specific artifacts now deserve the same rigor as code, config, and traditional dependencies.