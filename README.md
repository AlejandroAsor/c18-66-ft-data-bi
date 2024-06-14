# Tech Path Finder

<img src="https://github.com/Angeljs094/JobMatchAI/blob/main/images/logo.png"  height=400>


## Equipo del Proyecto

- Alejandro Asor Corrales Gómez
- Angel Jaramillo Sulca


## Objetivo

El objetivo principal de Tech Path Finder es desarrollar una aplicación web interactiva que permita visualizar ofertas laborales relacionadas con las tecnologías más demandadas en el ámbito tecnológico. La plataforma ayuda a los usuarios a tomar decisiones fundamentadas sobre su formación y especialización académica, basándose en las oportunidades laborales disponibles en el mercado tecnológico.

## Identificación del Problema

La rápida evolución del sector de las tecnologías de la información presenta desafíos significativos para los individuos que aspiran a ingresar o avanzar en este campo. La abundancia de recursos educativos y la diversidad de roles profesionales complican la elección de un itinerario formativo y profesional claro y eficaz. Además, existe una notable discrepancia entre las competencias enseñadas en los ámbitos académicos y aquellas demandadas en el mercado laboral.


## Descripción de la Solución

La solución propuesta por el proyecto "Tech Path Finder" es facilitar la visualización de ofertas laborales en el ámbito tecnológico. Esta plataforma proporciona información actualizada y relevante sobre las tecnologías más demandadas, incluyendo herramientas de lenguajes de programación, roles y base de datos. Su objetivo es ayudar a los usuarios a tomar decisiones informadas sobre su formación y especialización, alineando sus habilidades con las necesidades del mercado laboral.


## Tecnologías y Herramientas Utilizadas

<table>
  <tr>
    <td align="center"><img src="https://www.python.org/static/community_logos/python-logo.png" alt="Python" height="60"/></td>
    <td align="center"><img src="https://upload.wikimedia.org/wikipedia/commons/thumb/d/d5/Selenium_Logo.png/600px-Selenium_Logo.png" alt="Selenium" height="60"/></td>
    <td align="center"><img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS7k538EfZUljBbMXTKewRhX4kXi0KjV4qEkg&s" alt="AWS" height="60"/></td>
  </tr>
  <tr>
    <td align="center"><b>Python</b></td>
    <td align="center"><b>Selenium</b></td>
    <td align="center"><b>AWS</b></td>
  </tr>
  <tr>
    <td align="center"><img src="https://upload.wikimedia.org/wikipedia/commons/thumb/2/29/Postgresql_elephant.svg/1024px-Postgresql_elephant.svg.png" alt="PostgreSQL" height="60"/></td>
    <td align="center"><img src="https://upload.wikimedia.org/wikipedia/commons/thumb/f/f4/Elasticsearch_logo.svg/1200px-Elasticsearch_logo.svg.png" alt="Elasticsearch" height="60"/></td>
    <td align="center"><img src="https://upload.wikimedia.org/wikipedia/commons/thumb/f/f3/Apache_Spark_logo.svg/800px-Apache_Spark_logo.svg.png" alt="Apache Spark" height="60"/></td>
  </tr>
  <tr>
    <td align="center"><b>PostgreSQL</b></td>
    <td align="center"><b>Elasticsearch</b></td>
    <td align="center"><b>Apache Spark</b></td>
  </tr>
  <tr>
    <td align="center"><img src="https://streamlit.io/images/brand/streamlit-logo-primary-colormark-darktext.png" alt="Streamlit" height="60"/></td>
    <td align="center"><img src="https://upload.wikimedia.org/wikipedia/commons/e/ed/Pandas_logo.svg" alt="Pandas" height="60"/></td>
    <td align="center"><img src="https://www.sqlalchemy.org/img/sqla_logo.png" alt="SQLAlchemy" height="60"/></td>
  </tr>
  <tr>
    <td align="center"><b>Streamlit</b></td>
    <td align="center"><b>Pandas</b></td>
    <td align="center"><b>SQLAlchemy</b></td>
  </tr>
  <tr>
    <td align="center"><img src="https://images.plot.ly/logo/new-branding/plotly-logomark.png" alt="Plotly" height="60"/></td>
    <td align="center"><img src="https://camo.githubusercontent.com/19694a747faa4c55cbdb1cab99086099c6cf961930712f87ab3469e9bf706a4f/68747470733a2f2f68756767696e67666163652e636f2f64617461736574732f68756767696e67666163652f646f63756d656e746174696f6e2d696d616765732f7261772f6d61696e2f7472616e73666f726d6572732d6c6f676f2d6c696768742e737667" alt="Transformers" height="60"/></td>
    <td align="center"><img src="https://upload.wikimedia.org/wikipedia/commons/0/05/Scikit_learn_logo_small.svg" alt="Scikit Learn" height="60"/></td>
  </tr>
  <tr>
    <td align="center"><b>Plotly</b></td>
    <td align="center"><b>Transformers</b></td>
    <td align="center"><b>Scikit Learn</b></td>
  </tr>
  <tr>
    <td align="center"><img src="https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png" alt="GitHub" height="60"/></td>
    <td align="center"><img src="https://hackernoon.imgix.net/images/oS3VPBDztmPNM9laovQw4x5lwE83-fqh3eg3.jpeg" alt="Llama3" height="60"/></td>
  </tr>
  <tr>
    <td align="center"><b>GitHub</b></td>
    <td align="center"><b>Llama3</b></td>
  </tr>
</table>


## Arquitectura de Procesamiento de Datos

El siguiente diagrama ilustra el flujo de datos en el sistema Tech Path Finder, desde la base de datos PostgreSQL hasta Elasticsearch, utilizando Apache Spark para el procesamiento de datos:

![el drawio](https://github.com/AlejandroAsor/c18-66-ft-data-bi/assets/84219142/cb9024c6-070f-4ff0-b83f-85bd32eba977)

1. **PostgreSQL**: La base de datos PostgreSQL almacena las ofertas laborales recopiladas.
2. **Apache Spark**: Apache Spark se utiliza para procesar grandes volúmenes de datos. Los datos son extraídos de PostgreSQL, procesados por Spark y luego enviados a Elasticsearch. El procesamiento es distribuido a través de múltiples nodos de trabajo (workers) para aumentar la eficiencia y la velocidad.
3. **Elasticsearch**: Los datos procesados son indexados en Elasticsearch, lo que permite búsquedas y análisis rápidos y eficientes.

Este flujo asegura que las ofertas laborales estén siempre actualizadas y sean fácilmente accesibles para los usuarios de la plataforma.


# Esquema de la Base de Datos Centralizada

Este esquema de la base de datos está diseñado para centralizar y organizar datos extraídos de múltiples fuentes de bases de datos, similar a la indexación inversa en Elasticsearch pero implementada en PostgreSQL de manera más artesanal.

<img width="632" alt="image" src="https://github.com/AlejandroAsor/c18-66-ft-data-bi/assets/84219142/6b0eee83-4486-4001-88ae-f8b9f0afb4dd">

## Componentes del Esquema

A continuación se describen las principales tablas del esquema y sus relaciones:

- **source_database**
  - `name`: Nombre de la base de datos de origen.
  - `date_created`: Fecha de creación de la entrada.
  - `id`: Identificador único de la fuente.

- **locations**
  - `country`: País de la ubicación.
  - `id`: Identificador único de la ubicación.

- **salaries**
  - `amount`: Monto del salario como texto.
  - `amount_cleaned`: Monto del salario procesado y normalizado.
  - `id`: Identificador único del salario.

- **experience_levels**
  - `level`: Descripción del nivel de experiencia.
  - `level_cleaned`: Nivel de experiencia normalizado.
  - `id`: Identificador único del nivel de experiencia.

- **job_listings**
  - `experience_level_id`: ID del nivel de experiencia asociado.
  - `source_db_id`: ID de la base de datos de origen.
  - `location_id`: ID de la ubicación.
  - `salary_id`: ID del salario.
  - `date_scraped`: Fecha en que se extrajo la oferta.
  - `date_posted`: Fecha de publicación de la oferta.
  - `id`: Identificador único de la oferta de trabajo.

- **keywords**
  - `keyword`: Palabra clave.
  - `date_created`: Fecha de creación de la palabra clave.
  - `date_update`: Fecha de la última actualización de la palabra clave.
  - `id`: Identificador único de la palabra clave.

- **job_keywords**
  - `title_count`: Conteo de apariciones del título.
  - `content_count`: Conteo de apariciones en el contenido.
  - `keyword_id`: ID de la palabra clave asociada.
  - `job_id`: ID de la oferta de trabajo asociada.

- **currency_conversion**
  - `conversion_rate`: Tasa de conversión de la moneda.
  - `country`: País de la moneda.

Este modelo facilita consultas complejas y precisas, permitiendo un análisis detallado y la recuperación eficiente de información relacionada con ofertas de trabajo.

## Metodología de Trabajo 
### Metodología Scrum
Scrum es un marco ágil que se enfoca en la entrega iterativa y flexible de proyectos. Los roles clave incluyen al Product Owner, quien representa las necesidades del cliente, al Scrum Master, que facilita el proceso, y al Equipo de Desarrollo, encargado de ejecutar el trabajo. Scrum se centra en eventos clave como los Sprints, reuniones de planificación y revisiones, y artefactos como el Product Backlog y el Sprint Backlog para proporcionar transparencia, adaptabilidad y colaboración continua en la gestión de proyectos.
<br>[Volver al Índice](#Índice)

### Recolección y Limpieza de Datos
 *Web Scraping: Implementación de scripts de web scraping para extraer datos de ofertas de trabajo de Computrabajo y Elempleo.
 *Limpieza de Datos: Procesamiento y limpieza de datos para asegurar su calidad y consistencia.

### Análisis de Datos y Generación de Visualizaciones
 *Comparación de Tendencias: Análisis comparativo de las tendencias entre los cinco países seleccionados.
 *Generación de Informes: Elaboración de informes detallados que presenten los hallazgos del análisis.
 

## Modelo de Negocio

El modelo de negocio se enfoca en proporcionar insights y análisis detallados a empresas de tecnología, instituciones educativas y profesionales del sector. La generación de ingresos se estructura de la siguiente manera:

- **Suscripciones:** 
  - Ofrecemos planes de suscripción mensuales o anuales.
  - Acceso a informes y análisis detallados.

- **Consultoría:** 
  - Servicios de consultoría especializados para interpretación y aplicación de datos.
  - Apoyo en decisiones estratégicas para mejorar la gestión empresarial.

- **Publicidad:** 
  - Espacios publicitarios disponibles en la plataforma.
  - Orientados a empresas de formación y reclutamiento que buscan una audiencia especializada.

- **Venta de Datos:** 
  - Venta de datos agregados y anonimizados.
  - Apoyo a empresas en estudios de mercado y análisis de tendencias.
