# Snake — React

Minimal Snake game built with React + Vite, using an HTML `canvas` for rendering and Tailwind CSS for styling.

**Features**
- Simple game engine with a loop (interval) and collision detection.
- Random food spawning, snake length increase, and gradual speed-up.
- Keyboard controls (arrow keys / WASD), pause with `Space`, and on-screen buttons to start/pause/restart.
- Styles provided via `Tailwind CSS`.

**Prerequisites**
- Node.js (recommended v16+) and `npm` installed.

**Install & development**
1. From the project root, open a terminal in the `snake_game` folder:

```bash
cd snake_game
```

2. Install dependencies:

```bash
npm install
```

3. Start the Vite development server:

```bash
npm run dev
```

4. Open the URL shown by Vite (default: `http://localhost:5173`).

**Useful scripts**
- `npm run dev`: start development server.
- `npm run build`: create a production bundle in `dist/`.
- `npm run preview`: serve the produced build locally for verification.

**Controls**
- Move: arrow keys or `W A S D`.
- Pause / resume: press `Space`.
- Buttons: `Start` / `Pause` / `Restart` in the UI.

**Important structure**
- `index.html`: HTML entrypoint loaded by Vite.
- `src/main.jsx`: React entrypoint.
- `src/App.jsx`: root component.
- `src/SnakeGame.jsx`: game logic and canvas rendering.
- `src/index.css`: Tailwind directives and component styles.
- `tailwind.config.cjs` and `postcss.config.cjs`: Tailwind/PostCSS configuration.

**Troubleshooting**
- PostCSS / Tailwind errors:
  - Make sure `tailwindcss`, `postcss` and `autoprefixer` are listed in `snake_game/package.json` and installed.
  - If Vite reports that the PostCSS plugin configuration changed, use the compatible configuration for your Tailwind version (this project uses the standard Tailwind v3 setup).
- If styles are missing, verify that `@tailwind base; @tailwind components; @tailwind utilities;` are present in `src/index.css` and that `tailwind.config.cjs` includes `index.html` and `src/**/*` in its `content` paths.

**Possible improvements**
- Touch controls for mobile.
- Store high scores in `localStorage`.
- CSS animations / transitions for the UI.
- Difficulty options (initial speed, larger grid).

**Credits**
This repository contains a simple demo implementation — feel free to fork and adapt it.

---

## Screenshot

Here is a screenshot included in `img/`:

![Snake Screenshot](./img/sc_1.png)

If the image does not appear in your file viewer or on GitHub, open `snake_game/img/sc_1.png` directly or check that the relative path to the image is correct after moving the folder.
