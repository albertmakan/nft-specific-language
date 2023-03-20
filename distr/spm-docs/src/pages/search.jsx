import React, { useCallback, useEffect, useState } from "react";
import Layout from "@theme/Layout";
import Link from "@docusaurus/Link";
import { debounce } from "../utils/debounce";
import { checkImage } from "../utils/img";

export default function () {
  const [term, setTerm] = useState();
  const [results, setResults] = useState([]);

  const searchPackagesDebounced = useCallback(
    debounce((term) => {
      searchPackages(term).then(setResults);
    }, 600),
    []
  );

  useEffect(() => {
    if (term) {
      searchPackagesDebounced(term);
    }
  }, [term]);

  return (
    <Layout>
      <div className="w-full flex justify-center items-center mt-5 p-3">
        <input
          type="text"
          className="max-w-xl w-full rounded-md border h-10 pl-5 focus:ring-0 focus:ring-offset-0 text-gray-500 dark:text-gray-100"
          placeholder="Search packages..."
          onChange={(e) => {
            setTerm(e.target.value);
          }}
        />
      </div>
      <div className="flex flex-col items-center gap-2 mt-2">
        {results.map((pkg) => (
          <div
            key={pkg.cid}
            className="w-full flex flex-col gap-3 px-2 pb-3 max-w-xl border-0 border-b border-solid border-gray-500/70 dark:border-gray-100"
          >
            <div className="flex gap-5">
              <div className="flex items-center gap-3">
                <Link to={`/details?package-name=${pkg.name}`}>{pkg.name}</Link>
                <span className="text-xs pt-1">v{pkg.version}</span>
              </div>
              {term === pkg.name && (
                <div className="text-xs h-6 py-1 px-2 rounded-md bg-brand-primary-lightest/40">
                  exact match
                </div>
              )}
            </div>
            {pkg.description && (
              <div className="flex text-sm text-gray-500 dark:text-gray-100 pl-1">
                {pkg.description}
              </div>
            )}
            <div className="flex items-center gap-2">
              <AuthorImage url={`https://github.com/${pkg.author}.png`} />
              <span className="text-sm">{pkg.author}</span>
              <span className="text-gray-500 dark:text-gray-100 text-xs pt-1">
                package expires at {pkg.expirationDate}
              </span>
            </div>
          </div>
        ))}
      </div>
    </Layout>
  );
}

function AuthorImage(props) {
  const [exists, setExists] = useState(false);

  useEffect(() => {
    checkImage(
      props.url,
      () => {
        setExists(true);
      },
      () => {
        setExists(false);
      }
    );
  }, []);
  return exists ? (
    <img src={props.url} className="h-8 w-8 rounded-md" alt="author" />
  ) : (
    <div></div>
  );
}

async function searchPackages(term) {
  const response = await fetch(`/api/spm/search/${term}`);

  if (response.ok) {
    return response.json();
  }
  return [];
}
