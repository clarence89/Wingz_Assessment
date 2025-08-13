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
