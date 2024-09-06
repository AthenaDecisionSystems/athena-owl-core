import React, { forwardRef, useEffect, useImperativeHandle, useRef, useState } from 'react';
import { DatePicker, DatePickerInput, Dropdown, NumberInput, TextInput, TimePicker, Toggle } from '@carbon/react';
import ReactMarkdown from 'react-markdown';
import { useTranslation } from 'react-i18next';

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
    const [dateValue, setDateValue] = useState();
    const [timeValue, setTimeValue] = useState();

    const { t, i18n } = useTranslation();

    const controlRef = useRef(null);

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
        if (question.data_type === 'Boolean') {
            setInputValue(question.default_value || false);
        } else if (question.data_type === 'Text' && question.restrictions.enumeration) {
            setInputValue(question.default_value || question.restrictions.enumeration.possible_values[0].value);
        } else if ((question.data_type === 'Integer' || question.data_type === 'Number') && typeof question.default_value == 'number') {
            setInputValue("" + question.default_value);
        } else if (question.data_type === 'DateTime' && question.default_value) {
            setDateValue(question.default_value.split('T')[0]);
            setTimeValue(question.default_value.split('T')[1]);
        } else {
            setInputValue(question.default_value);
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

        return text;
        return text.split('\n').map((line, i) =>
            line === "" ? <br key={i} /> :
                <div key={i}>
                    <ReactMarkdown>{line}</ReactMarkdown>
                </div>
        )
    }

    const textInputError = (value) => {
        let err = "";
        if (value === "") {
            err = 'Text input required';
        } else if (minLength && value.length < minLength) {
            err = 'Input too short, minimum length is ' + minLength;
        } else if (maxLength && value.length > maxLength) {
            err = 'Input too long, maximum length is ' + maxLength;
        } else if (regex && !new RegExp(regex).test(value)) {
            err = 'Invalid input';
        }
        return err;
    }

    const numericInputError = (value) => {
        let err = "";
        if (value === "") {
            err = 'Numeric input required';
        } else if (dataType === 'Integer' && "" + parseInt(value) !== value) {
            err = 'Input must be an integer';
        } else if (dataType === 'Number' && "" + parseFloat(value) !== value) {
            err = 'Input must be a number';
        } else if (min && value < min) {
            err = 'Numeric value too low, minimum is ' + min;
        } else if (max && value > max) {
            err = 'Numeric value too high, maximum is ' + max;
        }
        return err;
    }

    const dateInputError = (date, time) => {
        const parseDateString = (dateString) => {
            //2024-07-31T17:00
            const [datePart, timePart] = dateString.split('T');
            const [year, month, day] = datePart.split('-');
            const [hours, minutes] = timePart.split(':');

            return new Date(year, month - 1, day, hours, minutes);
        };

        // Check time format (HH:MM)
        if (time && !/^\d{2}:\d{2}$/.test(time)) {
            return 'Invalid time format (HH:MM)';
        }
        const [hours, minutes] = time.split(':');
        if (hours < 0 || hours > 23 || minutes < 0 || minutes > 59) {
            return 'Invalid time format';
        }

        const dateTime = parseDateString(formatDate(date) + "T" + time);
        let err = "";

        if (min && dateTime < parseDateString(min)) {
            err = 'Date is too old, it must be after ' + min;
        } else if (max && dateTime > parseDateString(max)) {
            err = 'Date is to new, it must be before ' + max;
        }
        return err;
    }

    const formatDate = (date) => {
        if (typeof date === 'string') {
            return date;
        }
        const year = date.getFullYear();
        const month = String(date.getMonth() + 1).padStart(2, '0');
        const day = String(date.getDate()).padStart(2, '0');

        return `${year}-${month}-${day}`;
    };

    const formatDateTime = (date, time) => {
        if (typeof date === 'string') {
            return date + "T" + time;
        }
        const year = date.getFullYear();
        const month = String(date.getMonth() + 1).padStart(2, '0');
        const day = String(date.getDate()).padStart(2, '0');

        return `${year}-${month}-${day}T${time}`;
    };

    useImperativeHandle(ref, () => ({
        getIndex() {
            return index;
        },
        getAnswer() {
            if (dataType === 'Boolean') {
                return inputValue;
            } else if (dataType === 'Text') {
                if (enumeration) {
                    return inputValue;
                } else if (textInputError(inputValue) === "") {
                    return inputValue;
                } else {
                    return null;
                }
            } else if (dataType === 'Integer' || dataType === 'Number') {
                if (numericInputError(inputValue) === "") {
                    return inputValue;
                } else {
                    return null;
                }
            } else if (dataType === 'DateTime') {
                if (dateInputError(dateValue, timeValue) === "") {
                    return formatDateTime(dateValue, timeValue);
                } else {
                    return null;
                }
            } else {
                // dataType === 'Date'
                return formatDate(inputValue);
            }
        },
        getFullAnswer() {
            const answer = this.getAnswer();
            return {
                index: index,
                key_name: keyName,
                input: typeof answer === 'boolean' ? (answer ? "true" : "false") : answer
            }
        }
    }));

    if (dataType === 'Boolean') return (
        <Toggle id={keyName + Math.random().toString(36)}
            labelText={localizedLabel()}
            defaultToggled={inputValue}
            labelA="No"
            labelB="Yes"
            onClick={() => setInputValue(!inputValue)}
            disabled={disabled} />
    )
    if (dataType === 'Text' && enumeration) return (
        <Dropdown id={keyName}
            titleText={localizedLabel()}
            items={enumeration.possible_values}
            selectedItem={inputValue ? enumeration.possible_values.find(item => item.value === inputValue) : null}
            itemToString={item => item ? item.labels.find(label => label.locale === i18n.language).text : ''}
            onChange={({ selectedItem }) => setInputValue(selectedItem.value)}
            disabled={disabled} />
    )
    if (dataType === 'Text' && !enumeration) return (
        <TextInput id={keyName}
            labelText={localizedLabel()}
            value={inputValue}
            minLength={minLength}
            maxLength={maxLength}
            pattern={regex}
            onChange={e => setInputValue(e.target.value)}
            invalid={textInputError(inputValue) !== ""}
            invalidText={textInputError(inputValue)}
            disabled={disabled} />
    )
    if (dataType === 'Integer' || dataType === 'Number') return (
        <NumberInput id={keyName} ref={controlRef}
            label={localizedLabel()}
            value={inputValue}
            {...(min && { min })}
            {...(max && { max })}
            step={step}
            onChange={() => setInputValue(controlRef.current.value)}
            invalid={numericInputError(inputValue) !== ""}
            invalidText={numericInputError(inputValue)}
            disabled={disabled} />
    )
    if (dataType === 'Date') return (
        <DatePicker
            datePickerType="single"
            dateFormat="Y-m-d"
            {...(min && { minDate: min })}
            {...(max && { maxDate: max })}
            onChange={dates => setInputValue(dates[0])}>
            <DatePickerInput
                id={keyName}
                value={formatDate(inputValue)}
                labelText={localizedLabel()}
                disabled={disabled} />
        </DatePicker>
    )
    if (dataType === 'DateTime') return (<div style={{ display: "flex", alignItems: "flex-end" }}>
        <DatePicker
            datePickerType="single"
            dateFormat="Y-m-d"
            {...(min && { minDate: min })}
            {...(max && { maxDate: max })}
            onChange={dates => setDateValue(dates[0])}>
            <DatePickerInput
                id={keyName}
                value={formatDate(dateValue)}
                labelText={localizedLabel()}
                invalid={dateInputError(dateValue, timeValue) !== ""}
                invalidText={dateInputError(dateValue, timeValue)}
                disabled={disabled} />
        </DatePicker >
        <TimePicker id="time-picker"
            labelText="Time"
            value={timeValue}
            onChange={e => setTimeValue(e.target.value === "" ? "00:00" : e.target.value)}
            invalid={dateInputError(dateValue, timeValue) !== ""}
            invalidText={dateInputError(dateValue, timeValue) !== "" ? "." : ""}
            disabled={disabled} />
    </div >)
});

export default ClosedQuestion;