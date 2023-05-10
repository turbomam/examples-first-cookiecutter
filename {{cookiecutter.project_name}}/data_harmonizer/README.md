# Getting Started with DataHarmonizer

This project was bootstrapped with `create-data-harmonizer`.

## Available Scripts

In the project directory, you can run:

### `npm run dev`

Runs the app in the development mode.
Open [http://localhost:5173](http://localhost:5173) to view it in your browser.

### `npm run build`

Builds the app for production to the `dist` folder. This directory can be deployed to any static hosting service, such as [GitHub Pages](https://docs.github.com/en/pages/quickstart).

### `npm run preview`

Previews the production build locally.

## Schema Management

This project depends on `project/json/nmdc_submission_schema.json`. When changes to that file (either manually or as the result of a build process) are detected while the dev server are running the interface will automatically reload. When the interface is built for production, an optimized copy of this schema will be created in the build output directory. 
