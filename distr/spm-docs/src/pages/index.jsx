import React from "react";
import Link from "@docusaurus/Link";
import useDocusaurusContext from "@docusaurus/useDocusaurusContext";
import Layout from "@theme/Layout";
import HomepageFeatures from "@site/src/components/HomepageFeatures";

function HomepageHeader() {
  const { siteConfig } = useDocusaurusContext();
  return (
    <header className="bg-brand-primary-darkest">
      <div className="container mx-auto text-center py-24">
        <h1 className="text-4xl font-bold text-white">{siteConfig.title}</h1>
        <p className="text-xl py-6 text-white">{siteConfig.tagline}</p>

        <div className="py-10">
          <Link
            className="bg-white rounded-md text-gray-500 px-4 py-2"
            to="/docs/getting-started/setup"
          >
            Get started with SPM in 5min ⏱️
          </Link>
        </div>
      </div>
    </header>
  );
}

export default function () {
  return (
    <Layout>
      <HomepageHeader />
      <main>
        <HomepageFeatures />
      </main>
    </Layout>
  );
}
