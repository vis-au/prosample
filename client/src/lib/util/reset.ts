export function reset() {
  fetch("http://127.0.0.1:5000/reset").then(() => console.log("pipelines were reset."));
}