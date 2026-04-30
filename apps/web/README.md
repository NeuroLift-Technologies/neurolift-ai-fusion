# Web App

A runnable web starter for simulation control.

## Current capabilities

- check simulation API health
- trigger a demo session and inspect JSON output

## Local run

Use any static file server after the API is running:

```bash
python3 -m http.server 4173 --directory apps/web
```

Then open `http://localhost:4173`.
