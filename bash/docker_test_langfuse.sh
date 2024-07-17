docker run --name tmp_langfuse \
--rm \
-e DATABASE_URL=postgresql://khangnh:mysecretpassword@172.17.0.2:5432/langfuse \
-e NEXTAUTH_URL=http://localhost:3000 \
-e NEXTAUTH_SECRET=mysecret \
-e SALT=mysalt \
-p 3000:3000 \
-a STDOUT \
langfuse/langfuse:2