export const UPLOAD_URL = "http://127.0.0.1:8000/user/upload";
export const GET_PHOTOS_URL = "http://127.0.0.1:8000/user/getPhotos";

export const uploadImage = async (file, event) => {
  const form = new FormData();
  form.append("file", file);
  form.append("event", event);

  const res = await fetch(UPLOAD_URL, {
    method: "POST",
    body: form,
  });

  if (!res.ok) throw new Error("Upload failed");
  return res.json();
};

export const getPhotos = async (event, filename) => {
  const form = new FormData();
  form.append("event", event);
  form.append("filename", filename);

  const res = await fetch(GET_PHOTOS_URL, {
    method: "POST",
    body: form,
  });

  if (!res.ok) throw new Error("Matching failed");
  return res.json();
};