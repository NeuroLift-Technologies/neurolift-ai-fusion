# Simulation SDK

Shared TypeScript contracts and API client for web + mobile surfaces.

## Included

- `src/types.ts`: session/scenario request-response contracts
- `src/client.ts`: minimal API client wrapper

## Example

```ts
const client = new SimulationApiClient("http://localhost:8000");
const result = await client.runSession({ scenarios: [{ name: "Morning planning" }] });
```
