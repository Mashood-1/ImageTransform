// frontend/src/services/api.js

// --- Gray Sketch ---
export const uploadGraySketch = async (file) => {
  const formData = new FormData();
  formData.append("file", file);

  const response = await fetch("http://127.0.0.1:8000/gray-sketch/", {
    method: "POST",
    body: formData,
  });

  if (!response.ok) {
    throw new Error("Failed to process gray sketch");
  }

  const blob = await response.blob();
  return URL.createObjectURL(blob); // returns a preview URL
};

// --- Color Sketch ---
export const uploadColorSketch = async (file) => {
  const formData = new FormData();
  formData.append("file", file);

  const response = await fetch("http://127.0.0.1:8000/color-sketch/", {
    method: "POST",
    body: formData,
  });

  if (!response.ok) {
    throw new Error("Failed to process color sketch");
  }

  const blob = await response.blob();
  return URL.createObjectURL(blob); // returns a preview URL
};

// --- Sticker ---
export const uploadSticker = async (file) => {
  const formData = new FormData();
  formData.append("file", file);

  const response = await fetch("http://127.0.0.1:8000/sticker/", {
    method: "POST",
    body: formData,
  });

  if (!response.ok) {
    throw new Error("Failed to process Sticker");
  }

  const blob = await response.blob();
  return URL.createObjectURL(blob); // returns a preview URL
};

// --- Cartoon ---
export const uploadCartoon = async (file) => {
  const formData = new FormData();
  formData.append("file", file);

  const response = await fetch("http://127.0.0.1:8000/cartoon/", {
    method: "POST",
    body: formData,
  });

  if (!response.ok) {
    throw new Error("Failed to process Cartoon");
  }

  const blob = await response.blob();
  return URL.createObjectURL(blob); // returns a preview URL
};

// --- Neon Glow ---
export const uploadNeonGlow = async (file) => {
  const formData = new FormData();
  formData.append("file", file);

  const response = await fetch("http://127.0.0.1:8000/neon-glow/", {
    method: "POST",
    body: formData,
  });

  if (!response.ok) {
    throw new Error("Failed to process Neon Glow");
  }

  const blob = await response.blob();
  return URL.createObjectURL(blob); // returns a preview URL
};

// --- Comic Art ---
export const uploadComicArt = async (file) => {
  const formData = new FormData();
  formData.append("file", file);

  const response = await fetch("http://127.0.0.1:8000/comic-art/", {
    method: "POST",
    body: formData,
  });

  if (!response.ok) {
    throw new Error("Failed to process Comic Art");
  }

  const blob = await response.blob();
  return URL.createObjectURL(blob); // returns a preview URL
};

// --- Manga Effect ---
export const uploadManga = async (file) => {
  const formData = new FormData();
  formData.append("file", file);

  const response = await fetch("http://127.0.0.1:8000/manga/", {
    method: "POST",
    body: formData,
  });

  if (!response.ok) {
    throw new Error("Failed to process Manga Effect");
  }

  const blob = await response.blob();
  return URL.createObjectURL(blob); // returns a preview URL
};

// --- Pop Art ---
export const uploadPopArt = async (file) => {
  const formData = new FormData();
  formData.append("file", file);

  const response = await fetch("http://127.0.0.1:8000/pop-art/", {
    method: "POST",
    body: formData,
  });

  if (!response.ok) {
    throw new Error("Failed to process Pop Art");
  }

  const blob = await response.blob();
  return URL.createObjectURL(blob);
};

// --- Neural Style Transfer ---
export const uploadStyleTransfer = async (file, style) => {
  const formData = new FormData();
  formData.append("file", file);

  const response = await fetch(`http://127.0.0.1:8000/style-transfer/${style}/`, {
    method: "POST",
    body: formData,
  });

  if (!response.ok) {
    throw new Error("Failed to apply style transfer");
  }

  const blob = await response.blob();
  return URL.createObjectURL(blob);
};

// --- Retro / Pixel Art ---
export const uploadPixelArt = async (file, style) => {
  const formData = new FormData();
  formData.append("file", file);

  const response = await fetch(`http://127.0.0.1:8000/pixel-art/${style}/`, {
    method: "POST",
    body: formData,
  });

  if (!response.ok) {
    throw new Error(`Failed to apply pixel art style: ${style}`);
  }

  const blob = await response.blob();
  return URL.createObjectURL(blob); // returns a preview URL
};
