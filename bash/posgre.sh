docker run --name postgres_db -p 5432:5432 -v postgres_data:/var/lib/postgresql/data -e POSTGRES_PASSWORD=mysecretpassword -e POSTGRES_USER=khangnh -d postgres:13.15
