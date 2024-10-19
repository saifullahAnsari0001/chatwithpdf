Chat with Multiple PDFs :books:
This app enables users to upload multiple PDF files, process the content, and ask questions about the documents. The app uses Pinecone for vector storage, Cohere’s language model for generating responses, and Streamlit to provide a simple, interactive interface for communication.

Features
Multiple PDF Uploads: Upload multiple PDF files simultaneously and extract the content from all of them.
Interactive Q&A: Ask questions about the uploaded PDFs, and the bot will respond with answers based on the content of those files.
Conversational Memory: The bot remembers previous questions and answers within the session, making follow-up questions seamless.
Installation
Requirements
Ensure that you have the following installed on your system:
Python 3.8+

git clone https://github.com/saifullahAnsari0001/chatwithpdf.git
cd chatwithpdf

Install Dependencies
To install the necessary Python dependencies, run:

pip install -r requirements.txt
Set up Environment Variables
Create a .env file in the root of your project directory and add your Pinecone and Cohere API keys:

PINECONE_API_KEY=your_pinecone_api_key
COHERE_API_KEY=your_cohere_api_key
Usage
To run the app, use the following command:

streamlit run app.py
Steps to Use:
Upload PDF Files:

In the sidebar, upload multiple PDF files by clicking on the Browse button.
Click Process to extract text from the PDFs and generate the vector embeddings.
Ask a Question:

Once the documents are processed, type your question into the input box at the top.
The bot will respond based on the content of the uploaded PDFs.
View Responses:

The bot's responses will appear below the input box. You can ask follow-up questions as the bot maintains the conversation history.
Example Interaction
Upload PDFs:

Upload Research_Paper_1.pdf, Project_Report_2023.pdf, and User_Manual_Technology.pdf.
Ask Questions:

User: "What are the key points in Research Paper 1?"

Bot: "The key points from Research Paper 1 are: 1) The main research objective is... 2) The methodology involves... 3) The conclusion suggests..."

User: "What conclusions are made in the Project Report?"

Bot: "The conclusion of the Project Report states that the 2023 project met its objectives by achieving..."

Potential Use Cases
Research Assistance: Upload research papers or reports and quickly query specific sections of interest.
Business Insights: Extract financial insights from business reports or analyze the conclusions of project summaries.
Manual/Guide Lookup: Ask for instructions or explanations from technical manuals or user guides.
Requirements and Limitations
Document Size: Larger PDFs may take longer to process.
Question Complexity: While the bot can handle a wide range of questions, more complex queries might require specific phrasing.
Future Enhancements
Add support for more document types (e.g., DOCX, TXT).
Implement more robust error handling for invalid file formats.
Expand functionality for summarization and keyword extraction.

Acknowledgments
Pinecone for vector storage.
Cohere for the language model.
Streamlit for the UI framework.
