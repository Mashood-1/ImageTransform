import React, { useState } from "react";
import { uploadComicArt } from "../../../services/api";

const ComicArt = ({ file, onResult }) => {
  const [loading, setLoading] = useState(false);

  const handleGenerate = async () => {
    if (!file) return;

    try {
      setLoading(true);
      const resultUrl = await uploadComicArt(file);
      onResult(resultUrl); // send result back to Upload.jsx
    } catch (error) {
      console.error(error);
      alert("Failed to generate Comic Art.");
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
      {loading ? "Processing Comic Art..." : "Comic Art"}
    </button>
  );
};

export default ComicArt;
