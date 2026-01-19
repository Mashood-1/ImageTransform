import React, { useState } from "react";
import ChooseFile from "./ChooseFile";
import GraySketch from "../Filters/GraySketch/GraySketch";
import ColorSketch from "../Filters/ColorSketch/ColorSketch";
import Sticker from "../Filters/Sticker/Sticker";
import DownloadButton from "../DownloadButton/DownloadButton";
import "./Upload.css";
import Cartoon from "../Filters/Cartoon/Cartoon";
import NeonGlow from "../Filters/NeonGlow/NeonGlow";
import ComicArt from "../Filters/ComicArt/ComicArt";
import Manga from "../Filters/Manga/Manga";
import PopArt from "../Filters/PopArt/PopArt";
import StyleTransfer from "../Filters/StyleTransfer/StyleTransfer";
import RetroPixelArt from "../Filters/PixelArt/RetroPixelArt";

const Upload = () => {
  const [file, setFile] = useState(null);
  const [originalPreview, setOriginalPreview] = useState(null);
  const [transformedResult, setTransformedResult] = useState(null); // single result

  const handleFileSelect = (selectedFile) => {
    setFile(selectedFile);
    setOriginalPreview(URL.createObjectURL(selectedFile));
    setTransformedResult(null); // reset any previous result
    window.scrollTo({ top: 0, behavior: "smooth" });
  };

  return (
    <div className="upload-container">
      <ChooseFile onFileSelect={handleFileSelect} />

      {originalPreview && (
        <>
          <div className="preview-section">
            <h3>Original Image</h3>
            <img src={originalPreview} alt="Original Preview" className="preview-image" />
          </div>

          {/* Horizontal Filter Buttons */}
          <div className="filter-buttons-container">
            <GraySketch file={file} onResult={setTransformedResult} />
            <ColorSketch file={file} onResult={setTransformedResult} />
            <Sticker file={file} onResult={setTransformedResult} />
            <Cartoon file={file} onResult={setTransformedResult} />
            <NeonGlow file={file} onResult={setTransformedResult} />
            <ComicArt file={file} onResult={setTransformedResult} />
            <Manga file={file} onResult={setTransformedResult} />
            <PopArt file={file} onResult={setTransformedResult} />
            <StyleTransfer file={file} onResult={setTransformedResult} />
            <RetroPixelArt file={file} onResult={setTransformedResult} />
            {/* Future filters like Cartoon, Sticker can be added here */}
          </div>

          {/* Single Result Display */}
          {transformedResult && (
            <div className="result-section">
              <h3>Transformed Result</h3>
              <img src={transformedResult} alt="Transformed Result" className="preview-image" />
              <DownloadButton url={transformedResult} filename="transformed.png" />
            </div>
          )}
        </>
      )}
    </div>
  );
};

export default Upload;
