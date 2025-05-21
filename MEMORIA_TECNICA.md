# 📽️ Blog de Películas – Proyecto Final

## 👥 División del trabajo

**Cristofer Levy**  
Responsable del desarrollo del backend, encargado de implementar la lógica del sistema y garantizar el correcto funcionamiento de las funcionalidades.

**Carla Vásquez**  
Responsable del diseño visual del blog, enfocada en la reorganización de la estructura de la interfaz, la distribución de los elementos, a su vez la funcionalidad de la misma.

---

## 🛠️ ¿Qué implementamos?

> [!TIP]
> Este blog permite no solo escribir reseñas, sino también **calificar y comentar**, haciendo la experiencia más interactiva.

Nuestro proyecto consiste en un blog de películas que permite a los usuarios comentar y realizar reseñas sobre sus opciones favoritas de películas, así como calificarlas. El blog cuenta con las siguientes secciones principales:

---

### 🔐 Página de inicio de sesión y registro

> [!IMPORTANT]
> Este formulario sigue parámetros de seguridad esenciales, asegurando la protección de los datos personales ingresados.

Creamos un formulario elegante pero sencillo, pensado para ofrecer una experiencia de registro rápida y accesible para el usuario. Además, implementamos un inicio de sesión eficiente, permitiendo a los usuarios acceder fácilmente al sistema sin comprometer la seguridad ni la usabilidad.

---

### 🏠 Página de Home

**Encabezado (Header):**
- Botón de "Inicio"
- Botón para cambiar el tema del blog (modo claro/oscuro)
- Botón para crear un nuevo blog
- Botón para cerrar sesión

**Cuerpo del sitio:**

- **Columna izquierda:**  
  Muestra los blogs más recientes publicados por los usuarios. Cada blog incluye:  
  - Imagen destacada  
  - Título  
  - Nombre del autor  
  - Fecha de publicación  
  - Promedio de calificaciones recibidas

- **Columna derecha:**  
  Presenta el top 5 de los blogs con mayor calificación.

**Pie de página (Footer):**
- Logo del blog
- Términos de uso
- Correo de contacto

---

### ✍️ Página para Crear un Blog

> [!WARNING]
> En esta sección **todos los campos son obligatorios**. Asegúrate de completarlos correctamente antes de publicar.

Esta sección presenta un diseño moderno con estilo de nube y permite a los usuarios:

- Subir una imagen para el blog
- Escribir el título del blog
- Escribir una descripción detallada, utilizando un editor de texto enriquecido que permite aplicar distintos formatos al contenido
- Publicar el blog mediante un botón específico

---

### 📖 Página de Vista del Blog

Una vez publicado, el blog aparece en la sección de publicaciones recientes en el Home. Al hacer clic en "Leer más", se accede a una vista detallada del blog donde se visualizan:

- La imagen subida
- El título del blog
- La descripción realizada por el usuario
- Una sección de comentarios, donde otros usuarios pueden opinar sobre la reseña de la película y asignar una calificación a la publicación

---

## 🎓 ¿Qué aprendimos?

**Cristofer Levy:**  
Durante el desarrollo de este trabajo, aprendí a corregir errores y a codificar utilizando Django, entendiendo mejor su estructura y cómo moverme dentro del framework. A lo largo del proceso, fui adquiriendo diversos tips útiles para mejorar mi flujo de trabajo y optimizar mi código. También aprendí mucho de mis propios errores, lo que me ayudó a afianzar conceptos y evitar fallos comunes. Además, profundicé en aspectos de Python que complementan el desarrollo en Django, lo que me permitió tener una visión más completa del entorno y de cómo aprovecharlo al máximo.

**Carla Vásquez:**  
Antes de este proyecto, desconocía cómo utilizar Python y trabajar con Django. A lo largo del desarrollo, aprendí a aplicar funciones básicas y comprender cómo se integran con el diseño del sitio. También entendí la importancia de equilibrar la parte visual con el funcionamiento correcto del blog para brindar una buena experiencia al usuario.
