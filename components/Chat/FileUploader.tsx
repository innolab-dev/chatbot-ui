// import { IconFileUpload } from '@tabler/icons-react';
// import { FC } from 'react';

// import { useTranslation } from 'next-i18next';

// import { SupportedExportFormats } from '@/types/export';

// interface Props {
//     onImport: (data: SupportedExportFormats) => void;
// }

// export const FileUploader: FC<Props> = ({ onImport }) => {
//     const { t } = useTranslation('sidebar');

//     const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
//         if (!event.target.files?.length) return;

//         const file = event.target.files[0];
//         const reader = new FileReader();
//         reader.onload = (event) => {
//             const json = JSON.parse(event.target?.result as string);
//             onImport(json);
//         };
//         reader.readAsText(file);
//     };

//     return (
//         <>
//         <input
//             id="file-upload"
//             type="file"
//             className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
//             onChange={handleFileChange}
//         />
//         <button
//             className="absolute left-8 top-1.5 rounded-sm p-1 text-neutral-800 opacity-60 hover:bg-neutral-200 hover:text-neutral-900 dark:bg-opacity-50 dark:text-neutral-100 d ark:hover:text-neutral-200"
//             onClick={() => {
//             const fileUpload = document.querySelector(
//                 '#file-upload',
//             ) as HTMLInputElement;
//             if (fileUpload) {
//                 fileUpload.click();
//             }
//             }}
//         >
//             <IconFileUpload size={18} />
//         </button>
//         <span className="ml-2">{t('Upload data')}</span>
//         </>
//     );
// };

import { ChangeEvent, useState } from 'react';

function FileUploadSingle() {
    const [file, setFile] = useState<File>();

    const handleFileChange = (e: ChangeEvent<HTMLInputElement>) => {
    if (e.target.files) {
        setFile(e.target.files[0]);
    }
};

    const handleUploadClick = () => {
    if (!file) {
        return;
    }

    // 👇 Uploading the file using the fetch API to the server
    fetch('https://httpbin.org/post', {
        method: 'POST',
        body: file,
      // 👇 Set headers manually for single file upload
        headers: {
            'content-type': file.type,
            'content-length': `${file.size}`, // 👈 Headers need to be a string
        },
    })
    .then((res) => res.json())
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
