export function checkImage(imageSrc, good, bad) {
  const img = new Image();
  img.onload = good;
  img.onerror = bad;
  img.src = imageSrc;
}
