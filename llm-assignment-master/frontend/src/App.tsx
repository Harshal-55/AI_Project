import React, { useState, ChangeEvent, FormEvent } from "react";

export default function App(): JSX.Element {
  const [result, setResult] = useState<string>("");
  const [question, setQuestion] = useState<string>("");
  const [file, setFile] = useState<File | null>(null);

  const handleQuestionChange = (event: ChangeEvent<HTMLInputElement>): void => {
    setQuestion(event.target.value);
  };

  const handleFileChange = (event: ChangeEvent<HTMLInputElement>): void => {
    const selectedFile = event.target.files?.[0];
    if (selectedFile) {
      setFile(selectedFile);
    }
  };

  const handleSubmit = async (event: FormEvent<HTMLFormElement>): Promise<void> => {
    event.preventDefault();

    if (!file || !question) {
      console.error("Please provide both a file and a question.");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);
    formData.append("question", question);

    try {
      const response = await fetch("http://127.0.0.1:8000/predict", {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        throw new Error("Network response was not ok");
      }

      const data = await response.json();
      setResult(data.result);
    } catch (error) {
      console.error("Error:", error);
    }
  };

  return (
    <div className="appBlock">
      <form onSubmit={handleSubmit} className="form">
        <label htmlFor="question" className="questionLabel">
          Question:
        </label>
        <input
          id="question"
          type="text"
          value={question}
          onChange={handleQuestionChange}
          placeholder="Ask your question here"
          className="questionInput"
        />
        <br />
        <label htmlFor="file" className="fileLabel">
          Upload CSV file:
        </label>
        <input
          type="file"
          id="file"
          name="file"
          accept=".csv"
          onChange={handleFileChange}
          className="fileInput"
        />
        <br />
        <button type="submit" className="submitBtn" disabled={!file || !question}>
          Submit
        </button>
      </form>
      <p className="resultOutput">Result: {result}</p>
    </div>
  );
}
