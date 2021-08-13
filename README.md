# Dooger

Prueba tecnica

## Stack
* Django
* React

## Descripción:
Se está desarrollando una plataforma llamada “Dogger”. El objetivo de la app es conectar “dueños” de perros con “paseadores” de perros.

## Funcionalidades mínimas esperadas:
* Registrar usuarios “dueños”.
* Registrar usuarios “paseadores”.
* Un dueño puede registrar perros con su tamaño (Grande, Chico, Mediano).
* Un dueño puede reservar a un paseador en específico.
* Un dueño también puede pedir que alguien pasee a su perro en algún horario.
* Un paseador puede tener un máximo de 3 perros al mismo tiempo.
* Desde el punto de vista del paseador, puede recibir perros de múltiples dueños en cada reserva.
* Un paseador puede definir horarios para pasear ciertos tamaños de perro (chico, mediano, grande o alguna combinación de estos).

## Dependencias

Esta prueba fue construida bajo una arquitectura de microservicios, por lo que es requerido un microservicio de usuarios el cual gestione la authorización de los usuarios finales, este debe hacer uso de jwt cuyo payload contenga los siguientes campos:

```
{
    ...
    "exp": epoch,
    "user_id": uuid,
    "roles": list of roles (owner, walker)
    ...
}
```

Se recomienda el uso del siguiente microservicio:

* git@github.com:edcilo/edc_service_users.git

## Instalación del servicio dogger

1. Clonar repositorio
```
git clone git@github.com:edcilo/edc_service_dogger.git
```

2. Acceder al directorio del servicio
```
cd edc_service_dogger
```

3. Configurar variables de entorno
```
cp .env.example .env
```

4. Construir y ejecutar imagenes docker
```
docker-compose build
docker-compose up
```

5. Crear super user
```
dcker-compose exec edc_dogger_django sh
> python manage.py createsuperuser
```

6. Desde el navegador acceder a http://localhost:8001/admin/ y acceder como super user

## Endpoints

Endpoints correspondientes al crud de perros

* Crear un nuevo registro de un perro
```
POST /api/v1/dogs/
Auth: Bearer Token
Body:
{
    "name": string,
    "size": int
}
```

* Listar todos los perros del usuario autorizado
```
GET /api/v1/dogs/
Auth: Bearer Token
```

* Ver el detalle de un perro
```
POST /api/v1/dogs/{pk}/
Auth: Bearer Token
```

* Modificar los datos de un perro
```
PUT /api/v1/dogs/{pk}/
Auth: Bearer Token
Body:
{
    "name": string,
    "size": int
}
```

* Eliminar un registro de un perro
```
DELETE /api/v1/dogs/{pk}/
Auth: Bearer Token
```

Endpoints correspondientes al crud de paseadores de perros

* Registrar una hora de paseo
```
POST /api/v1/schedule/
Auth: Bearer Token
Body:
{
    "day": int,
    "start": int,
    "end": int,
    "sizes": list of dog size ids
}
```

* Listar todas las horas de paseo
```
GET /api/v1/schedule/
Auth: Bearer Token
```

* Ver detalle de una hora de paseo
```
GET /api/v1/schedule/{pk}/
Auth: Bearer Token
```

* Modificar una hora de paseo
```
PUT /api/v1/schedule/{pk}/
Auth: Bearer Token
Body:
{
    "day": int,
    "start": int,
    "end": int,
    "sizes": list of dog size ids
}
```

* Eliminar una hora de paseo
```
DELETE /api/v1/schedule/{pk}/
Auth: Bearer Token
```
