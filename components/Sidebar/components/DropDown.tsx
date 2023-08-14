import React, { useEffect, useState } from 'react';
import { useRouter } from 'next/router'

type DropDownProps = {
    LLMs: string[][];
    showDropDown: boolean;
    toggleDropDown: Function;
    LLMSelection: Function;
};

const DropDown: React.FC<DropDownProps> = ({
    LLMs,
    LLMSelection,
    }: DropDownProps): JSX.Element => {
    const [showDropDown, setShowDropDown] = useState<boolean>(false);

    const [goToURL, setGoToURL] = useState<boolean>(false);
    const [curLLM, setCurLLM] = useState<string>("");
    const router = useRouter()
    /**
     * Handle passing the LLM name
     * back to the parent component
     *
     * @param LLM  The selected LLM
     */
    const onClickHandler = (LLM: string[]): void => {
        LLMSelection(LLM[0]);
        console.log(LLM[1]);
        // handleRedirect(LLM[1]);
    };

    useEffect(() => {
        setShowDropDown(showDropDown);
    }, [showDropDown]);

    if (goToURL) {
        // window.location.replace(curLLM);
        router.push(curLLM);
    }

    return (
        <>
        <div className={showDropDown ? 'dropdown' : 'dropdown active'}>
            {LLMs.map(
            (LLM: string[], index: number): JSX.Element => {
                return (
                <a className='p-2'
                    key={index}
                    onClick={(): void => {
                    onClickHandler(LLM);
                    // setGoToURL(true);
                    setCurLLM(LLM[1]);
                    }}
                    href={LLM[1]}
                    target="_blank"
                >
                    {LLM[0]}
                </a>
                );
            }
            )}
        </div>
        </>
    );
};

export default DropDown;
