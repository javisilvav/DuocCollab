setTimeout(() => {
  const intereses = document.getElementById('intereses');
  if (intereses) {
    $('#intereses').select2({
      placeholder: 'Etiquetas',
      tags: true,
      width: '516px'
    });
  }
}, 100);

setTimeout(() => {
  const colaboradores = document.getElementById('colaboradores');
  if (colaboradores) {
    $('#colaboradores').select2({
      placeholder: 'Añadir colaboradores',
      tags: true,
      width: '516px'
    });
  }
}, 100);

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
$('#colaboradores').on('change', function () {
  const selectedIds = $(this).val(); // IDs seleccionados

  if (selectedIds && selectedIds.length > 0) {
    const nombresCompletos = selectedIds.map(id => {
      const option = $(`#colaboradores option[value="${id}"]`);
      const nombre = option.data('nombre') || '';
      const apellido = option.data('apellido') || '';
      return `${nombre} ${apellido}`.trim();
    });

    prevColaboradores.textContent = nombresCompletos.join(', ');
  } else {
    prevColaboradores.textContent = "autores, colaboradores";
  }
});
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