// Copyright 2024, Athena Decision Systems
// @author Joel Milgram

import './DisplayDocument.css';
import React, { useEffect, useState } from 'react';
import { Document, Page, pdfjs } from 'react-pdf';
//import { Highlight, PdfHighlighter, Popup, AreaHighlight, setPdfWorker } from "react-pdf-highlighter";
import 'react-pdf/dist/Page/AnnotationLayer.css';
import 'react-pdf/dist/Page/TextLayer.css';
import DOMPurify from 'dompurify'
import ReactMarkdown from 'react-markdown';
import { useTranslation } from 'react-i18next';

pdfjs.GlobalWorkerOptions.workerSrc = `//cdnjs.cloudflare.com/ajax/libs/pdf.js/${pdfjs.version}/pdf.worker.js`;

const DisplayDocument = ({ name, type, content, dismiss }) => {
    const [numPages, setNumPages] = useState(null);
    const { t } = useTranslation();

    useEffect(() => {
        if (type === "application/pdf") {
            const binaryContent = atob(content);
            const len = binaryContent.length;
            const bytes = new Uint8Array(len);
            for (let i = 0; i < len; i++) {
                bytes[i] = binaryContent.charCodeAt(i);
            }
        }
    }, []); // eslint-disable-line

    function onDocumentLoadSuccess({ numPages }) {
        setNumPages(numPages);
    }
    console.log("DisplayDocument.js: name: " + name + ", type: " + type + ", content: " + content);
    /*<div className="display-annotation-content"><pre>{JSON.stringify(annotations, null, 2)}</pre></div>*/

    return (
        <>
            <div className="close-document" onClick={dismiss} title={t("commons.alt.clickToDismiss")}>X</div>
            <div className="display-document">
                <div className="display-document-header" onClick={dismiss} title={t("commons.alt.clickToDismiss")}>
                    <div className="display-document-name">{name}</div>
                </div>
                {(type === "text/plain") &&
                    <div className="display-document-content">
                        <pre>{content}</pre>
                    </div>}
                {(type === "text/markdown") &&
                    <div className="display-document-content">
                        <ReactMarkdown className="markdown-adjust-format">{content}</ReactMarkdown>
                    </div>}
                {(type === "text/html") &&
                    <div
                        id="editor"
                        className="display-document-content"
                        dangerouslySetInnerHTML={{ __html: DOMPurify.sanitize(content) }} />
                }
                {(type === 'application/pdf') && (
                    <div className="display-pdf-file">
                        <Document file={"data:application/pdf;base64," + content} onLoadSuccess={onDocumentLoadSuccess}>
                            {Array.from(new Array(numPages), (el, index) => (
                                <Page
                                    key={`page_${index + 1}`}
                                    pageNumber={index + 1}
                                    renderMode="canvas"
                                    renderAnnotationLayer={true}
                                    style={{ margin: 0, display: 'block', padding: 0, height: 'auto', width: 'auto' }}
                                />
                            ))}
                        </Document>
                    </div>
                )}
            </div>
        </>
    );
};

export default DisplayDocument;
