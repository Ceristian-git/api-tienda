# 🖥️ API Tienda de PCs - Documentación para Postman

Esta API permite gestionar un CRUD de computadores (PCs) y obtener recomendaciones personalizadas según el presupuesto y propósito del usuario.

---

## 🔗 Base URL

```
http://[localhost]:8000
```

---

## 📦 Endpoints CRUD - PCs

### 📥 Crear una PC

- **Método:** `POST`
- **URL:** `/pcs`
- **Body (JSON):**
```json
{
  "nombre": "[nombre]",
  "procesador": "[procesador]",
  "ram": "[ram]",
  "almacenamiento": "[almacenamiento]",
  "tarjeta_grafica": "[tarjeta_grafica]"
}
```

---

### 📄 Listar todas las PCs

- **Método:** `GET`
- **URL:** `/pcs`

---

### 🔍 Obtener una PC por ID

- **Método:** `GET`
- **URL:** `/pcs/[id]`

---

### ✏️ Actualizar una PC

- **Método:** `PUT`
- **URL:** `/pcs/[id]`
- **Body (JSON):** Igual al de creación

---

### 🗑️ Eliminar una PC

- **Método:** `DELETE`
- **URL:** `/pcs/[id]`

---

## 🔐 Autenticación

### 🔑 Iniciar sesión

- **Método:** `POST`
- **URL:** `/login`
- **Body (x-www-form-urlencoded):**
```
username=[usuario]
password=[contraseña]
```

- **Respuesta esperada:**
```json
{
  "access_token": "[token]"
}
```

---

## 🤖 Recomendación con IA

### 💡 Obtener recomendación de PC

- **Método:** `POST`
- **URL:** `/recomendar/`
- **Headers:**
```
Authorization: Bearer [token]
```

- **Body (JSON):**
```json
{
  "presupuesto": [presupuesto],
  "objetivo": "[objetivo]"
}
```

---

## 📌 Notas

- Esta API usa MongoDB para almacenar la información.
- Requiere autenticación con JWT para acceder al endpoint `/recomendar/`.
