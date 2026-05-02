# Predicción de Precios de Vehículos - Mockup

Este es un mockup funcional (front-end only) para simular un sistema predictivo de precios de vehículos. Está construido con **React** y **Vite**, y no requiere ninguna conexión a backend ni a base de datos.

## Características
- Diseño moderno Glassmorphism centrado en UX/UI.
- Simulación de carga (spinner y mensajes dinámicos).
- Lógica algorítmica interna para calcular un precio base simulado dependiente de Marca, Modelo, Año y Kilometraje.
- Totalmente responsivo.
- Listo para desplegar en plataformas serverless como Vercel.

## Desarrollo Local

1. Instala las dependencias:
   ```bash
   npm install
   ```

2. Ejecuta el servidor de desarrollo local:
   ```bash
   npm run dev
   ```

3. Abre `http://localhost:5173` en tu navegador.

## Despliegue en Vercel

Esta aplicación está optimizada y lista para ser desplegada en Vercel sin configuraciones adicionales.

### Método 1: GitHub (Recomendado)
1. Sube este código a un repositorio en GitHub.
2. Inicia sesión en [Vercel](https://vercel.com).
3. Haz clic en **Add New... > Project**.
4. Importa el repositorio de GitHub.
5. Vercel detectará automáticamente que es un proyecto Vite.
6. Haz clic en **Deploy**.

### Método 2: Vercel CLI
Si prefieres usar la terminal:
1. Instala Vercel CLI: `npm i -g vercel`
2. Ejecuta en la raíz del proyecto:
   ```bash
   vercel
   ```
3. Sigue las instrucciones en consola (acepta la configuración por defecto para Vite). Para subir a producción, ejecuta `vercel --prod`.

## Personalización
Puedes añadir el branding o las guías de diseño en el archivo `branding-lines.md`.
También, reemplaza los divs "[Imagen del vehículo aquí]" en `src/App.jsx` con tus assets finales.
