// Copyright 2024, Athena Decision Systems
// @author Joel Milgram

import React, { useRef, useState } from 'react';
import './Attachments.css'
import attach from './assets/attach.png';
import { useDispatch, useSelector } from 'react-redux';
import { setError } from './reducer/error.action';
import DisplayDocument from './DisplayDocument';
import { useTranslation } from 'react-i18next';

const Attachments = ({ informUser }) => {
    const serverUrl = useSelector((state) => state.serverUrlReducer.serverUrl)
    const [attachments, setAttachments] = useState([]);
    const dispatch = useDispatch()

    const hiddenFileInput = useRef(null);
    const [files, setFiles] = useState([]);
    const [selectedFile, setSelectedFile] = useState(null);
    const [fileContents, setFileContents] = useState({});

    const { t } = useTranslation();

    const handleClick = () => {
        hiddenFileInput.current.click();
    };

    function arrayBufferToBase64(buffer) {
        let binary = '';
        let bytes = new Uint8Array(buffer);
        let len = bytes.byteLength;
        for (let i = 0; i < len; i++) {
            binary += String.fromCharCode(bytes[i]);
        }
        return window.btoa(binary);
    }

    const handleFileChange = async (event) => {
        const newFiles = Array.from(event.target.files);
        setFiles([...files, ...newFiles]);
        let atts = attachments;
        informUser("...");

        const promises = newFiles.map((file) => {
            const formData = new FormData();
            //formData.append("filename", file.name); // doesn't work for now because of a bug at OpenAI level
            formData.append("myFile", file, file.name);

            // Upload to backend
            dispatch(setError(null));

            const fileNameWithoutExtension = file.name.split('.').slice(0, -1).join('.');
            const fileNameExstension = file.name.split('.').pop();
            fetch(serverUrl + "a/documents?name=" + fileNameWithoutExtension + "&type=" + fileNameExstension + "&file_name=" + file.name, { method: 'POST', body: formData })
                .then(response => response.json())
                .then(data => {
                    console.log("Upload document: " + file.name + ": ");
                    console.log(data);

                    if (data.status === 201) {
                        informUser(t("attachments.msg.documentUploaded", { fileName: file.name }))
                        atts.push({ filename: file.name, type: file.type, visible: true });
                    } else {
                        informUser(t("attachments.err.errorUploadingDocument", { fileName: file.name, message: data.message, error: data.error }))
                    }
                })
                .catch(error => {
                    console.error('Error:', error)
                    dispatch(setError(error.message))
                });

            // Read file content and store it in fileContents
            return new Promise((resolve, reject) => {
                const reader = new FileReader();

                reader.onload = function (e) {
                    resolve({ filename: file.name, type: file.type, content: e.target.result });
                };

                reader.onerror = function (e) {
                    reject(new Error(t("attachments.err.errorReadingDocument", { error: e.toString() })));
                };

                if (file.type === 'application/pdf') {
                    reader.readAsArrayBuffer(file);
                } else {
                    reader.readAsText(file);
                }
            });
        });
        const results = await Promise.all(promises);

        const newFileContents = fileContents;
        results.forEach(({ filename, type, content }) => {
            // PDF files are converted to base64 to avoid error "Cannot perform Construct on a detached ArrayBuffer"
            newFileContents[filename] = (type === "application/pdf") ? arrayBufferToBase64(content) : content;
        });
        setFileContents(newFileContents);
        setAttachments(atts);
        console.log("Attachments: ", atts);
    }

    const handleFileClick = (file) => {
        if (file.visible) {
            setSelectedFile(file);
        }
    }

    const closeDocument = () => {
        setSelectedFile(null);
    };

    return (
        <div className="attachments">
            <div className="button-attach">
                <img className="attach" src={attach} alt={t("attachments.alt.loadDocuments")} title={t("attachments.alt.loadDocuments")} onClick={handleClick} />
                <input ref={hiddenFileInput} multiple type="file" accept=".pdf,.txt,.html,.md" onChange={handleFileChange} />
            </div>
            {Array.from(attachments).map((f, index) => <div key={index} className={f.visible ? "file-attached" : "file-attached-not-visible"} title={f.visible ? t("attachments.alt.clickToDisplayFile") : t("attachments.alt.fileUnavailable")} onClick={() => handleFileClick(f)}>{f.filename}</div>)}
            {selectedFile && (<DisplayDocument name={selectedFile.filename} type={selectedFile.type} content={fileContents[selectedFile.filename]} dismiss={closeDocument} />)}
        </div >
    );
};

export default Attachments;