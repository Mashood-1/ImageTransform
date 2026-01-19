import React, { useState } from "react";
import { uploadStyleTransfer } from "../../../services/api";

const StyleTransfer = ({ file, onResult }) => {
  const [loading, setLoading] = useState(false);

  // Available styles (match your .pth models in backend/models/instance_norm)
  const styles = ["candy", "mosaic", "rain_princess", "udnie"];

  const handleStyleSelect = async (style) => {
    if (!file) return;

    try {
      setLoading(true);
      const resultUrl = await uploadStyleTransfer(file, style);
      onResult(resultUrl);
    } catch (err) {
      console.error(err);
      alert(`Failed to apply style: ${style}`);
    } finally {
      setLoading(false);
    }
  };

  if (!file) return null;

  return (
    <div className="action-button-dropdown">
      <button className="action-button" disabled={loading}>
        {loading ? "Applying Style..." : "Style Transfer ▼"}
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

export default StyleTransfer;
