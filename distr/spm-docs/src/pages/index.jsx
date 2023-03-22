import React from "react";
import Link from "@docusaurus/Link";
import useDocusaurusContext from "@docusaurus/useDocusaurusContext";
import Layout from "@theme/Layout";
import HomepageFeatures from "@site/src/components/HomepageFeatures";
import Logo from "../../static/img/logo-dark.svg";

function HomepageHeader() {
  const { siteConfig } = useDocusaurusContext();
  return (
    <header className="bg-brand-primary-darkest">
      <div className="container mx-auto text-center py-24">
        <div className="flex w-full justify-center gap-3 items-center">
          <Logo className="h-12 w-12" />

          <h1 className="text-4xl font-bold text-white m-0">
            {siteConfig.title}
          </h1>
        </div>
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
