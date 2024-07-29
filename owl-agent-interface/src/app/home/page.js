'use client';

import {
  Breadcrumb,
  BreadcrumbItem,
  Button,
  Tabs,
  Tab,
  TabList,
  TabPanels,
  TabPanel,
  Grid,
  Column,
} from '@carbon/react';
import { Launch } from '@carbon/pictograms-react';
import Image from 'next/image';

export default function LandingPage() {
  return (
    <Grid className="landing-page" fullWidth>
      <Column lg={16} md={8} sm={4} className="landing-page__banner">
        <Breadcrumb noTrailingSlash aria-label="Page navigation">
          <BreadcrumbItem>
            <a href="/">Manage intelligent decision with Hybrid AI</a>
          </BreadcrumbItem>
        </Breadcrumb>
        <h1 className="landing-page__heading">Owl Agent</h1>
      </Column>
      <Column lg={16} md={8} sm={4} className="landing-page__r2">
        <Tabs defaultSelectedIndex={0}>
          <TabList className="tabs-group" aria-label="Page navigation">
            <Tab>About</Tab>
            <Tab>Learn more</Tab>
            <Tab>Contribute</Tab>
          </TabList>
          <TabPanels>
            <TabPanel>
              <Grid className="tabs-group-content">
                <Column
                  md={4}
                  lg={7}
                  sm={4}
                  className="landing-page__tab-content"
                >
                  <h3 className="landing-page__subheading">
                    What is Owl Agent?
                  </h3>
                  <p className="landing-page__p">
                    Owl Agent is a conversational agent based on generative AI
                    and Business Rules that helps you make repeatable,
                    explainable, reliable and accurate decisions.
                  </p>
                </Column>
                <Column md={4} lg={{ span: 8, offset: 8 }} sm={4}>
                  <Image
                    className="landing-page__illo"
                    src="/athena-logo.png"
                    alt="Owl illustration"
                    width={420}
                    height={500}
                  />
                </Column>
              </Grid>
            </TabPanel>
            <TabPanel>
              <Grid className="tabs-group-content">
                <Column
                  lg={16}
                  md={8}
                  sm={4}
                  className="landing-page__tab-content"
                >
                  <p className="landing-page__p">
                    Owl Agent was initially designed by{' '}
                    <a href="https://athenadecisions.com" target="_blank">
                      Athena Decision Systems{' '}
                      <Launch width={16} height={16} viewBox="0 0 32 32" />
                    </a>
                    .
                  </p>
                </Column>
              </Grid>
            </TabPanel>
            <TabPanel>
              <Grid className="tabs-group-content">
                <Column
                  lg={16}
                  md={8}
                  sm={4}
                  className="landing-page__tab-content"
                >
                  <p className="landing-page__p">
                    Contribute by building new assistants based on generative AI
                    and Business Rules. Visit{' '}
                    <a
                      href="https://github.com/AthenaDecisionSystems/athena-owl-demos"
                      target="_blank"
                    >
                      Owl Demos Github{' '}
                      <Launch width={16} height={16} viewBox="0 0 32 32" />
                    </a>
                    .
                  </p>
                </Column>
              </Grid>
            </TabPanel>
          </TabPanels>
        </Tabs>
      </Column>
      <Column lg={16} md={8} sm={4} className="landing-page__r3"></Column>
    </Grid>
  );
}
