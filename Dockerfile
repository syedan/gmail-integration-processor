# Use the official PostgreSQL image from Docker Hub
FROM postgres:16.2

# Set environment variables for PostgreSQL
ENV POSTGRES_DB=mydatabase
ENV POSTGRES_USER=myuser
ENV POSTGRES_PASSWORD=mypassword

# Allow PostgreSQL to accept connections from all network interfaces
COPY pg_hba.conf /etc/postgresql/pg_hba.conf
RUN echo "listen_addresses='*'" >> /etc/postgresql/postgresql.conf

# Expose the PostgreSQL port to the host machine
EXPOSE 5432

# Start PostgreSQL when the container starts
CMD ["postgres"]
