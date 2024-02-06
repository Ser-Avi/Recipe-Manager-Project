const tags = [];

function addTag() {
	const tag = document.getElementById("tag").value

	if (tag === "")
		return;

	tags.push(tag);

	const li = document.createElement("li");
	const node = document.createTextNode(tag);
	li.appendChild(node);

	const element = document.getElementById("tags");
	const deleteBtn = createDeleteBtn("Delete tag", () => {element.removeChild(li);});
	li.appendChild(deleteBtn)
	element.appendChild(li);

	document.getElementById("tag").value = "";
}

const ingredients = [];

function addIngredient() {
	const name = document.getElementById("ingredient_name").value
	const amount = document.getElementById("ingredient_amount").value
	const measurement = document.getElementById("ingredient_measurement").value

	if (name === "" || amount === "" || measurement === ""){
		return;
	}

	ingredients.push({name: name, amount: amount, measurement: measurement});
	
	const li = document.createElement("li");
	const node = document.createTextNode(`${name} ${amount} ${measurement}`);
	li.appendChild(node);

	const element = document.getElementById("ingredients");
	const deleteBtn = createDeleteBtn("Delete ingredient", () => {element.removeChild(li);});
	li.appendChild(deleteBtn)
	element.appendChild(li);

	document.getElementById("ingredient_name").value = "";
	document.getElementById("ingredient_amount").value = "";
	document.getElementById("ingredient_measurement").value = "";
}

const steps = [];

function addStep() {
	const step = document.getElementById("step").value

	if (step === "") {
		return;
	}

	steps.push(step);

	const li = document.createElement("li");
	const node = document.createTextNode(step);
	li.appendChild(node);

	const element = document.getElementById("steps");
	const deleteBtn = createDeleteBtn("Delete step", () => {element.removeChild(li);});
	li.appendChild(deleteBtn)
	element.appendChild(li);
	document.getElementById("step").value = "";
}

async function addRecipe() {
	const name = document.getElementById("name").value;
	const timeToMake = document.getElementById("time_to_make").value;
	const servings = document.getElementById("servings").value;

	const recipe = {
		name: name,
		tags: tags,
		timeToMake: timeToMake,
		servings: servings,
		ingredients: ingredients,
		steps: steps,
	};

	await fetch('/submit', {
		method: 'POST',
		headers: {
			'Accept': 'application/json',
			'Content-Type': 'application/json',
		},
		body: JSON.stringify(recipe)
	});
}


function createDeleteBtn(text, onRemove) {
	const button = document.createElement("BUTTON");
	button.innerText = text;
	button.addEventListener("click", () => onRemove());
	button.setAttribute("type", "button");
	return button;
}

