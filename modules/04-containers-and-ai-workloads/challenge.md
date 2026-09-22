# Module 04 Challenge

## Challenge Prompt

Acme AI wants to run the sample chat stack in developer environments with the lowest possible friction, but it also wants the packaging decisions to remain credible for later production work.

Design the container packaging policy for the first release.

## Deliverable

Create a note in:

- `my-solutions/module-04-container-strategy.md`

Include:

1. what belongs in the application image
2. what belongs in the model API image
3. what should stay outside the image
4. which backing services are required now versus later
5. which runtime limits you would enforce first

## Failure Extension

Propose a second deliberate failure lab beyond OOM, such as a provider failure or broken prompt/config mount, and describe how you would trigger it locally.