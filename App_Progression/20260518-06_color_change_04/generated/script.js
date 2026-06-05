"use strict";

// Policy data extracted from guardrails markdown
const policies = {
  michigan: {
    id: "michigan",
    school: "University of Michigan",
    allowed_colors: [
      { name: "Michigan Blue", value: "#00274C" },
      { name: "Michigan Maize", value: "#FFCB05" },
      { name: "White", value: "#FFFFFF" }
    ]
  },
  stanford: {
    id: "stanford",
    school: "Stanford University",
    allowed_colors: [
      { name: "Stanford Cardinal", value: "#8C1515" },
      { name: "Palo Alto Green", value: "#175E54" },
      { name: "Cool Gray", value: "#4D4F53" }
    ]
  }
};

const defaultPolicyId = "michigan";

// State
let selectedSchoolId = defaultPolicyId;
let selectedColor = null;

// DOM Elements
const schoolSelect = document.getElementById("schoolSelect");
const colorSelect = document.getElementById("colorSelect");
const colorButtons = document.getElementById("colorButtons");

function checkDomNodes() {
  if (!schoolSelect) throw new Error("Missing DOM node: schoolSelect");
  if (!colorSelect) throw new Error("Missing DOM node: colorSelect");
  if (!colorButtons) throw new Error("Missing DOM node: colorButtons");
}

// Render school options
function render_schools() {
  checkDomNodes();
  schoolSelect.innerHTML = "";
  Object.values(policies).forEach(policy => {
    const option = document.createElement("option");
    option.value = policy.id;
    option.textContent = policy.school;
    schoolSelect.appendChild(option);
  });
  schoolSelect.value = selectedSchoolId;
}

// Render colors for selected school
function render_colors_for_selected_school() {
  checkDomNodes();
  const policy = policies[selectedSchoolId];
  if (!policy) return;

  // Clear colorSelect
  colorSelect.innerHTML = "";

  // Clear colorButtons
  colorButtons.innerHTML = "";

  policy.allowed_colors.forEach(color => {
    // Add option to colorSelect
    const option = document.createElement("option");
    option.value = color.value;
    option.textContent = color.name;
    colorSelect.appendChild(option);

    // Add button to colorButtons
    const btn = document.createElement("button");
    btn.type = "button";
    btn.textContent = color.name;
    btn.style.backgroundColor = color.value;
    btn.setAttribute("data-color", color.value);
    btn.setAttribute("aria-label", `Set background color to ${color.name}`);
    colorButtons.appendChild(btn);
  });

  // Reset selectedColor
  selectedColor = null;
}

// Apply first allowed color of current policy
function apply_first_allowed_color() {
  const policy = policies[selectedSchoolId];
  if (!policy || !policy.allowed_colors.length) return;
  const firstColor = policy.allowed_colors[0].value;
  apply_color_if_allowed(firstColor);
  // Update selects
  colorSelect.value = firstColor;
  selectedColor = firstColor;
}

// Check if color is allowed for current policy
function is_color_allowed(colorValue) {
  const policy = policies[selectedSchoolId];
  if (!policy) return false;
  return policy.allowed_colors.some(c => c.value.toLowerCase() === colorValue.toLowerCase());
}

// Apply color if allowed
function apply_color_if_allowed(colorValue) {
  if (!is_color_allowed(colorValue)) return;
  document.body.style.backgroundColor = colorValue;
  selectedColor = colorValue;
}

// Apply selected color from colorSelect if allowed
function apply_selected_color_if_allowed() {
  checkDomNodes();
  const colorValue = colorSelect.value;
  if (!colorValue) return;
  if (is_color_allowed(colorValue)) {
    apply_color_if_allowed(colorValue);
  }
}

// Apply clicked color button if allowed
function apply_clicked_color_if_allowed(event) {
  checkDomNodes();
  const target = event.target;
  if (target.tagName !== "BUTTON") return;
  const colorValue = target.getAttribute("data-color");
  if (!colorValue) return;
  if (is_color_allowed(colorValue)) {
    apply_color_if_allowed(colorValue);
    // Update colorSelect to match
    colorSelect.value = colorValue;
  }
}

// Event handlers
function on_school_change() {
  selectedSchoolId = schoolSelect.value;
  render_colors_for_selected_school();
  apply_first_allowed_color();
}

function on_color_change() {
  apply_selected_color_if_allowed();
}

function on_color_button_click(event) {
  apply_clicked_color_if_allowed(event);
}

// Initialization
function init() {
  checkDomNodes();
  render_schools();
  render_colors_for_selected_school();
  apply_first_allowed_color();

  schoolSelect.addEventListener("change", on_school_change);
  colorSelect.addEventListener("change", on_color_change);
  colorButtons.addEventListener("click", on_color_button_click);
}

window.addEventListener("load", init);
