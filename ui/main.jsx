import React from "react";
import { createRoot } from "react-dom/client";

async function main() {
  const rootElt = document.getElementById("app");
  const root = createRoot(rootElt);

  root.render(<h1>Hello From React!</h1>);
  root.render(<h2>This is another header!</h2>);
}

window.onload=main
