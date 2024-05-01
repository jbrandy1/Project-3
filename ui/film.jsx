import React from "react";
import { createRoot } from "react-dom/client";

function FilmEntry({ id, title, description }) {
  return (
    <p>
      <a href={`/film/{id}`}>{title}</a>: {description}
    </p>
  );
}

async function main() {

  const filmId = window.location.pathname.split("/").pop();

  const filmResponse = await fetch(`/api/v1/film/{filmId}`);
  const film = await filmResponse.json();

  const rootElt = document.getElementById("app");
  const root = createRoot(rootElt);
  root.render(
    <div>
      <FilmEntry
        id={film.film.id}
        title={film.title}
        description={film.description}
      />
    </div>
  );
}

window.onload=main
