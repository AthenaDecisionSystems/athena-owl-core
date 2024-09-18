import { Button, FileUploaderDropContainer, FileUploaderItem, InlineNotification } from "@carbon/react";
import { Add, Upload } from "@carbon/react/icons";
import React, { useState } from "react";
import { useTranslation } from 'react-i18next';

const UploadDocument = ({ backendBaseAPI, setError }) => {
    const [file, setFile] = useState();
    const [uploadStatus, setUploadStatus] = useState(null);

    const { t, i18n } = useTranslation();

    const updateFile = (event) => {
        const file0 = event.target.files[0];
        if (file0) {
            setFile(file0);
        };
    }

    const uploadFile = async () => {
        const formData = new FormData();
        formData.append('myFile', file);
        formData.append('name', file.name);
        formData.append('description', 'to be added');
        formData.append('type', 'text');
        formData.append('file_name', file.name);

        try {
            const response = await fetch(`${backendBaseAPI}a/documents/`, {
                method: 'POST',
                body: formData,
            });

            if (response.ok) {
                console.log('Upload successful');
                const responseBody = await response.json();
                console.log('Response Body:', responseBody);
                setUploadStatus({ kind: "success", text: file.name + ' uploaded' });
                setFile();
            } else {
                setUploadStatus({ kind: "error", text: file.name + ' NOT uploaded. ' + response.statusText });
                console.error('Upload failed', response.statusText);
            }
        } catch (error) {
            console.error('Error uploading document:', error);
            setError('Error uploading document:' + error.message);
        }
    }

    return (
        <div>
            <FileUploaderDropContainer name="fileUploader"
                labelText="Drag and drop a file here or click to upload"
                multiple={false}
                accept={['text/plain', 'text/html', 'text/markdown', 'application/pdf']}
                onAddFiles={updateFile} />
            {file && <FileUploaderItem name={file.name} status="edit"
                iconDescription="Delete file"
                onDelete={() => setFile()}
                errorBody="500kb max file size. Select a new file and try again."
                errorSubject="File size exceeds limit" invalid={false} />}
            {file && <Button kind="tertiary" renderIcon={Upload} iconDescription="Upload" onClick={() => uploadFile()}>Upload</Button>}
            {uploadStatus && (
                <InlineNotification
                    aria-label="closes notification"
                    kind={uploadStatus.kind}
                    onClose={() => setUploadStatus(null)}
                    onCloseButtonClick={() => setUploadStatus(null)}
                    statusIconDescription="notification"
                    subtitle={uploadStatus.text}
                    title="Upload file: "
                />)}
        </div>
    );
};

export default UploadDocument;