'use client';

import { Button, Column, Grid, SkeletonText, TextInput, ToastNotification } from '@carbon/react';

import React, { useEffect, useState } from 'react';
import { Octokit } from '@octokit/core';
import DocumentMap from './DocumentMap';
import { Search } from '@carbon/react/icons';
import { useEnv } from '../providers';
import { getEnv } from '../env';
import UploadDocument from './UploadDocument';

const octokitClient = new Octokit({});

function DocumentsPage() {
  let env = useEnv();

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState();
  const [query, setQuery] = useState('');
  const [empty, setEmpty] = useState(false);
  const [rows, setRows] = useState([]);

  useEffect(() => {
    if (!env.backendBaseAPI) {
      getEnv().then((e) => {
        env = e;
      })
    }
  }, []);

  const getDocuments = async () => {
    try {
      const res = await octokitClient.request(`GET ${env.backendBaseAPI}a/documents/${query}`);

      if (res.status === 200) {
        setRows(res.data);
      } else {
        setError('Error when querying documents (' + res.status + ')');
      }
    } catch (error) {
      setError('Error when querying documents:' + error.message);
      console.error('Error when querying documents:' + error.message);
    }
    setLoading(false);
  }

  const searchDocuments = () => {
    if (!query) {
      setEmpty(true);
      return;
    }

    setLoading(true);
    getDocuments();
  }

  return (
    <Grid>
      <Column lg={16} md={8} sm={4} className="landing-page__banner">
        <h1 className="landing-page__heading">Documents</h1>
      </Column>

      <Column lg={16} md={8} sm={4} className="upload-area">
        <UploadDocument backendBaseAPI={env.backendBaseAPI} setError={setError} />
      </Column>

      <Column lg={16} md={8} sm={4}>
        <div style={{ display: 'flex', alignItems: 'center', marginTop: '1rem' }} />
        <TextInput data-modal-primary-focus id="text-input-1"
          labelText="Query"
          placeholder="e.g. loan validation"
          invalid={empty}
          invalidText="This field cannot be empty"
          value={query}
          onChange={(e) => { setEmpty(!e.target.value); setQuery(e.target.value.trim()) }}
          onKeyDown={(e) => { if (e.key === 'Enter') searchDocuments(); }} />
        <Button renderIcon={Search} disabled={empty} iconDescription="Search" onClick={() => searchDocuments()}>Search</Button>
        <div style={{ display: 'flex', alignItems: 'center', marginTop: '1rem' }} />
      </Column>

      {loading && (
        <Column lg={3} md={2} sm={2}>
          <SkeletonText className="card" paragraph={true} lineCount={2} />
        </Column>
      )}

      {!loading && (<DocumentMap rows={rows} />)}

      <Column lg={16} md={8} sm={4} className="landing-page__banner">
        {error && (<ToastNotification role="alert" caption={error} timeout={3000} title="Error" subtitle="" />)}
      </Column>
    </Grid>
  );
}

export default DocumentsPage;
