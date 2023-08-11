import React from "react" 


const Result = ({ status }: { status: string }) => {
    if (status === "success") {
        return <p className="flex justify-center align-center pt-3">
            ✅ <span className="text-black/50 dark:text-white/50 pl-1"> File uploaded successfully!</span></p>;
    } else if (status === "fail") {
        return <p className="flex justify-center align-center pt-3 text-black/50 dark:text-white/50">
            ❌ <span className="text-black/50 dark:text-white/50 pl-1"> File upload failed!</span></p>;
    } else if (status === "uploading") {
        return <p className="flex justify-center align-center pt-3 text-black/50 dark:text-white/50">
            ⏳ <span className="text-black/50 dark:text-white/50 pl-1"> Uploading selected file...</span></p>
    } else {
        return null;
    }
};

export default Result;