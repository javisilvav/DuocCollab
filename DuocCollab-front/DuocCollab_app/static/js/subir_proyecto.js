// Agregar hashtags
const listaHashtags = document.getElementById("lista-hashtags");
const btnAgregarHashtag = document.getElementById("agregar-hashtag");

// Lista en memoria de hashtags agregados
let hashtagsArray = [];

// Al presionar "+"
btnAgregarHashtag.addEventListener("click", () => {
  let tag = hashtags.value.trim();

  // Asegurar que comience con #
  if (tag && !tag.startsWith("#")) {
    tag = "#" + tag;
  }

  if (tag && !hashtagsArray.includes(tag)) {
    hashtagsArray.push(tag);
    hashtags.value = ""; // limpiar input

    // Mostrar lista visual debajo del input
    renderHashtags();

    // Actualizar la vista previa con los hashtags separados por coma
    prevHashtags.textContent = hashtagsArray.join(", ");
  }
});

// Función para renderizar la lista debajo del input
function renderHashtags() {
  listaHashtags.innerHTML = hashtagsArray.map((tag, index) =>
    `<span class="badge bg-secondary me-1 mb-1" style="cursor: pointer;" data-index="${index}" title="Haz clic para eliminar">${tag} ✕</span>`
  ).join("");

  // Agrega evento de clic a cada badge para eliminarlo
  const badges = listaHashtags.querySelectorAll(".badge");
  badges.forEach(badge => {
    badge.addEventListener("click", () => {
      const index = badge.getAttribute("data-index");
      hashtagsArray.splice(index, 1); // eliminar de array
      renderHashtags(); // volver a renderizar
      prevHashtags.textContent = hashtagsArray.length > 0 ? hashtagsArray.join(", ") : "#tags";
    });
  });
}


// Agregar colaboradores
const listaColaboradores = document.getElementById("lista-colaboradores");
const btnAgregarColaborador = document.getElementById("agregar-colaborador");

// Lista en memoria de colaboradores agregados
let colaboradoresArray = [];

// Al presionar "+"
btnAgregarColaborador.addEventListener("click", () => {
  const nombre = colaboradores.value.trim();

  if (nombre && !colaboradoresArray.includes(nombre)) {
    colaboradoresArray.push(nombre);
    colaboradores.value = ""; // limpiar input

    // Mostrar lista visual debajo del input
    renderColaboradores();

    // Actualizar la vista previa con los nombres separados por coma
    prevColaboradores.textContent = colaboradoresArray.join(", ");
  }
});

// Función para renderizar la lista debajo del input
function renderColaboradores() {
  listaColaboradores.innerHTML = colaboradoresArray.map((nombre, index) =>
    `<span class="badge bg-secondary me-1 mb-1" style="cursor: pointer;" data-index="${index}" title="Haz clic para eliminar">${nombre} ✕</span>`
  ).join("");

  // Agrega evento de clic a cada badge para eliminarlo
  const badges = listaColaboradores.querySelectorAll(".badge");
  badges.forEach(badge => {
    badge.addEventListener("click", () => {
      const index = badge.getAttribute("data-index");
      colaboradoresArray.splice(index, 1); // eliminar de array
      renderColaboradores(); // volver a renderizar
      prevColaboradores.textContent = colaboradoresArray.join(", "); // actualizar vista previa
    });
  });
}



// Referencias a elementos del formulario
const titulo = document.getElementById("titulo");
const descripcion = document.getElementById("descripcion");
const requisitos = document.getElementById("requisitos");
const carrera = document.getElementById("carrera");
const colaboradores = document.getElementById("colaboradores");
const archivo = document.getElementById("archivo");
const sede = document.getElementById("sede");
const nombre_proyecto = document.getElementById("nombre_proyecto");

// Vista previa
const prevTitulo = document.getElementById("prev-titulo");
const prevDescripcion = document.getElementById("prev-descripcion");
const prevNombre = document.getElementById("prev-nombre");
const prevSede = document.getElementById("prev-sede");
const prevColaboradores = document.getElementById("prev-colaboradores");
const prevArchivo = document.getElementById("prev-archivo");
const prevCarrera = document.getElementById("prev-carrera");
const prevReq = document.getElementById("prev-req");

// Actualización de campos de texto
titulo.addEventListener("input", () => prevTitulo.textContent = titulo.value || "Lorem Ipsum");
descripcion.addEventListener("input", () => prevDescripcion.textContent = descripcion.value || "Sin descripción.");
nombre_proyecto.addEventListener("input", () => prevNombre.textContent = nombre_proyecto.value || "Lorem Ipsum");
requisitos.addEventListener("input", () => prevReq.textContent = requisitos.value || "requisitos");
carrera.addEventListener("input", () => prevCarrera.textContent = carrera.value || "Ingenieria en informatica");
colaboradores.addEventListener("input", () => prevColaboradores.textContent = colaboradores.value || "autores, colaboradores");
sede.addEventListener("input", () => prevSede.textContent = sede.value || "San Bernardo");



// Mostrar imagen o nombre del archivo
archivo.addEventListener("change", () => {
  const file = archivo.files[0];

  if (!file) {
    prevArchivo.textContent = "📎";
    return;
  }

  // Si es imagen
  if (file.type.startsWith("image/")) {
    const reader = new FileReader();
    reader.onload = () => {
      prevArchivo.innerHTML = `<img src="${reader.result}" alt="Vista previa" style="max-height: 100%; max-width: 100%;">`;
    };
    reader.readAsDataURL(file);
  } else {
    prevArchivo.textContent = "📎 " + file.name;
  }
});