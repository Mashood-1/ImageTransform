import React, { useState } from "react";
import { uploadPopArt } from "../../../services/api";

const PopArt = ({ file, onResult }) => {
  const [loading, setLoading] = useState(false);

  const handleGenerate = async () => {
    if (!file) return;

    try {
      setLoading(true);
      const resultUrl = await uploadPopArt(file);
      onResult(resultUrl);
    } catch (error) {
      console.error(error);
      alert("Failed to generate Pop Art.");
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
      {loading ? "Processing Pop Art..." : "Pop Art"}
    </button>
  );
};

export default PopArt;
