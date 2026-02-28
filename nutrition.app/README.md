# Nutrition & Training Planner

Motor de decisión para planificación nutricional y de entrenamiento personalizado.

## 📋 Descripción

Aplicación web que calcula perfiles metabólicos y nutricionales personalizados basados en las características físicas y objetivos del usuario. Utiliza ecuaciones científicas validadas (Mifflin-St Jeor) para proporcionar recomendaciones precisas de calorías y macronutrientes.

## 🚀 Características

- **Cálculo Metabólico Preciso**: Usa la ecuación Mifflin-St Jeor para BMR y TDEE
- **Planificación Nutricional**: Distribución automática de macronutrientes
- **Múltiples Objetivos**: Pérdida de peso, mantenimiento o ganancia muscular
- **Interfaz Web Amigable**: Formulario intuitivo con resultados en tiempo real
- **Recomendaciones Personalizadas**: Sistema de IA que genera consejos accionables
- **Visualización de Datos**: Gráficos de progreso nutricional

## 🛠️ Tecnologías

- **Backend**: Python 3.11+
- **Framework Web**: Flask
- **Procesamiento de Datos**: Pandas, NumPy
- **Visualización**: Matplotlib
- **Estructura**: Dataclasses para modelos de datos

## 📁 Estructura del Proyecto

```
nutrition.app/
├── models/                 # Modelos de datos
│   ├── user_profile.py    # Perfil de usuario
│   └── calculation_result.py # Resultados de cálculos
├── services/              # Lógica de negocio
│   ├── metabolic_service.py    # Cálculos metabólicos
│   ├── nutrition_service.py    # Análisis nutricional
│   ├── recommendation_engine.py # Motor de recomendaciones
│   ├── calories.py            # Gráficos de calorías
│   ├── protein.py             # Gráficos de proteína
│   └── data_gen.py           # Generación de datos
├── templates/             # Plantillas HTML
│   └── index.html         # Interfaz principal
├── static/               # Archivos estáticos
├── utils/                # Utilidades
│   └── constants.py      # Constantes y factores
├── app.py               # Aplicación Flask
├── main.py              # Demostración CLI
└── requirements.txt     # Dependencias
```

## 🚀 Instalación

1. **Clonar el repositorio**:
   ```bash
   git clone <repository-url>
   cd nutrition.app
   ```

2. **Crear entorno virtual**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```

3. **Instalar dependencias**:
   ```bash
   pip install -r requirements.txt
   ```

## 🏃‍♂️ Uso

### Modo Web (Recomendado)

```bash
python app.py
```

Visita `http://localhost:5000` y completa el formulario con tus datos:
- Peso, altura, edad y sexo
- Nivel de actividad (sedentario a muy alto)
- Objetivo (pérdida, mantenimiento o volumen)
- Calorías actuales y de entrenamiento (opcional)

### Modo Demostración CLI

```bash
python main.py
```

Ejecuta análisis con 4 perfiles de ejemplo predefinidos.

## 🧮 Cálculos Realizados

### Metabólicos
- **BMR (Tasa Metabólica Basal)**: Ecuación Mifflin-St Jeor
- **TDEE (Gasto Energético Total)**: BMR × Factor de actividad
- **Factores de actividad**: 1.2 (sedentario) a 1.9 (muy alto)

### Nutricionales
- **Balance energético**: Ingesta vs gasto calórico
- **Calorías objetivo**: Ajustadas según objetivo del usuario
- **Distribución de macronutrientes**: Proteínas, grasas y carbohidratos

## 📊 Ejemplo de Resultados

El sistema proporciona:
- **Análisis metabólico**: BMR, TDEE y factor de actividad
- **Plan nutricional**: Calorías objetivo y distribución de macros
- **Recomendaciones personalizadas**: Consejos con nivel de confianza
- **Pasos accionables**: Plan concreto para alcanzar objetivos

## 🔧 Configuración

El proyecto incluye validaciones automáticas:
- Peso: 30-200 kg
- Altura: 100-250 cm  
- Edad: 15-100 años
- Niveles de actividad predefinidos
- Objetivos limitados a opciones válidas

## 📈 Próximas Mejoras

- [ ] Integración con bases de datos para historial
- [ ] API REST para integración con apps móviles
- [ ] Sistema de seguimiento de progreso
- [ ] Exportación de planes en PDF
- [ ] Integración con wearables para datos automáticos

## 📄 Licencia

Este proyecto es para fines demostrativos y educativos.

---

**Desarrollado como motor de decisión para planificación nutricional y de entrenamiento personalizado.**
