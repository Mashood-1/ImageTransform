// frontend/src/components/DownloadButton/DownloadButton.jsx

import React from "react";
import "./DownloadButton.css";

const DownloadButton = ({ url, filename = "image.png" }) => {
  if (!url) return null;

  return (
    <a
      href={url}
      download={filename}
      className="download-button"
    >
      Download Image
    </a>
  );
};

export default DownloadButton;
