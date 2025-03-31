# Contributing Guide

## Metodología de Trabajo con GitFlow

Utilizamos la metodología GitFlow para el manejo de ramas y versiones. La estructura de ramas es la siguiente:

- **main**: Contiene la última versión estable y lista para producción.
- **develop**: Rama de integración donde se agrupan nuevas funcionalidades y correcciones.
- **feature/**: Ramas para el desarrollo de nuevas funcionalidades.
- **bugfix/**: Ramas para corregir errores detectados.
- **hotfix/**: Ramas para resolver problemas críticos en producción.

Cada desarrollo se realiza en una rama específica que sigue la nomenclatura correspondiente (por ejemplo, `feature/nueva-funcionalidad`). Una vez completado, se crea un Pull Request (PR) hacia `develop`, donde al menos otro miembro del equipo debe aprobarlo.

## Reporte de Issues

Utilizamos GitHub Issues para el manejo de incidencias. El proceso para crear un issue es el siguiente:

1. Crear un issue siguiendo el template predefinido.
2. Incluir una descripción clara del problema o la funcionalidad solicitada.
3. Utilizar etiquetas (tags) para clasificar el issue, como:
   - `bug`: Errores menores que no impiden el uso.
   - `future feature`: Funcionalidades adicionales.
   - `UI enhancement`: Mejoras de la interfaz.
   - `blocking bug`: Errores críticos que impiden el uso.
   - `documentation`: Falta de documentación.

## Pull Requests (PR)

Los PR deben incluir referencias a los issues que resuelven. El proceso es el siguiente:

1. Crear un PR desde la rama correspondiente hacia `develop`.
2. Solicitar revisión de al menos otro miembro del equipo.
3. Asegurarse de que el código pase las pruebas automatizadas (GitHub Actions).
4. Incluir una descripción detallada de los cambios realizados.

## Estándares de Código

Para asegurar la calidad del código, seguimos estas prácticas:

- Uso de linters (ESLint, Pylint) y formatters (Prettier, Black) para mantener consistencia.
- Realización de pruebas unitarias para asegurar la funcionalidad (UnitTest para backend).
- Realización de pruebas end-to-end para verificar el comportamiento completo.

## Proceso de Releases

Utilizamos el versionado semántico (SemVer) siguiendo el esquema X.Y.Z (Major.Minor.Patch). Cada versión se marca con un tag en Git con sem-ver según lo que se fuera a integrar. El despliegue se realiza de forma manual en AWS.

## GitHub Actions

Hemos configurado GitHub Actions para automatizar las siguientes tareas:

- Ejecutar pruebas unitarias y de integración en cada commit y PR.
- Realizar análisis estático del código para detectar errores comunes.
- Garantizar consistencia en el formato del código.

Estos procesos se ejecutan automáticamente en cada PR o al realizar un commit en cualquier rama activa.
