// Copyright 2024, Athena Decision Systems
// @author Joel Milgram

import React from 'react';
import ReactDOM from 'react-dom/client'
import App from './App';

import { Provider } from 'react-redux';
import { configureStore } from '@reduxjs/toolkit';
import rootReducer from './reducer';

import i18n from 'i18next';
import { I18nextProvider } from 'react-i18next';
import './i18n';


const root = ReactDOM.createRoot(document.getElementById('root'));
const store = configureStore({
  reducer: rootReducer,
  devTools: true
})

root.render(
  <I18nextProvider i18n={i18n}>
    <Provider store={store}>
      <App />
    </Provider >
  </I18nextProvider>
);