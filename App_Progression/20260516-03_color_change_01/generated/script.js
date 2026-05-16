const colors = ["#F94144", "#F8961E", "#F9C74F", "#90BE6D", "#43AA8B", "#577590"];

const button = document.getElementById("changeColorBtn");

if (!button) {
  throw new Error("Missing button element: changeColorBtn");
}

function pickRandomColor() {
  const index = Math.floor(Math.random() * colors.length);
  return colors[index];
}

button.addEventListener("click", () => {
  document.body.style.backgroundColor = pickRandomColor();
});
