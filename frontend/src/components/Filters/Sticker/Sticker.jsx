import React, { useState } from "react";
import { uploadSticker } from "../../../services/api";

const Sticker = ({ file, onResult }) => {
  const [loading, setLoading] = useState(false);

  const handleGenerate = async () => {
    if (!file) return;

    try {
      setLoading(true);
      const resultUrl = await uploadSticker(file);
      onResult(resultUrl); // send result back to Upload.jsx
    } catch (error) {
      console.error(error);
      alert("Failed to generate Sticker.");
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
      {loading ? "Processing Sticker..." : "Sticker"}
    </button>
  );
};

export default Sticker;
