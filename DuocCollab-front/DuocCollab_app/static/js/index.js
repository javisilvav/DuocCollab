const carreras = {
  informatica: [
    'Ingeniería en Informática',
    'Técnico en Redes y Telecomunicaciones',
    'Ingeniería en Redes y Telecomunicaciones',
    'Analista Programador'
  ],
  ingenieria: [
    'Ingeniería en Mantenimiento Industrial',
    'Técnico Veterinario y Pecuario',
    'Técnico en Maquinaria y Vehículos Pesados',
    'Técnico en Electricidad y Automatización Industrial',
    'Ingeniería en Medio Ambiente',
    'Ingeniería en Mecánica Automotriz y Autotrónica',
    'Ingeniería en Maquinaria y Vehículos Pesados',
    'Ingeniería en Electricidad y Automatización Industrial',
    'Ingeniería Agrícola',
    'Técnico Agrícola',
    'Técnico en Mecánica Automotriz y Autotrónica',
  ],
  negocios: [
    'Contabilidad General Mención Legislación Tributaria',
    'Comercio Exterior',
    'Técnico en Gestión Logística',
    'Ingeniería en Comercio Exterior',
    'Técnico en Administración',
    'Ingeniería en Gestión Logística',
    'Ingeniería en Administración Mención Gestión de Personas',
    'Ingeniería En Administración Mención Finanzas',
    'Ingeniería en Marketing Digital',
    'Auditoría'
  ],
  construccion: [
    'Ingeniería en Prevención de Riesgos',
    'Ingeniería en Construcción',
    'Técnico en Construcción',
    'Dibujo y Modelamiento Arquitectónico y Estructural'
  ],
  salud: [
    'Técnico en Química y Farmacia',
    'Informática Biomédica',
    'Técnico de Laboratorio Clínico y Banco de Sangre',
    'Técnico en Odontología',
    'Técnico de Enfermería',
    'Preparador Físico'
  ],
  turismo: [
    'Administración en Turismo y Hospitalidad Mención Gestión de Destinos Turísticos',
    'Administración en Turismo y Hospitalidad Mención Gestión para el Ecoturismo',
    'Administración en Turismo y Hospitalidad Mención Administración Hotelera'
  ]
};

const coloresEscuelas = {
  informatica: '#307FE2',
  ingenieria: '#43B02A',
  negocios: '#AC4FC6',
  construccion: '#E87722',
  salud: '#5BC2E7',
  turismo: '#00A499'
};

function mostrarCarreras(escuela) {
  const lista = document.getElementById("carreras-lista");
  const contenedor = document.getElementById("carreras-container");
  lista.innerHTML = "";

  carreras[escuela].forEach(carrera => {
    const li = document.createElement("li");
    li.textContent = carrera;
    lista.appendChild(li);
  });

  contenedor.style.backgroundColor = coloresEscuelas[escuela];

  contenedor.style.display = "block";
}