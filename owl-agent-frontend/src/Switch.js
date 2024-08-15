// Copyright 2024, Athena Decision Systems
// @author Joel Milgram

import React from "react";
import "./Switch.css";
import { useTranslation } from 'react-i18next';

const SWITCH_WIDTH_PX = 50;
const HANDLE_DIAMETER_PX = 20;
const SWITCH_OFFSET_PX = 3;

const Switch = ({ value, onClick, justifyContent, disabled }) => {
    const { t } = useTranslation();

    return (
        <div className={"switch-container" + (justifyContent === "flex-start" ? " switch-flex-start" : "")}>
            <div className={disabled ? "switch-yesno switch-disabled" : "switch-yesno"}>{value ? t("switch.lbl.yes") : t("switch.lbl.no")}</div>

            <div className={disabled ? "switch-box switch-disabled" : "switch-box"}
                style={{
                    width: SWITCH_WIDTH_PX,
                    height: HANDLE_DIAMETER_PX + 2 * SWITCH_OFFSET_PX,
                    borderRadius: HANDLE_DIAMETER_PX,
                    background: value ? "rgba(28, 30, 58, 1)" : "lightgrey",
                }}
                onClick={() => {
                    if (!disabled) {
                        onClick(!value);
                    }
                }}>
                <div className="switch-circle"
                    style={{
                        background: (value && !disabled) ? "white" : "grey",
                        height: HANDLE_DIAMETER_PX,
                        width: HANDLE_DIAMETER_PX,
                        top: SWITCH_OFFSET_PX,
                        left: value
                            ? SWITCH_WIDTH_PX - HANDLE_DIAMETER_PX - SWITCH_OFFSET_PX
                            : SWITCH_OFFSET_PX,
                    }}></div>
                <input className="switch-display-none"
                    type="checkbox"
                    value={value}
                    onChange={(e) => { onClick(e.target.value); }} />
            </div>
        </div >
    );
};
export default Switch;