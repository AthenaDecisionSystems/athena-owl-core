'use client';

import { Button, Column, Grid, NumberInput, SkeletonText, TextInput, ToastNotification } from '@carbon/react';

import React, { useEffect, useRef, useState } from 'react';
import { Octokit } from '@octokit/core';
import DocumentMap from './DocumentMap';
import { Search } from '@carbon/react/icons';
import { context } from '../providers';
import { getEnv } from '../env';
import UploadDocument from './UploadDocument';

const octokitClient = new Octokit({});

function DocumentsPage() {
  let env = context()?.env;

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState();
  const [query, setQuery] = useState('');
  const [topK, setTopK] = useState(5);
  const [empty, setEmpty] = useState(true);
  const [rows, setRows] = useState([]);

  const controlRef = useRef(null);

  useEffect(() => {
    if (!env.backendBaseAPI) {
      getEnv().then((e) => {
        env = e;
      })
    }
  }, []);

  const getDocuments = async () => {
    const collectionName = env.collectionName || "owl_default";
    console.log('Querying documents:', `GET ${env.backendBaseAPI}a/documents/${collectionName}/${encodeURIComponent(query)}/${topK}`);
    try {
      const res = await octokitClient.request(`GET ${env.backendBaseAPI}a/documents/${collectionName}/${query}/${topK}`);

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
        <UploadDocument env={env} setError={setError} />
        <hr style={{ margin: "3rem 0rem" }} />
      </Column>

      <Column lg={13} md={6} sm={2}>
        <TextInput data-modal-primary-focus id="text-input-1"
          labelText="Query"
          placeholder="e.g. loan validation"
          invalid={empty}
          invalidText="This field cannot be empty"
          value={query}
          onChange={(e) => { setEmpty(!e.target.value.trim()); setQuery(e.target.value) }}
          onKeyDown={(e) => { if (e.key === 'Enter') searchDocuments(); }} />
      </Column>
      <Column lg={3} md={2} sm={2}>
        <NumberInput id="number-input-1" ref={controlRef}
          label="Top K"
          value={topK}
          min={1}
          max={20}
          invalid={topK < 1 || topK > 20}
          invalidText="Value must be between 1 and 20"
          onChange={() => setTopK(controlRef.current.value)} />
      </Column>
      <Column lg={16} md={8} sm={4}>
        <div style={{ display: 'flex', alignItems: 'center', marginTop: '1rem' }} />
        <Button renderIcon={Search} disabled={empty || topK < 1 || topK > 20} iconDescription="Search" onClick={() => searchDocuments()}>Search</Button>
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
