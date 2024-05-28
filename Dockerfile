# Use an official Python runtime as a parent image
FROM python:3.12.2-alpine

# Set the working directory in the container to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 8080 available to the world outside this container
EXPOSE 8080

# Define environment variables
ENV OPENAI_API_KEY=sk-proj-ZDINUmeoDvJo6WNibHv0T3BlbkFJdldHxoxC6gWTGIez9kYW
ENV GROQ_API_KEY=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
ENV FLASK_ENV=development
ENV FLASK_APP=server.py
ENV PORT=8080

# Run the app when the container launches
CMD ["flask", "run", "--host=0.0.0.0", "--port=8080"]