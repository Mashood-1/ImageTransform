import React, { useState } from "react";
import { uploadNeonGlow } from "../../../services/api";

const NeonGlow = ({ file, onResult }) => {
  const [loading, setLoading] = useState(false);

  const handleGenerate = async () => {
    if (!file) return;

    try {
      setLoading(true);
      const resultUrl = await uploadNeonGlow(file);
      onResult(resultUrl); // send result back to Upload.jsx
    } catch (error) {
      console.error(error);
      alert("Failed to generate Neon Glow.");
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
      {loading ? "Processing Neon Glow..." : "Neon Glow"}
    </button>
  );
};

export default NeonGlow;
