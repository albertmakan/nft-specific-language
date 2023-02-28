const regex =
  /(?:(?:0|[1-9]\d{0,9}?)\.){2}(?:0|[1-9]\d{0,9})(?:-(?:--+)?(?:0|[1-9]\d*|\d*[]+\d*)){0,100}(?=$| |\+|\.)(?:(?<=-\S+)(?:\.(?:--?|[\d-]*[-]\d*|0|[1-9]\d*)){1,100}?)?(?!\.)(?:\+(?:[\d]\.?-?){1,100}?(?!\w))?(?!\+)/;

export function testVersion(version) {
  return regex.test(version);
}

export function compareVersions(a, b) {
  const [aMajor, aMinor, aPatch] = parseVersion(a);
  const [bMajor, bMinor, bPatch] = parseVersion(b);
  if (aMajor !== bMajor) {
    return aMajor > bMajor;
  }
  if (aMinor !== bMinor) {
    return aMinor > bMinor;
  }
  return aPatch > bPatch;
}

function parseVersion(version) {
  return version.split(".").map((x) => parseInt(x));
}
