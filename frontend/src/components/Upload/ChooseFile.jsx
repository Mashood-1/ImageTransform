// frontend/src/components/Upload/ChooseFile.jsx

import React from "react";
import "./ChooseFile.css";

const ChooseFile = ({ onFileSelect }) => {
  const handleChange = (event) => {
    const file = event.target.files[0];
    if (!file) return;

    const supportedTypes = [
      "image/jpeg",
      "image/jpg",
      "image/png",
      "image/webp",
    ];

    if (!supportedTypes.includes(file.type)) {
      alert("Unsupported image type!");
      return;
    }

    onFileSelect(file);
  };

  return (
    <div className="choose-file-container">
      <input
        type="file"
        accept="image/*"
        id="fileInput"
        onChange={handleChange}
        className="choose-file-input"
      />
      <label htmlFor="fileInput" className="choose-file-button">
        Choose File
      </label>
    </div>
  );
};

export default ChooseFile;
