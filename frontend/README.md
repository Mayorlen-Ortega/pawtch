# Huella Cerca frontend

This folder contains the Angular and TypeScript browser application for the Huella Cerca lost-and-found pet matching POC.

The repository root [README](../README.md) is the canonical guide for the complete project, including Python API setup, Angular setup, the live demo flow, the matching approach, local data privacy, and the POC boundaries.

## Frontend commands

Install dependencies and start the development server from this folder:

```powershell
npm install
npm start -- --port 4200
```

Open `http://localhost:4200`. The FastAPI backend must also be running; see the root README for its setup instructions.

Create a production build with:

```powershell
npm run build
```
