# Equipo 5: Ingeniería y Calidad de Software 4k1
El presente documento tiene como propósito definir los lineamientos para la gestión de la configuración de la materia Ingeniería y Calidad de Software durante todo su desarrollo.
El plan de gestión de configuración estará disponible en el directorio raíz del repositorio, bajo el nombre “PGC.md”, lo que permitirá su consulta y modificación de manera sencilla.
De esta forma, los integrantes tendrán acceso rápido y centralizado a la información necesaria.

## Integrantes del equipo
| Apellido y Nombre | Legajo |
|--------------|------|
| Bacchin, Rosario | 90229 |
| Barrios, Martina | 98678 |
| De Giorgi, Matteo | 90056 |
| Escudero Garay, Candela | 91516 |
| Felippa, Alexis | 90843 |
| Jaureguialzo, Carolina Belen | 94278 |
| Odar Alejos, Yanella Esmeralda | 95230 |
| Osella, Lourdes | 97245 |

## Estructura
Hemos definido la siguiente estructura de directorios, organizada en función del desarrollo y gestión del cursado de la materia Ingeniería y Calidad de Software.

&lt;img width="829" height="864" alt="Estructura&#95;PCG drawio" src="https://github.com/user-attachments/assets/dc0e8708-e188-44e4-b0b7-de860c1d8fbb" /&gt;

## Convención de Nombrado de Items de Configuración
- Para Carpetas:
  - Utilizar el estilo snake&#95;case.
  - No usar caracteres especiales ni espacios.
- Para Archivos:
  - Respetar la nomenclatura respectiva a cada Item. 
  - Separar palabras utilizando "&#95;".
  - Se permiten mayúsculas, minúsculas y números.
  - No usar caracteres especiales.

## Ítems de Configuración
| Item de Configuracion | Nomenclatura | Definición | Ubicación |
|-----------------------|--------------|------------|-----------|
| Plan de Gestión de Configuración | PGC.md | Definición de la estructura del repositorio | / |
| Material Bibliografico | BIBLIO&#95;&lt;nombre&#95;libro&gt;.pdf | Material de referencia académico | /material&#95;teorico/material&#95;de&#95;la&#95;uv/bibliografia |
| Presentacion de Clase | PPT&#95;&lt;nombre&#95;presentacion&gt;.&lt;pdf/ppt/pptx&gt; | Diapositivas elaboradas por los docentes de la cátedra | /material&#95;teorico/material&#95;de&#95;la&#95;uv/presentacion&#95;de&#95;clases |
| Notas de Clase Teórico | NOTA&#95;&lt;dd-mm-aa&gt;&#95;&lt;nombre&#95;persona&gt;&#95;&lt;nro&#95;archivo&gt;.&lt;pdf/docx/jpg/png&gt; | Notas tomadas para la clase teórica de la fecha (dd//mm/aa) indicada | /material&#95;teorico/material&#95;de&#95;elaboracion&#95;propia/notas&#95;de&#95;clases |
| Resumen | RES&#95;&lt;tema&#95;res&gt;.&lt;docx/pdf&gt; | Resumen para el &lt;tema&#95;res&gt; indicado | /material&#95;teorico/material&#95;de&#95;elaboracion&#95;propia/resumenes |
| Trabajos Practicos Evaluables | TPS.pdf | Consignas de Trabajos Prácticos a realizar | /material&#95;practico/trabajos&#95;practicos&#95;evaluables |
| Resolución de Trabajo Practico | TP&#95;&lt;nro&#95;tp&gt;.pdf | Resolución del Trabajo Práctico número &lt;nro&#95;tp&gt; realizado | /material&#95;practico/trabajos&#95;practicos/tp&#95;&lt;nro&#95;tp&gt; |
| Resolución de Trabajo de Investigación | TI&#95;&lt;nro&#95;ti&gt;.pdf | Resolución del Trabajo de Investigación número &lt;nro&#95;ti&gt; realizado | /material&#95;practico/trabajos&#95;de&#95;Investigación |
| Minutas | MIN&#95;&lt;dd-mm-aa&gt;.pdf | Registro de acuerdos y tareas de cada reunión del TP &lt;nro&#95;tp&gt; | /material&#95;practico/trabajos&#95;practicos&#95;evaluables/tp&#95;&lt;nro&#95;tp&gt;/minutas |
| Casos de Estudio | CE.pdf | Descripción de todos los Casos de Estudio | /material&#95;practico/ejercitacion/casos&#95;de&#95;estudio |
| Casos de Estudio de Resolución Propia | CERP&#95;&lt;nombre&#95;caso&gt;&#95;&lt;nombre&#95;persona&gt;.pdf | Resolución de Casos de estudio resueltos por el Grupo 5 | /material&#95;practico/ejercitacion/casos&#95;de&#95;estudio |
| Notas de clase Práctico | NOTA&#95;&lt;dd-mm-aa&gt;&#95;&lt;nombre&#95;persona&gt;&#95;&lt;nro&#95;archivo&gt;.&lt;pdf/docx/jpg/png&gt; | Notas tomadas para la clase práctica de la fecha (dd/mm/aa) indicada | /material&#95;practico/notas&#95;de&#95;clases |



## Glosario
| Termino | Descripción |
|-----------------------|--------------|
| PGC | Plan de Gestión de Configuración de Software |
| BIBLIO | Material Bibliográfico |
| PPT | Presentación |
| NOTA | Nota de clases |
| RES | Resumen |
| TPS | Trabajos Prácticos Evaluables|
| TP | Trabajos Prácticos Evaluables Resueltos |
| TI | Trabajos de Investigación Resueltos |
| CE | Casos de Estudio |
| CERP | Casos de Estudio de Resolución Propia |
| MIN | Minuta |

| Variable | Descripción |
|-----------------------|--------------|
| &lt;nombre&#95;libro&gt; | Nombre del libro referenciado en material bibliográfico |
| &lt;nombre&#95;presentacion&gt; | Nombre asignado a una presentación |
| &lt;dd-mm-aa&gt; | Fecha en el formato día-mes-año |
| &lt;tema&#95;res&gt; | Tema al que corresponde el resumen |
| &lt;nro&#95;tp&gt; | Número del Trabajo Práctico |
| &lt;nro&#95;ti&gt; | Número del Trabajo de Investigación |
| &lt;nombre&#95;caso&gt; | Nombre del caso de estudio |
| &lt;nombre&#95;ejercicio&gt; | Nombre del ejercicio |
| &lt;nombre&#95;persona&gt; | Nombre de la persona que creó el contenido |
| &lt;nro&#95;archivo&gt; | Número de secuencia del archivo, respetando el formato "nn", por ej.: "01", "02", "03"... |

## Criterio de Línea Base
Definimos como criterio de línea base del repositorio, que la misma se establecerá luego de la corrección de dos trabajos prácticos, considerando únicamente los prácticos evaluables. Decidimos este criterio, ya que, consideramos que luego de la corrección de dos trabajos prácticos, contaremos con ítems de configuración validados y estables.
Como equipo, decidimos identificar de manera única cada versión de la línea base, definiendo que los nombres con los que vamos a identificar a cada una de las versiones serán con sabores de helado. 


