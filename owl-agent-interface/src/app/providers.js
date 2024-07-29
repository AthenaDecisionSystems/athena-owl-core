'use client';

import { createContext, useContext, useEffect, useState } from "react";
import { Content, Theme } from '@carbon/react';
import OwlAgentHeader from './home/OwlAgentHeader';
import { getEnv } from "./env";

export const EnvContext = createContext({});

export function Providers({ children }) {
  const [env, setEnv] = useState({});
  useEffect(() => {
    getEnv().then(setEnv);
  }, []);

  return (
    <div>
      <Theme theme="g100">
        <EnvContext.Provider value={env}>
          <OwlAgentHeader />
        </EnvContext.Provider>
      </Theme>
      <Theme theme="g10">
        <Content>
          <EnvContext.Provider value={env}>
            {children}
          </EnvContext.Provider>
        </Content>
      </Theme>
    </div>
  );
}

export const useEnv = () => {
  return useContext(EnvContext);
};