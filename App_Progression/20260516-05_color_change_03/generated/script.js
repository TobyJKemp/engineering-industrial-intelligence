const policyMap = {
  "michigan": { school: "University of Michigan", colors: [{ name: "Michigan Blue", value: "#00274C" }, { name: "Michigan Maize", value: "#FFCB05" }, { name: "White", value: "#FFFFFF" }] },
  "stanford": { school: "Stanford University", colors: [{ name: "Stanford Cardinal", value: "#8C1515" }, { name: "Palo Alto Green", value: "#175E54" }, { name: "Cool Gray", value: "#4D4F53" }] }
};

const schoolSelect = document.getElementById("schoolSelect");
const colorSelect = document.getElementById("colorSelect");
const buttonContainer = document.getElementById("colorButtons");

if (!schoolSelect || !colorSelect || !buttonContainer) {
  throw new Error("Missing one or more required UI elements.");
}

function setBackground(color) {
  document.body.style.backgroundColor = color;
}

function renderSchools() {
  const ids = Object.keys(policyMap);
  schoolSelect.innerHTML = ids
    .map((id) => `<option value="${id}">${policyMap[id].school}</option>`)
    .join("");

  const fallback = ids.includes("michigan") ? "michigan" : ids[0];
  schoolSelect.value = fallback;
}

function renderColors(policyId) {
  const policy = policyMap[policyId];
  if (!policy) {
    return;
  }

  colorSelect.innerHTML = policy.colors
    .map((item) => `<option value="${item.value}">${item.name}</option>`)
    .join("");

  buttonContainer.innerHTML = "";
  policy.colors.forEach((item) => {
    const button = document.createElement("button");
    button.type = "button";
    button.textContent = item.name;
    button.addEventListener("click", () => setBackground(item.value));
    buttonContainer.appendChild(button);
  });

  if (policy.colors.length > 0) {
    colorSelect.value = policy.colors[0].value;
    setBackground(policy.colors[0].value);
  }
}

schoolSelect.addEventListener("change", (event) => {
  renderColors(event.target.value);
});

colorSelect.addEventListener("change", (event) => {
  const schoolId = schoolSelect.value;
  const policy = policyMap[schoolId];
  const isAllowed = policy && policy.colors.some((item) => item.value === event.target.value);
  if (isAllowed) {
    setBackground(event.target.value);
  }
});

renderSchools();
renderColors(schoolSelect.value);
