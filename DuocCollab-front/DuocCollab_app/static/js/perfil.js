function cargarContenido(seccion) {
  fetch(`/perfil/${seccion}/`)
    .then(response => response.text())
    .then(html => {
      document.getElementById('contenido-dinamico').innerHTML = html;

      // Reiniciar estilos de los enlaces
      const enlaces = document.querySelectorAll('.menu-link-perfil');
      enlaces.forEach(link => {
        link.classList.remove('fw-bold');
        link.innerHTML = link.dataset.label; // restaurar texto original sin '>'
      });

      // Aplicar estilo al enlace seleccionado
      const enlaceActivo = document.querySelector(`.menu-link-perfil[data-section="${seccion}"]`);
      if (enlaceActivo) {
        enlaceActivo.classList.add('fw-bold');
        enlaceActivo.innerHTML = `> ${enlaceActivo.dataset.label}`;
      }

      // Inicializar Select2 si existe el campo
      setTimeout(() => {
        const intereses = document.getElementById('intereses');
        if (intereses) {
          $('#intereses').select2({
            placeholder: 'Selecciona tus intereses',
            tags: true,
            width: '100%'
          });
        }
      }, 100);
    })
    .catch(error => {
      console.error('Error al cargar la sección:', error);
    });
}
// Cargar la sección "postulaciones" por defecto al cargar la página
document.addEventListener('DOMContentLoaded', function () {
  cargarContenido('postulaciones');
});