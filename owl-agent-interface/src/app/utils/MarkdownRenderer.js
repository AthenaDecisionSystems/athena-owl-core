import React from "react";
import ReactMarkdown from 'react-markdown';

const CustomListItem = ({ children }) => {
    // When using ReactMarkdown, the children of <li> of <ol> are wrapped in a <p> tag
    // This causes the items to be displayed on a new line
    // This component removes the <p> tag and displays the children directly
    const newChildren = React.Children.map(children, child => {
        if (child.type === 'p') {
            return child.props.children;
        }
        return child;
    });

    return <li>{newChildren}</li>;
};

const MarkdownRenderer = ({ message }) => (
    <ReactMarkdown
        children={message}
        components={{
            li: CustomListItem,
        }}
    />
);

export default MarkdownRenderer;