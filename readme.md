# django-svelte-flowbite

## Features

- [x] Django Rest Framework based JWT auth
- [x] Custom Django users
- [x] Svelte-Kit frontend
- [x] Custom Svelte-Django auth library
- [x] Flowbite UI Kit
- [x] Docker Compose with nginx

## Usage

`make local` will start docker compose and mount the appropriate directories. Sometimes it's necessary to clean out the frontend directory, `make clean` is available for that.

It's necessary to create `frontend/.env.development` and `frontend/.env.production`. The files should contain the following:

```
VITE_BASE_API_URI_DEV="http://localhost:81/api"
```

The above contents work for development however the value should be changed for production.

## Credit

Originally forked from [django_svelte_jwt_auth](https://github.com/Sirneij/django_svelte_jwt_auth/tree/main).