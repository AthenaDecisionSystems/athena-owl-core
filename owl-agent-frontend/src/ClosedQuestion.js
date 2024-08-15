import './ClosedQuestion.css';

import React, { forwardRef, useEffect, useImperativeHandle, useState } from 'react';
import ReactMarkdown from 'react-markdown';
import { useTranslation } from 'react-i18next';
import Switch from './Switch'

const ClosedQuestion = forwardRef(({ index, question, disabled }, ref) => {
    const [keyName, setKeyName] = useState('');
    const [labels, setLabels] = useState([]);
    const [dataType, setDataType] = useState('');
    const [min, setMin] = useState(null);
    const [max, setMax] = useState(null);
    const [step, setStep] = useState(1);
    const [regex, setRegex] = useState('');
    const [minLength, setMinLength] = useState(1);
    const [maxLength, setMaxLength] = useState(null);
    const [enumeration, setEnumeration] = useState(null);

    const [inputValue, setInputValue] = useState();
    const [error, setError] = useState('');

    const { t, i18n } = useTranslation();

    useEffect(() => {
        setKeyName(question.key_name);
        setLabels(question.labels);
        setDataType(question.data_type);
        if (question.restrictions) {
            setEnumeration(question.restrictions.enumeration);
            if (question.restrictions.range) {
                setMin(question.restrictions.range.min);
                setMax(question.restrictions.range.max);
                setStep(question.restrictions.range.step);
            }
            if (question.restrictions.text) {
                setRegex(question.restrictions.text.regex);
                setMinLength(question.restrictions.text.minLength);
                setMaxLength(question.restrictions.text.maxLength);
            }
        }

        switch (typeof question.default_value) {
            case 'string':
                setInputValue(question.default_value || "");
                break;
            case 'number':
                setInputValue("" + question.default_value || "0");
                break;
            case 'boolean':
                setInputValue(question.default_value || false);
                break;
        };
        if (question.data_type === 'Text' && question.restrictions.enumeration) {
            setInputValue(question.default_value || question.restrictions.enumeration.possible_values[0].value);
        }

    }, [question]);

    const localizedLabel = () => {
        let text = "";
        if (labels && labels.length > 0) {
            let label = labels.find(label => label.locale === i18n.language);
            if (label) {
                text = label.text;
            } else {
                text = labels[0].text;
            }
        } else {
            text = "Missing data for " + keyName + ": ";
        }

        return text.split('\n').map((line, i) =>
            line === "" ? <br key={i} /> :
                <div key={i}>
                    <ReactMarkdown>{line}</ReactMarkdown>
                </div>
        )
    }

    const handleInputChange = (e) => {
        setInputValue(e.target.value);
    }

    const validateInputText = () => {
        if (!inputValue) {
            setError('Input required');
            return false;
        }
        if (minLength && inputValue.length < minLength) {
            setError('Input too short, minimum length is ' + minLength);
            return false;
        }
        if (maxLength && inputValue.length > maxLength) {
            setError('Input too long, maximum length is ' + maxLength);
            return false;
        }
        if (regex && !new RegExp(regex).test(inputValue)) {
            setError('Invalid input');
            return false;
        }
        setError('');
        return true;
    }
    const validateInput = () => {
        if (!inputValue) {
            setError('Input required');
            return false;
        }
        if (dataType === 'Integer' && "" + parseInt(inputValue) !== inputValue) {
            setError('Input must be an integer');
            return false;
        }
        if (dataType === 'Number' && "" + parseFloat(inputValue) !== inputValue) {
            setError('Input must be a number');
            return false;
        }
        if (min && inputValue < min) {
            setError('Value too low, minimum is ' + min);
            return false;
        }
        if (max && inputValue > max) {
            setError('Value too high, maximum is ' + max);
            return false;
        }
        setError('');
        return true;
    }

    useImperativeHandle(ref, () => ({
        getIndex() {
            return index;
        },
        getAnswer() {
            if (dataType === 'Text') {
                if (enumeration) {
                    return inputValue;
                }
                if (validateInputText()) {
                    return inputValue;
                } else {
                    return null;
                }
            } else if (dataType === 'Boolean') {
                return inputValue;
            } else {
                if (validateInput()) {
                    return inputValue;
                } else {
                    return null;
                }
            }
        },
        getFullAnswer() {
            return {
                index: index,
                key_name: keyName,
                input: this.getAnswer()
            }
        }
    }));

    return (
        <div className="closed-question-input-zone" tabindex="-1">
            <div className="closed-question-label">
                {localizedLabel()}
            </div>
            {dataType === 'Boolean' && (
                <Switch value={inputValue} onClick={() => setInputValue(!inputValue)} justifyContent="flex-start" disabled={disabled} />
            )}
            {dataType === 'Text' && enumeration && (
                <select id={keyName} value={inputValue} onChange={handleInputChange} className="closed-question-select" disabled={disabled}>
                    {enumeration.possible_values.map((value, index) => (
                        <option key={index} value={value.value}>
                            {value.labels.find(label => label.locale === i18n.language).text}
                        </option>
                    ))}
                </select>
            )}
            {dataType === 'Text' && !enumeration && (
                <input id={keyName}
                    type="text"
                    value={inputValue}
                    minLength={minLength}
                    maxLength={maxLength}
                    pattern={regex}
                    onChange={handleInputChange}
                    onBlur={validateInputText}
                    disabled={disabled}
                />
            )}
            {dataType === 'Integer' && (
                <input id={keyName}
                    type="number"
                    value={inputValue}
                    min={min}
                    max={max}
                    step={step}
                    onChange={handleInputChange}
                    onBlur={validateInput}
                    disabled={disabled}
                />
            )}
            {dataType === 'Number' && (
                <input id={keyName}
                    type="number"
                    value={inputValue}
                    min={min}
                    max={max}
                    step={step}
                    onChange={handleInputChange}
                    onBlur={validateInput}
                    disabled={disabled}
                />
            )}
            {dataType === 'Date' && (
                <input id={keyName}
                    type="date"
                    value={inputValue}
                    min={min}
                    max={max}
                    onChange={handleInputChange}
                    onBlur={validateInput}
                    disabled={disabled}
                />
            )}
            {dataType === 'DateTime' && (
                <input id={keyName}
                    type="datetime-local"
                    value={inputValue}
                    min={min}
                    max={max}
                    onChange={handleInputChange}
                    onBlur={validateInput}
                    disabled={disabled}
                />
            )}
            <div className="closed-question-error">{error}</div>
        </div>
    );
});

export default ClosedQuestion;