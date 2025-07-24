# LLM-PDF-Summarizer-
#Run the commands:

Install Python.<br>
Install Ollama.<br>
Run the following commands to get everything set up and test the scripts:-<br>
&nbsp;&nbsp;ollama run mistral.<br><br>

python -m venv venv<br>
venv\Scripts\activate &nbsp;&nbsp;# On Windows<br>
pip install fastapi uvicorn streamlit requests<br><br>
pip install streamlit transformers torch pdfminer.six


Get the following scripts ready:<br>
├── streamlit_app.py &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;# Streamlit frontend<br><br>

Run Ollama in a terminal: ollama serve<br><br>

Run Streamlit frontend:<br>
cd path\to\LLM_Project<br>
streamlit run app.py

App opens at: [http://localhost:8501](http://localhost:8501)

