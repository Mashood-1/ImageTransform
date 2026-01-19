import React, { useState } from "react";
import { uploadManga } from "../../../services/api";

const Manga = ({ file, onResult }) => {
  const [loading, setLoading] = useState(false);

  const handleGenerate = async () => {
    if (!file) return;

    try {
      setLoading(true);
      const resultUrl = await uploadManga(file);
      onResult(resultUrl); // send result back to Upload.jsx
    } catch (error) {
      console.error(error);
      alert("Failed to generate Manga Effect.");
    } finally {
      setLoading(false);
    }
  };

  if (!file) return null;

  return (
    <button
      className="action-button"
      onClick={handleGenerate}
      disabled={loading}
    >
      {loading ? "Processing Manga..." : "Manga"}
    </button>
  );
};

export default Manga;
