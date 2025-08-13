# Wingz Exam

## How to Run

1. Make sure you have **Docker** and **Docker Compose** installed on your system.
2. Clone the repository to your local machine:  

   ```bash
   git clone https://github.com/clarence89/Wingz_Assessment.git
   ```

3. Go into the project folder:

   ```bash
   cd Wingz_Assessment
   ```

4. Start the application using Docker Compose:

   ```bash
   docker-compose up
   ```

5. In a separate terminal, create a **superuser** for admin login:

   ```bash
   docker-compose exec ride_web  python manage.py createsuperuser
   ```

   Follow the prompts to set username, email, and password.

6. Once the containers are running:
   - Visit `http://localhost:8000` to open Django.
   - Visit `http://localhost:8000/swagger` for the API documentation (Swagger UI).
   - Log in using the superuser credentials you just created.

---

## Postman Collection

```json
{
 "info": {
  "_postman_id": "725615f8-c0f4-4754-b7d4-f77508daa113",
  "name": "Rides API Flow",
  "description": "Full workflow from login to ride creation, update, listing, deletion, and ride events",
  "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json",
  "_exporter_id": "29014621",
  "_collection_link": "https://thealphadevs.postman.co/workspace/Team-Workspace~9bf3e20a-c514-4036-8bc4-192264d2700c/collection/29014621-725615f8-c0f4-4754-b7d4-f77508daa113?action=share&source=collection_link&creator=29014621"
 },
 "item": [
  {
   "name": "1. Login",
   "event": [
    {
     "listen": "test",
     "script": {
      "exec": [
       "var jsonData = pm.response.json();\r",
       "\r",
       "if (jsonData.access_token) {\r",
       "    pm.globals.set(\"token\", jsonData.access_token);\r",
       "} else if (jsonData.token) {\r",
       "    pm.globals.set(\"token\", jsonData.token);\r",
       "} else if (jsonData.access) {\r",
       "    pm.globals.set(\"token\", jsonData.access);\r",
       "} else {\r",
       "    console.log(\"No token found in the response\");\r",
       "}\r",
       ""
      ],
      "type": "text/javascript",
      "packages": {}
     }
    }
   ],
   "request": {
    "method": "POST",
    "header": [
     {
      "key": "Content-Type",
      "value": "application/json"
     }
    ],
    "body": {
     "mode": "raw",
     "raw": "{\n    \"username\": \"yourusername\",\n    \"password\": \"yourpassword\"\n}"
    },
    "url": {
     "raw": "http://localhost:8000/api/token/",
     "protocol": "http",
     "host": [
      "localhost"
     ],
     "port": "8000",
     "path": [
      "api",
      "token",
      ""
     ]
    }
   },
   "response": []
  },
  {
   "name": "2. Create Ride",
   "request": {
    "auth": {
     "type": "bearer",
     "bearer": [
      {
       "key": "token",
       "value": "{{token}}",
       "type": "string"
      }
     ]
    },
    "method": "POST",
    "header": [
     {
      "key": "Authorization",
      "value": "Bearer {{token}}"
     },
     {
      "key": "Content-Type",
      "value": "application/json"
     }
    ],
    "body": {
     "mode": "raw",
     "raw": "{\n    \"status\": \"pickup\",\n    \"rider_id\": 1,\n    \"driver_id\": 1,\n    \"pickup_latitude\": 14.5995,\n    \"pickup_longitude\": 120.9842\n}"
    },
    "url": {
     "raw": "http://localhost:8000/api/rides/",
     "protocol": "http",
     "host": [
      "localhost"
     ],
     "port": "8000",
     "path": [
      "api",
      "rides",
      ""
     ]
    }
   },
   "response": []
  },
  {
   "name": "3. List Rides",
   "request": {
    "auth": {
     "type": "bearer",
     "bearer": [
      {
       "key": "token",
       "value": "{{token}}",
       "type": "string"
      }
     ]
    },
    "method": "GET",
    "header": [
     {
      "key": "Authorization",
      "value": "Bearer {{token}}",
      "disabled": true
     }
    ],
    "url": {
     "raw": "http://localhost:8000/api/rides/",
     "protocol": "http",
     "host": [
      "localhost"
     ],
     "port": "8000",
     "path": [
      "api",
      "rides",
      ""
     ]
    }
   },
   "response": []
  },
  {
   "name": "4. Update Ride",
   "request": {
    "auth": {
     "type": "bearer",
     "bearer": [
      {
       "key": "token",
       "value": "{{token}}",
       "type": "string"
      }
     ]
    },
    "method": "PUT",
    "header": [
     {
      "key": "Authorization",
      "value": "Bearer {{access_token}}",
      "disabled": true
     },
     {
      "key": "Content-Type",
      "value": "application/json"
     }
    ],
    "body": {
     "mode": "raw",
     "raw": "{\n    \"status\": \"dropoff\",\n    \"rider_id\": 1,\n    \"driver_id\": 1,\n    \"pickup_latitude\": 11,\n    \"pickup_longitude\": 11,\n    \"dropoff_latitude\": 1,\n    \"dropoff_longitude\": 1\n}"
    },
    "url": {
     "raw": "http://localhost:8000/api/rides/1/",
     "protocol": "http",
     "host": [
      "localhost"
     ],
     "port": "8000",
     "path": [
      "api",
      "rides",
      "1",
      ""
     ]
    }
   },
   "response": []
  },
  {
   "name": "5. Create Ride Event",
   "request": {
    "auth": {
     "type": "bearer",
     "bearer": [
      {
       "key": "token",
       "value": "{{token}}",
       "type": "string"
      }
     ]
    },
    "method": "POST",
    "header": [
     {
      "key": "Authorization",
      "value": "Bearer {{access_token}}",
      "disabled": true
     },
     {
      "key": "Content-Type",
      "value": "application/json"
     }
    ],
    "body": {
     "mode": "raw",
     "raw": "{\n    \"ride_id\": 1,\n    \"description\": \"Reached pickup point\"\n}"
    },
    "url": {
     "raw": "http://localhost:8000/api/ride_events/",
     "protocol": "http",
     "host": [
      "localhost"
     ],
     "port": "8000",
     "path": [
      "api",
      "ride_events",
      ""
     ]
    }
   },
   "response": []
  },
  {
   "name": "6. List Ride Events",
   "request": {
    "auth": {
     "type": "bearer",
     "bearer": [
      {
       "key": "token",
       "value": "{{token}}",
       "type": "string"
      }
     ]
    },
    "method": "GET",
    "header": [
     {
      "key": "Authorization",
      "value": "Bearer {{access_token}}",
      "disabled": true
     }
    ],
    "url": {
     "raw": "http://localhost:8000/api/ride_events/",
     "protocol": "http",
     "host": [
      "localhost"
     ],
     "port": "8000",
     "path": [
      "api",
      "ride_events",
      ""
     ]
    }
   },
   "response": []
  },
  {
   "name": "7. Delete Ride",
   "request": {
    "auth": {
     "type": "bearer",
     "bearer": [
      {
       "key": "token",
       "value": "{{token}}",
       "type": "string"
      }
     ]
    },
    "method": "DELETE",
    "header": [
     {
      "key": "Authorization",
      "value": "Bearer {{access_token}}",
      "disabled": true
     }
    ],
    "url": {
     "raw": "http://localhost:8000/api/rides/1/",
     "protocol": "http",
     "host": [
      "localhost"
     ],
     "port": "8000",
     "path": [
      "api",
      "rides",
      "1",
      ""
     ]
    }
   },
   "response": []
  }
 ],
 "variable": [
  {
   "key": "access_token",
   "value": ""
  }
 ]
}
```

## SQL Report Query

The following query returns the **count of trips longer than 1 hour**, grouped by **month** and **driver**.

```sql
WITH pickup_dropoff AS (
    SELECT
        r.id AS ride_id,
        r.pickup_time,
        r.driver_id,
        MIN(CASE WHEN LOWER(re.description) = 'status changed to pickup' THEN re.created_at END) AS pickup_time_actual,
        MIN(CASE WHEN LOWER(re.description) = 'status changed to dropoff' THEN re.created_at END) AS dropoff_time_actual
    FROM
        rides_ride r
    JOIN
        rides_rideevent re ON r.id = re.ride_id
    GROUP BY
        r.id, r.pickup_time, r.driver_id
)
SELECT
    TO_CHAR(pd.pickup_time, 'YYYY-MM') AS monthyear,
    u.first_name || ' ' || LEFT(u.last_name, 1) || '.' AS driver_name,
    COUNT(*) AS trip_count
FROM
    pickup_dropoff pd
JOIN
    users_user u ON pd.driver_id = u.id
WHERE
    EXTRACT(EPOCH FROM (pd.dropoff_time_actual - pd.pickup_time_actual)) > 3600
GROUP BY
    monthyear, driver_name
ORDER BY
    monthyear DESC, driver_name;
```

---

## Notes from Me (Developer)

I set this up using **Docker Compose** because it makes running the app way easier — especially for someone new setting it up on a fresh machine.  

Here’s what’s included:

- **Django backend** with **Django REST Framework** and **SimpleJWT** for authentication.
- **Postgres** database (with PostGIS support for location queries).
- Ready for **Trench** if we want to add 2FA later.

**Why Docker?**

- No need to manually install Postgres or mess with database configs.
- Everything runs in isolated containers, so nothing conflicts with your local environment.
- If something breaks, you just restart the containers.

To run the project locally, you only need:

```bash
docker-compose up --build
```

and then create the superuser with:

```bash
docker-compose exec web python manage.py createsuperuser
```
