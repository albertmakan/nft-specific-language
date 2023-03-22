import React from "react";
import clsx from "clsx";
import styles from "./styles.module.css";

const FeatureList = [
  {
    title: "Easy to Use",
    Svg: require("@site/static/img/easy.svg").default,
    description: (
      <>
        SMP was designed from the ground up to be easily installed and used to
        get your Solidity project up and running quickly.
      </>
    ),
  },
  {
    title: "Powered by People",
    Svg: require("@site/static/img/group.svg").default,
    description: (
      <>
        SPM is not just a tool, it is a community of people. Find and use
        packages created by others. Contribute to the community by creating new
        packages.
      </>
    ),
  },
  {
    title: "Secure",
    Svg: require("@site/static/img/secure-shield.svg").default,
    description: (
      <>
        The benefit of distributing Solidity code using SPM is that more people
        will get to see it, read it, and find potential security issues. The
        bigger the community is, the more developers will be able to rely on
        other packages.
      </>
    ),
  },
];

function Feature({ Svg, title, description }) {
  return (
    <div className={clsx("col col--4")}>
      <div className="text--center">
        <Svg className={styles.featureSvg} role="img" />
      </div>
      <div className="text--center padding-horiz--md">
        <h3>{title}</h3>
        <p>{description}</p>
      </div>
    </div>
  );
}

export default function HomepageFeatures() {
  return (
    <section className={styles.features}>
      <div className="container">
        <div className="row">
          {FeatureList.map((props, idx) => (
            <Feature key={idx} {...props} />
          ))}
        </div>
      </div>
    </section>
  );
}
