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


    const onClickHandler = (LLM: string[]): void => {
        LLMSelection(LLM[0]);

    
    };

    useEffect(() => {
        setShowDropDown(showDropDown);
    }, [showDropDown]);

    return (
        <>
        <ul className={showDropDown ? 'dropdown' : 'dropdown active '}>
            {LLMs.map(
            (LLM: string[], index: number): JSX.Element => {
                return (
                <a href={LLM[1]} key={index} target="_blank">
                    <li className='px-1 py-1 break-words text-center'
                    key={index}
                    onClick={(): void => {
                    onClickHandler(LLM);}}>
                        {LLM[0]}
                    </li>
                </a>
                );
            }
            )}
        </ul>
        </>
    );
};

export default DropDown;
