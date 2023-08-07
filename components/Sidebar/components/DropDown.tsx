import React, { useEffect, useState } from 'react';

type DropDownProps = {
    LLMs: string[];
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
    const onClickHandler = (LLM: string): void => {
        LLMSelection(LLM);
    };

    useEffect(() => {
        setShowDropDown(showDropDown);
    }, [showDropDown]);

    return (
        <>
        <div className={showDropDown ? 'dropdown' : 'dropdown active'}>
            {LLMs.map(
            (LLM: string, index: number): JSX.Element => {
                return (
                <p className='p-2'
                    key={index}
                    onClick={(): void => {
                    onClickHandler(LLM);
                    }}
                >
                    {LLM}
                </p>
                );
            }
            )}
        </div>
        </>
    );
};

export default DropDown;
