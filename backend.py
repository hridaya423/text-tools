import mindsdb_sdk

# Create a MindsDB client instance
server = mindsdb_sdk.connect('http://127.0.0.1:47334')

project = server.get_project()

summarizer = project.models.get('cohere_text_summarization')
generator = project.models.get('cohere_text_generation')
