

````markdown
# 🕉️ Valmiki Ramayana Translation Verifier

This project checks if a user-submitted English translation of a verse from the *Valmiki Ramayana* is **factually correct**, **incorrect**, or **irrelevant**.  
It uses semantic search, reranking, and a local LLM to return structured outputs — with explanations, references, and correction suggestions.

---

## 🛠️ Features

- Extracts English verses from [valmikiramayan.net](http://www.valmikiramayan.net)
- Chunks and embeds verses for semantic search
- Finds and reranks most relevant verses using vector similarity + MMR
- Uses an LLM (LLaMA 3 via Ollama) for fact-checking and correction
- Outputs results in structured JSON format with reasons and references
- Saves results in CSV for further analysis

---

## 🧪 Setup Instructions


1. Make sure the following files are in the root folder: 

   * `valmiki_ramayana_dataset.xlsx`
   * `ramayana.py`
   * `requirements.txt`

2. Install dependencies: 

   ```bash
   pip install -r requirements.txt
   ```

3. Run the project: 

   ```bash
   python ramayana.py
   ```

---

## 🔍 Project Pipeline

### 1. Data Extraction (via Selenium)

* Navigates to `valmikiramayan.net` and switches to the `main` frame.
* Extracts all Book (Kanda) and Chapter (Sarga) links.
* For each verse:

  * Extracts the verse number and English translation.
  * Handles different HTML formats across books using custom logic and regex.
* Saves all verse data into `valmiki_ramayana_dataset.xlsx`.

### 2. Preprocessing

* Loads dataset and splits each verse into overlapping 300-character chunks (with 50-character overlap).
* Associates each chunk with its source verse metadata.

### 3. Embedding and Storage

* Uses `all-MiniLM-L6-v2` from HuggingFace to convert text into embeddings.
* Stores embeddings in a **Chroma vector database**, ideal for use with LangChain.

### 4. Semantic Search + Reranking

* Converts user translation into an embedding.
* Retrieves 20–30 similar chunks using **Maximal Marginal Relevance (MMR)**.
* Reranks results using `amberoad/bert-multilingual-passage-reranking-msmarco` to select top 6 most relevant chunks.

### 5. Fact-Checking using LLM

* Prompts LLaMA 3 with:

  * Top 6 relevant chunks
  * User translation to evaluate
* Returns structured JSON:

  ```json
  {
    "prediction": "correct/incorrect/irrelevant",
    "reason": "...",
    "reference": "...",
    "correction": "..." // only if incorrect
  }
  ```

### 6. Output Handling

* Uses regex cleanup to fix malformed LLM outputs.
* Parses and maps JSON into a structured DataFrame.
* Saves all final results to a CSV file.

---

## 🤖 Model Choices & Rationale

| Stage     | Model                                                  | Why Chosen                                                |
| --------- | ------------------------------------------------------ | --------------------------------------------------------- |
| Embedding | `all-MiniLM-L6-v2`                                     | Fast, free, and better semantic accuracy vs Ollama/others |
| Vector DB | Chroma                                                 | LangChain-compatible and local                            |
| Reranker  | `amberoad/bert-multilingual-passage-reranking-msmarco` | High cross-lingual matching performance                   |
| LLM       | LLaMA 3 via Ollama                                     | Local, tunable, gives structured reasoning                |

---

## ❌ Models We Tried But Rejected

### Embeddings:

* **Ollama’s nomic-embed-text**: Couldn’t match names like “Sita” vs “Seetha”
* **OpenAI / Cohere**: Paid or rate-limited

### Reranking:

* **Only MMR**: Returned diverse but inaccurate results without deeper comparison

### LLMs:

* **Bespoke-mini-check**: Returned only True/False, no explanations
* **Gemma 2B**: Struggled with structured outputs
* **Osmosis / Nemotron Mini**: JSON structure was inconsistent or incorrect

---

## 🔮 Future Improvements

* Try newer and faster embedding models for better precision.
* Improve UI of the Streamlit app version.
* Enhance handling of near-similar verses to reduce false negatives.
* Extend the system to other epics (e.g., Mahabharata) with minimal changes.

---

## 🧾 Output Sample

```json
{
  "prediction": "incorrect",
  "reason": "The translated line misrepresents the speaker and context of the verse.",
  "reference": "Sundara Kanda, Chapter 5, Verse 12",
  "correction": "Hanuman did not say that; it was spoken by Ravana."
}
```

---

## 🧑‍💻 Authors & Credits

This project was built using:

* Python, Selenium, Pandas, Regex
* HuggingFace Transformers
* Chroma DB
* LangChain
* Ollama + LLaMA 3
* [valmikiramayan.net](http://www.valmikiramayan.net) for source data

```


```
