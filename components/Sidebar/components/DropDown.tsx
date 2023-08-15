import React, { useEffect, useState } from 'react';
import Link from "next/link";
// import { useRouter } from 'next/router'

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

    /**
     * Handle passing the LLM name
     * back to the parent component
     *
     * @param LLM  The selected LLM
     */
    const onClickHandler = (LLM: string[]): void => {
        LLMSelection(LLM[0]);
        console.log("clicked");
        // setGoToURL(true);
        // setCurLLM(LLM[1]);

    
    };

    useEffect(() => {
        setShowDropDown(showDropDown);
    }, [showDropDown]);

    return (
        <>
        <div className={showDropDown ? 'dropdown' : 'dropdown active'}>
            {LLMs.map(
            (LLM: string[], index: number): JSX.Element => {
                return (
                <a href={LLM[1]} key={index} target="_blank">

                    {/* <p className='p-2'
                        
                        
                        }}
                    >
                        {LLM[0]}
                    </p> */}
                    <p className='p-1 break-words'
                        key={index}
                        onClick={(): void => {
                        onClickHandler(LLM);}}>{LLM[0]}</p>
                </a>
                );
            }
            )}
        </div>
        </>
    );
};

export default DropDown;
