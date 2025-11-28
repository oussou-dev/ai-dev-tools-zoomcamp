# Snake — React

Jeu Snake minimal construit avec React + Vite, utilisant un canevas (`canvas`) pour le rendu et Tailwind CSS pour le style.

**Fonctionnalités**
- Moteur de jeu simple avec boucle (interval) et détection de collision.
- Nourriture aléatoire, augmentation de la longueur du serpent et accélération progressive.
- Contrôles clavier (flèches / WASD), pause avec `Espace`, boutons pour démarrer/mettre en pause/recommencer.
- Styles fournis via `Tailwind CSS`.

**Prérequis**
- Node.js (version 16+ recommandée) et `npm` installés.

**Installation & développement**
1. Depuis la racine du projet, ouvrez un terminal dans le dossier `snake_game` :

```bash
cd snake_game
```

2. Installez les dépendances :

```bash
npm install
```

3. Lancez le serveur de développement Vite :

```bash
npm run dev
```

4. Ouvrez l'URL indiquée par Vite (par défaut `http://localhost:5173`).

**Commandes utiles**
- `npm run dev` : démarre le serveur de développement.
- `npm run build` : construit le bundle de production dans `dist/`.
- `npm run preview` : sert le build produit pour vérification locale.

**Contrôles**
- Déplacer : flèches du clavier ou `W A S D`.
- Pause / reprise : appuyer sur `Espace`.
- Boutons : `Start` / `Pause` / `Restart` depuis l'interface.

**Structure importante**
- `index.html` : point d'entrée HTML chargé par Vite.
- `src/main.jsx` : point d'entrée React.
- `src/App.jsx` : composant racine.
- `src/SnakeGame.jsx` : logique et rendu du jeu (canevas).
- `src/index.css` : directives Tailwind et styles composants.
- `tailwind.config.cjs` et `postcss.config.cjs` : configuration Tailwind/PostCSS.

**Dépannage**
- Erreur PostCSS / Tailwind :
	- Assurez-vous d'avoir installé `tailwindcss`, `postcss` et `autoprefixer` dans `snake_game/package.json`.
	- Si Vite signale une erreur disant que le plugin PostCSS a changé, utilisez la configuration compatible (le projet utilise la config standard pour Tailwind v3).
- Si le style n'apparaît pas, vérifiez que `@tailwind base; @tailwind components; @tailwind utilities;` sont présents dans `src/index.css` et que `tailwind.config.cjs` référence bien les fichiers `index.html` et `src/**/*`.

**Améliorations possibles**
- Touch controls pour mobile.
- Sauvegarde du meilleur score dans `localStorage`.
- Animations CSS / transitions pour l'UI.
- Options de difficulté (vitesse initiale, grille plus grande).

**Crédits**
Ce dépôt contient un exemple simple réalisé comme démo; vous pouvez le forker et l'adapter.

---

Si vous voulez, je peux :
- Lancer `npm run dev` ici pour vérifier (si l'environnement autorise l'exécution).
- Ajouter le stockage du meilleur score.
- Ajouter des contrôles tactiles pour mobile.

Dites-moi quelle option vous intéresse.
