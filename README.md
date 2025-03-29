# Gestor de Pagos Mensuales

![Python](https://img.shields.io/badge/Python-3.x-blue.svg)

## Descripción

**Gestor de Pagos Mensuales** es una aplicación educativa desarrollada en Python, diseñada para practicar conceptos básicos de programación. Este proyecto se enfoca en el manejo de archivos CSV, estructuras de datos, interacción con el usuario y manipulación de fechas. Su objetivo es gestionar clientes y sus pagos mensuales, registrando y actualizando la información en un archivo CSV, lo que lo convierte en una herramienta ideal para aprender sin fines comerciales.

## Características Principales

- **Gestión de Clientes:**
  - **Añadir Cliente:** Registra un nuevo cliente ingresando su nombre, fecha de inicio, monto mensual y una breve descripción.
  - **Editar Cliente:** Permite modificar o eliminar la información de un cliente existente.
  
- **Manejo de Pagos:**
  - **Registrar Pagos:** Marca a un cliente como "pagado" y actualiza la fecha de su próximo pago automáticamente, sumando un mes.
  - **Visualización de Ganancias:** Muestra las ganancias programadas para el mes actual, el siguiente mes o para una fecha específica ingresada por el usuario.

- **Persistencia de Datos:**
  - Los datos se almacenan en un archivo `clientes.csv` ubicado en la carpeta `datos`, garantizando que la información se conserve entre sesiones.

## Requisitos

- **Python 3.x:** Asegúrate de tener instalada una versión 3.x de Python.
- **Módulos Estándar:** No se requieren dependencias externas, ya que se utilizan únicamente módulos integrados de Python como `datetime`, `csv` y `os`.

Notas Adicionales
Propósito Educativo: Este proyecto está diseñado para aprender y practicar conceptos básicos de programación. No se recomienda su uso en entornos de producción.

Extensibilidad: La estructura del código permite ampliar fácilmente las funcionalidades o adaptarlo a diferentes contextos según tus necesidades.
