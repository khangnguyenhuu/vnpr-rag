docker run --name tmp_langfuse \
--rm \
-v `
-e DATABASE_URL=postgresql://root:gotit!321@localhost:5432/langfuse \
-e NEXTAUTH_URL=http://localhost:3000 \
-e NEXTAUTH_SECRET=mysecret \
-e SALT=mysalt \
-p 3000:3000 \
-a STDOUT \
langfuse/langfuse:2