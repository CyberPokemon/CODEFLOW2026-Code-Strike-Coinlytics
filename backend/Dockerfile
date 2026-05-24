# Use stable Maven with OpenJDK 21
FROM maven:3.9.6-eclipse-temurin AS build

WORKDIR /app

# Copy and download dependencies
COPY pom.xml .
RUN mvn dependency:go-offline

# Copy application source code
COPY src ./src

# Build application
RUN mvn clean package -DskipTests

# Use lightweight JDK image
FROM eclipse-temurin:21-jdk-jammy

WORKDIR /app

# Copy the JAR file correctly
COPY --from=build /app/target/backend-0.0.1-SNAPSHOT.jar /app/app.jar


# Expose port
EXPOSE 8080

ENTRYPOINT ["java","-jar","/app/app.jar"]