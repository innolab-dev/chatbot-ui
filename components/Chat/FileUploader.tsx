import { ChangeEvent, useState } from 'react';

function FileUploadSingle() {
    const [file, setFile] = useState<File>();

    const handleFileChange = (e: ChangeEvent<HTMLInputElement>) => {
        if (e.target.files) {
            setFile(e.target.files[0]);
        }
    };

    const handleUploadClick = async () => {
        if (!file) {
            return;
        }

        // 👇 Uploading the file using the fetch API to the server
        const formData = new FormData();
        formData.append('file', file);

        const data = {
            purpose: 'upload',
            files: formData,
        };

        await fetch('http://219.79.203.190:1111/file_uploader', {
            method: 'POST',
            body: JSON.stringify(data),
            headers: {  
                'Content-Type': 'application/json',
            },
        })
        .then((response) => response.json())
        .then((data) => console.log(data))
        .catch((err) => console.error(err));
    };

    return (
        <div>
        <input type="file" onChange={handleFileChange} />

        <div>{file && `${file.name} - ${file.type}`}</div>

        <button onClick={handleUploadClick}>Upload</button>
        </div>
    );
}

export default FileUploadSingle;
