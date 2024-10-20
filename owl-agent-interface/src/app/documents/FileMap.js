import React, { useEffect, useState } from 'react';
import { AspectRatio, Column, OverflowMenu, OverflowMenuItem, Popover, PopoverContent, IconButton } from '@carbon/react';
import { Documentation } from '@carbon/pictograms-react';

export const FileMap = ({ rows }) => {
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
            {rows.length === 0 && <Column lg={3} md={2} sm={2} >
                <div style={{ display: 'flex', alignItems: 'center', marginTop: '1rem' }} />
                <h4>No File found</h4>
            </Column>}

            {rows.map((row, i) => (
                <Column key={i} lg={3} md={2} sm={2} >
                    <AspectRatio className="card" ratio="4x3">
                        <div className="card-header" >
                            <Documentation style={{ padding: "0.5rem" }} />
                            <OverflowMenu className="card-menu">
                                {/*<OverflowMenuItem itemText="Open" />*/}
                                <OverflowMenuItem hasDivider isDelete itemText="Delete" disabled />
                            </OverflowMenu>
                        </div>
                        <div className="card-name">{row.name}</div>
                        <div className="card-label">Description: {row.description}</div>

                        <div className="card-label">Type: {row.type}</div>
                        <div className="card-label">File base URI: {row.file_base_uri}</div>
                        <div className="card-label">Collection: {row.collection_name}</div>
                    </AspectRatio>
                </Column>
            ))}
        </>
    );
};

export default FileMap;
