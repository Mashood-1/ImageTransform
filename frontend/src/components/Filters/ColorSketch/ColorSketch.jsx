import React, { useState } from "react";
import { uploadColorSketch } from "../../../services/api";

const ColorSketch = ({ file, onResult }) => {
  const [loading, setLoading] = useState(false);

  const handleGenerate = async () => {
    if (!file) return;

    try {
      setLoading(true);
      const resultUrl = await uploadColorSketch(file);
      onResult(resultUrl); // send result back to Upload.jsx
    } catch (error) {
      console.error(error);
      alert("Failed to generate Color Sketch.");
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
      {loading ? "Processing Color Sketch..." : "Color Sketch"}
    </button>
  );
};

export default ColorSketch;
