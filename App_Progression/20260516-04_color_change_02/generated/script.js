const buttons = [
  { id: "btnBlue", color: "blue" },
  { id: "btnRed", color: "red" },
  { id: "btnGreen", color: "green" },
  { id: "btnYellow", color: "yellow" },
  { id: "btnPurple", color: "purple" },
  { id: "btnOrange", color: "orange" }
];

const select = document.getElementById("colorSelect");

if (!select) {
  throw new Error("Missing dropdown element: colorSelect");
}

function setBackground(color) {
  document.body.style.backgroundColor = color;
}

buttons.forEach((buttonConfig) => {
  const button = document.getElementById(buttonConfig.id);
  if (!button) {
    throw new Error(`Missing button element: ${buttonConfig.id}`);
  }

  button.addEventListener("click", () => {
    setBackground(buttonConfig.color);
  });
});

select.addEventListener("change", (event) => {
  setBackground(event.target.value);
});
