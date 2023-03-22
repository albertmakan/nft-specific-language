import React, { useEffect, useMemo, useState } from "react";
import Layout from "@theme/Layout";
import BrowserOnly from "@docusaurus/BrowserOnly";

function DetailsPage() {
  const packageName = useMemo(
    () => new URLSearchParams(location.search).get("package-name"),
    [location]
  );

  const [packageVersions, setPackageVersions] = useState([]);

  useEffect(() => {
    if (!packageName) {
      location.href = "/search";
    } else {
      getPackageVersions(packageName).then(setPackageVersions);
    }
  }, [packageName]);

  return (
    <Layout>
      <div className="w-full flex flex-col justify-center items-center mt-5 p-3">
        {packageVersions.map((v) => (
          <div className="flex gap-3">
            <a href={`https://gw.spm.bjelicaluka.com/ipfs/${v.cid}`} target="_blank">{v.cid}</a>
            <span>{v.author}</span>
            <span>{v.name}</span>
            <span>{v.version}</span>
          </div>
        ))}
      </div>
    </Layout>
  );
}

async function getPackageVersions(name) {
  const response = await fetch(`/api/spm/package/${name}`);

  if (response.ok) {
    return response.json();
  }
  return [];
}

export default function () {
  return (
    <BrowserOnly>
      {() => {
        return <DetailsPage />;
      }}
    </BrowserOnly>
  );
}
