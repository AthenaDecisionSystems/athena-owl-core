import React, { useEffect, useState } from 'react';
import { AspectRatio, Column, OverflowMenu, OverflowMenuItem, Popover, PopoverContent, IconButton } from '@carbon/react';
import { Documentation } from '@carbon/pictograms-react';

export const DocumentMap = ({ rows }) => {
    const [openPopoverTable, setOpenPopoverTable] = useState([]);

    useEffect(() => {
        setOpenPopoverTable(new Array(rows.length).fill(false));
    }, [rows]);

    const displayPopoverTable = (index, open) => {
        const newOpenPopoverTable = openPopoverTable.map((item, i) => (i === index ? open : false));
        setOpenPopoverTable(newOpenPopoverTable);
    }

    return (
        <>
            {rows.map((row, i) => (<Column key={i} lg={3} md={2} sm={2} >
                <AspectRatio className="card" ratio="4x3">
                    <div className="card-header" >
                        <Documentation style={{ padding: "0.5rem" }} />
                        <OverflowMenu className="card-menu">
                            <OverflowMenuItem itemText="Open" />
                            <OverflowMenuItem hasDivider isDelete itemText="Delete" />
                        </OverflowMenu>
                    </div>
                    <div className="card-name">{row?.id}</div>
                    {Object.keys(row.metadata).map((key, j) => <>
                        <div className="card-description" key={j}>{key}: {row.metadata[key]}</div>
                    </>)}
                    <div className="card-label">Page content:</div>
                    <div className="card-description">{row.page_content}</div>
                </AspectRatio>
            </Column>
            ))}
        </>
    );
};

export default DocumentMap;
