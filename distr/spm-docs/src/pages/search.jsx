import React, { useEffect, useState } from "react";
import Layout from "@theme/Layout";

export default function () {
  const [term, setTerm] = useState();

  console.log(term);
  return (
    <Layout>
      <div className="w-full flex justify-center items-center mt-5 p-3">
        <input
          type="text"
          className="max-w-xl w-full rounded-md border h-10 pl-5 focus:ring-0 focus:ring-offset-0 text-gray-500"
          placeholder="Search packages..."
          onChange={(e) => {
            setTerm(e.target.value);
          }}
        />
      </div>
    </Layout>
  );
}
