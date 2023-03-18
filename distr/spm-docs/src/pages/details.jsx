import React, { useEffect, useMemo } from "react";
import Layout from "@theme/Layout";

export default function () {
  const packageName = useMemo(
    () => new URLSearchParams(location.search).get("package-name"),
    [location]
  );

  useEffect(() => {
    if (!packageName) {
      console.log(packageName);
      location.href = "/search";
    }
  }, [packageName]);

  return (
    <Layout>
      <div className="w-full flex justify-center items-center mt-5 p-3"></div>
    </Layout>
  );
}
