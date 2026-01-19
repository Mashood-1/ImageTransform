// src/components/Filters/PixelArt/RetroPixelArt.jsx

import React, { useState } from "react";
import { uploadPixelArt } from "../../../services/api";

const RetroPixelArt = ({ file, onResult }) => {
  const [loading, setLoading] = useState(false);

  // Available pixel art styles
  const styles = ["8bit", "16bit", "modern", "mosaic"];

  const handleStyleSelect = async (style) => {
    if (!file) return;

    try {
      setLoading(true);
      const resultUrl = await uploadPixelArt(file, style);
      onResult(resultUrl);
    } catch (err) {
      console.error(err);
      alert(`Failed to apply pixel art style: ${style}`);
    } finally {
      setLoading(false);
    }
  };

  if (!file) return null;

  return (
    <div className="action-button-dropdown">
      <button className="action-button" disabled={loading}>
        {loading ? "Applying Pixel Art..." : "Pixel Art ▼"}
      </button>
      <div className="dropdown-menu">
        {styles.map((s) => (
          <button
            key={s}
            className="action-button dropdown-item"
            onClick={() => handleStyleSelect(s)}
            disabled={loading}
          >
            {s}
          </button>
        ))}
      </div>
    </div>
  );
};

export default RetroPixelArt;
