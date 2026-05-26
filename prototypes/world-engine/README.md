# World Engine — Frontend Prototype

A standalone React prototype that visualises the Avatar/Aide/Scenario world. **Not wired** to the Python simulation engine — the sim ticks locally in the browser. See `docs/specs/world-engine-prototype-schema.md` for the full data contract.

## Run it

No build step. Any static file server works:

```bash
cd prototypes/world-engine
python3 -m http.server 8765
# then open http://127.0.0.1:8765/
```

The page boots React 18 + Babel from a CDN and loads the `.jsx` files in-browser via `<script type="text/babel">`.

## Runtime model

- `index.html` must load files in this order: `data.js`, `tweaks-panel.jsx`, `sim.jsx`, `world-view.jsx`, `hud.jsx`, then `app.jsx`.
- `data.js` exposes the only data source as `window.WE_DATA`; there are no fetches, API clients, or environment variables.
- `sim.jsx` exposes `window.useWorldEngine(...)` and keeps runtime state in React. It advances a local tick loop, assigns scenarios, emits event objects, and records coaching interventions.
- `world-view.jsx` renders a 24 x 18 isometric tile map using DOM/CSS; it does not use Canvas or WebGL.
- `tweaks-panel.jsx` starts open when run standalone and listens for the `__activate_edit_mode` / `__deactivate_edit_mode` host protocol only when embedded in a parent frame.

## What's here

| File | Role |
|---|---|
| `index.html` | Entry point, CDN loaders, script order |
| `data.js` | Static data — 19 avatars, paired aides, 11 scenarios, 5 rooms, NPCs, strategies, event vocabulary |
| `app.jsx` | Top-level composition, layout, theme/zoom/pan, tweaks panel mount |
| `sim.jsx` | Tick loop, avatar runtime state, event emission, flavor-bias tables |
| `world-view.jsx` | Isometric CSS/SVG renderer (32×16 tile diamond, rooms, props, avatars, NPCs) |
| `hud.jsx` | HUD panels — `TopBar`, `AvatarStateCard`, `EventStream`, `AideLog`, `FleetRoster`, `ScenarioControls`, `ProgressPanel` |
| `tweaks-panel.jsx` | Live-tuning shell with the `__activate_edit_mode` host protocol |
| `world.css` | Full styling |
| `_drafts/` | Earlier single-file drafts preserved verbatim: `world-engine.jsx` (full sim+UI in one file), `tweaks-panel.jsx` (top-level dup), `design-canvas.jsx` (Figma-style artboard shell), and the original `scraps/` |

## Roster

19 ADHD-trait avatars. IDs use snake_case matching the Python repo convention (`src/avatars/adhd_traits/`). The first two map directly to existing Python implementations (`stay_alert`, `task_kickstart`); the remaining 17 are design proposals.

Full table in `docs/specs/world-engine-prototype-schema.md#canonical-roster`.

### Roster corrections applied to source

The two zip drafts shipped conflicting rosters. This directory uses the cleaner-named roster with three fixes:

- `transition` → `transition_ease` (consistency with other ids)
- `follow_thru` → `follow_through` (full word)
- `Physical Restless.` → `Physical Restlessness` (no truncation)

The richer schema (blurb, flavor, tag) came from `engine/data.js`. The `_drafts/world-engine.jsx` original is preserved unchanged for reference.

## What's deliberately NOT here

- **No build pipeline.** No package.json, no Vite/Next/Webpack. Adding one is out of scope until the prototype is promoted into `apps/`.
- **No API wiring.** No fetch calls; all state is in-browser. The `mkEvent` payloads and the `AvatarRuntime` shape (in `sim.jsx`) are the eventual API contract — see the open questions in the schema doc.
- **No tests.** This is a design prototype, not production code.
- **No changes to `src/`.** The Python simulation engine is untouched. The two are reconciled later through an explicit transport decision.

## Common pitfalls

- Do not open `index.html` with `file://`; serve the directory so Babel can fetch the `.jsx` files consistently.
- The page needs network access to `unpkg.com` for React 18 and Babel. An offline browser will stay on the boot screen unless those CDN assets are made local.
- If the screen stays on "booting world engine prototype...", check the browser console first. Missing globals usually mean the script order changed or a `.jsx` file failed to load.
- Scenario routing is prototype-only: `data.js` has 11 room-aware scenarios, while `src/simulation/environment/scenarios.py` has 13 Python scenarios without room layout.
- The first two avatar ids (`stay_alert`, `task_kickstart`) have Python classes; only `stay_alert` has a checked-in JSON config under `src/avatars/avatar_configs/`.
