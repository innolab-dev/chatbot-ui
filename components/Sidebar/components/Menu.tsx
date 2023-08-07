import React, { useState } from "react";
import DropDown from "./DropDown";
import { IconMenu2 } from '@tabler/icons-react';

const Menu: React.FC = (): JSX.Element => {
    const [showDropDown, setShowDropDown] = useState<boolean>(false);
    const [selectLLMs, setSelectLLMs] = useState<string>("");
    const LLMs = () => {
        return ["Respond with database", "Email Automation", "Image Generation", "Summarize a website"];
    };

    /**
     * Toggle the drop down menu
     */
    const toggleDropDown = () => {
        setShowDropDown(!showDropDown);
    };

    /**
     * Hide the drop down menu if click occurs
     * outside of the drop-down element.
     *
     * @param event  The mouse event
     */
    const dismissHandler = (event: React.FocusEvent<HTMLButtonElement>): void => {
        if (event.currentTarget === event.target) {
        setShowDropDown(false);
        }
    };

    /**
     * Callback function to consume the
     * city name from the child component
     *
     * @param city  The selected city
     */
    const LLMSelection = (city: string): void => {
        setSelectLLMs(city);
    };

    return (
        <div className="w-full flex-1 rounded-md border border-neutral-600 bg-[#202123] px-4 py-3 pr-10 text-[14px] leading-4 text-white flex flex-grow-2 flex-shrink-2">
            <IconMenu2 size={16} className="ml-0"/>
            <div>                
                <div className="announcement">
                    <div>
                    {selectLLMs
                        ? ""
                        : "Select a langchain"}
                    </div>
                </div>
                <button
                    className={showDropDown ? "active" : undefined}
                    onClick={(): void => toggleDropDown()}
                    onBlur={(e: React.FocusEvent<HTMLButtonElement>): void =>
                    dismissHandler(e)
                    }
                >
                    <div>{selectLLMs ? "Selected: " + selectLLMs : "Select one"} </div>
                    {showDropDown && <hr></hr>}
                    {showDropDown && (
                    <DropDown
                        LLMs={LLMs()}
                        showDropDown={false}
                        toggleDropDown={(): void => toggleDropDown()}
                        LLMSelection={LLMSelection}
                    />
                    )}
                </button>
            </div>
        </div>
    );
};

export default Menu;
