'use client';

import { createContext, useContext, useEffect, useState } from "react";
import { Content, InlineLoading, Theme } from '@carbon/react';
import OwlAgentHeader from './home/OwlAgentHeader';
import { getEnv } from "./env";
import i18n from 'i18next';
import { I18nextProvider } from 'react-i18next';
import './i18n';
import EventEmitter from "events";

export const EnvContext = createContext({});

export function Providers({ children }) {
  const [env, setEnv] = useState({});
  const [role, setRole] = useState("user"); // This is the current user role (admin, user, etc.)
  const [loading, setLoading] = useState(true);

  EventEmitter.defaultMaxListeners = 20;

  useEffect(() => {
    const initEnvironmentVariables = async () => {
      let environnementVariables = await getEnv();
      setEnv(environnementVariables);
    }

    try {
      initEnvironmentVariables();
    } finally {
      setLoading(false);
    }
  }, []);

  return (
    <div>
      <EnvContext.Provider value={{ env, role, setRole }}>
        {loading && (<InlineLoading status="active" iconDescription="Please wait..." description="Veuillez patienter / Please wait..." />)}

        {!loading && (env.backendBaseAPI === null || env.backendBaseAPI === undefined || env.backendBaseAPI === "") && (<div>
          Erreur de configuration serveur: les variables d'environnement ne sont pas définies
          <br></br>
          Server configuration error: environment variables are not defined</div>)}
        {!loading && env.backendBaseAPI && (
          <I18nextProvider i18n={i18n}>
            <Theme theme="g100">
              <OwlAgentHeader />
            </Theme>
            <Theme theme="g10">
              <Content>
                {children}
              </Content>
            </Theme>
          </I18nextProvider>
        )}
      </EnvContext.Provider>
    </div>
  );
}

export const context = () => {
  return useContext(EnvContext);
};
